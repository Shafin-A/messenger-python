import React from "react";
import { Box, Avatar } from "@material-ui/core";
import { SenderBubble, OtherUserBubble } from "../ActiveChat";
import moment from "moment";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  avatarContainer: {
    display: "flex",
    justifyContent: 'flex-end',
  },
  avatar: {
    height: theme.spacing(2.5),
    width: theme.spacing(2.5),
    margin: '3px',
  }
}));

const Messages = (props) => {
  const { messages, otherUser, userId } = props;
  const classes = useStyles();

  const lastReadMessage = messages.filter((message) => 
    message.senderId === userId && message.read
  ).pop();

  return (
    <Box>
      {messages.map((message) => {
        const time = moment(message.createdAt).format("h:mm");

        return message.senderId === userId ? (
          <div>
            <SenderBubble key={message.id} text={message.text} time={time} />
            { message === lastReadMessage ? 
            <div className={classes.avatarContainer}>
              <Avatar alt={otherUser.username} src={otherUser.photoUrl} className={classes.avatar} />
            </div>
             : ''}
          </div>
        ) : (
          <OtherUserBubble key={message.id} text={message.text} time={time} otherUser={otherUser} />
        );
      })}
    </Box>
  );
};

export default Messages;
