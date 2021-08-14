import io from "socket.io-client";
import store from "./store";
import {
  setNewMessage,
  removeOfflineUser,
  addOnlineUser,
} from "./store/conversations";
import { fetchConversations } from "./store/utils/thunkCreators";


const socket = io(window.location.origin,
  {
    auth: async (cb) => {
      cb(localStorage.getItem("messenger-token"));
    }
  });

socket.on("connect", async () => {
  if (!socket.auth.token) {
    socket.auth.token = await localStorage.getItem("messenger-token");
  }
  console.log("connected to server");

});

socket.on("add-online-user", (id) => {
  store.dispatch(addOnlineUser(id));
});

socket.on("remove-offline-user", (id) => {
  store.dispatch(removeOfflineUser(id));
});

socket.on("new-message", (data) => {
  store.dispatch(setNewMessage(data.message, data.sender, data.recipientId));
});

socket.on("update-read", async () => {
  try {
    store.dispatch(fetchConversations())
  } catch (error) {
    console.error(error);
  }

});

export default socket;
