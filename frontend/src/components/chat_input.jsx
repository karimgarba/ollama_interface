import React, { useState } from 'react';

const ChatInput = ({ on_send_prompt }) => {
  const [prompt_text, set_prompt_text] = useState('');

  const handle_submit = (e) => {
    e.preventDefault();
    if (prompt_text.trim() === '') return;
    on_send_prompt(prompt_text);
    set_prompt_text('');
  };

  return (
    <form className="chat_input_container" onSubmit={handle_submit}>
      <input
        type="text"
        value={prompt_text}
        onChange={(e) => set_prompt_text(e.target.value)}
        placeholder="enter your prompt..."
        className="chat_input_field"
      />
      <button type="submit" className="chat_input_button">
        send
      </button>
    </form>
  );
};

export default ChatInput;
