import React, { useState } from 'react';

const ChatInput = ({ onSendPrompt }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSendPrompt(prompt);
      setPrompt('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chatInputForm">
      <div className="chatInputContainer">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your message..."
          className="chatInputField"
        />
        <button type="submit" className="sendButton">
          Send
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
