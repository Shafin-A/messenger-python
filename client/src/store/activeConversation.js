const SET_ACTIVE_CHAT = "SET_ACTIVE_CHAT";

export const setActiveChat = (conversation) => {
  return {
    type: SET_ACTIVE_CHAT,
    username: conversation.otherUser.username,
  };
};

const reducer = (state = "", action) => {
  switch (action.type) {
    case SET_ACTIVE_CHAT: {
      return action.username;
    }
    default:
      return state;
  }
};

export default reducer;
