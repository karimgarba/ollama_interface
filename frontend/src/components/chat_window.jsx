import React from 'react';

const ChatWindow = ({ chat_messages }) => {
  return (
    <div className="chat_window_container">
      {chat_messages.length === 0 ? (
        <p>no messages yet...</p>
      ) : (
        chat_messages.map((message, idx) => (
          <div key={idx} className="chat_message">
            <span className="message_sender">{message.sender}: </span>
            <span className="message_content">{message.content}</span>
          </div>
        ))
      )}
    </div>
  );
};

export default ChatWindow;
