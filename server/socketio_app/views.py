async_mode = None

import os

import socketio
from online_users import online_users
from dotenv import dotenv_values
import jwt

basedir = os.path.dirname(os.path.realpath(__file__))

env_vars = dotenv_values('.env')
CLIENT_ORIGIN = env_vars.get("CLIENT_ORIGIN")
cao = CLIENT_ORIGIN if CLIENT_ORIGIN else "http://localhost:8000/"

sio = socketio.Server(cors_allowed_origins=cao, async_mode=async_mode, logger=False)
thread = None


@sio.event
def connect(sid, environ, token=None):
    try:
        jwt.decode(token, env_vars.get("SECRET_KEY"), algorithms="HS256")
        sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)

    except Exception as e:
        print("Invalid connection request")
        sio.disconnect(sid)


@sio.on("go-online")
def go_online(sid, user_id):
    if user_id not in online_users:
        online_users[user_id] = sid
    sio.emit("add-online-user", user_id, skip_sid=sid)


@sio.on("new-message")
def new_message(sid, message):
    recipient_userid = message["recipientId"]
    recipient_sid = online_users.get(recipient_userid)

    if recipient_sid:
        sio.emit(
            "new-message",
            {"message": message["message"], "sender": message["sender"], "recipientId": recipient_userid},
            skip_sid=sid, room=recipient_sid
        )


@sio.on("logout")
def logout(sid, user_id):
    if user_id in online_users:
        online_users.pop(user_id)
    sio.emit("remove-offline-user", user_id, skip_sid=sid)
    sio.disconnect(sid)


@sio.on("update-read")
def update_read(sid, user_id):
    room_id = online_users.get(user_id)

    if room_id:
        sio.emit("update-read", skip_sid=sid, room=room_id)
