from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                .all()
            )

            conversations_response = []
            empty_message_convos = []

            for convo in conversations:
                convo_dict = {
                    "id": convo.id,
                    "messages": [
                        message.to_dict(["id", "text", "senderId", "createdAt", "read"])
                        for message in convo.messages.all()
                    ],
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"] if convo_dict["messages"] else None

                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                convo_dict["unreadCount"] = 0

                for message in convo_dict["messages"]:
                    if not message["read"] and message["senderId"] != user_id:
                        convo_dict["unreadCount"] += 1

                read_messages = list(filter(lambda message: message["read"] and message["senderId"] == user_id, convo_dict["messages"]))

                convo_dict["lastReadMessage"] = read_messages[-1] if read_messages else None
                
                # add to empty_message_convos in case messages is empty
                conversations_response.append(convo_dict) if convo_dict["messages"] else empty_message_convos.append(convo_dict)
                    
            conversations_response.sort(
                key=lambda convo: convo["messages"][-1]["createdAt"],
                reverse=True,
            )
            
            # conversations with empty messages will show up at the end
            conversations_response.extend(empty_message_convos)

            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)
