import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const ChatWindow = ({ chatMessages = [] }) => {
  // Function to parse content and identify code blocks
  const parseMessageContent = (content) => {
    // Check if the content has code blocks with markdown syntax
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;
    
    // If there are no code blocks, return the content as is
    if (!content || typeof content !== 'string' || !content.includes('```')) {
      return [{ type: 'text', content: content || '' }];
    }
    
    // Extract code blocks and text parts
    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Add text before the code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.substring(lastIndex, match.index)
        });
      }
      
      // Add the code block with language info
      parts.push({
        type: 'code',
        language: match[1] || 'python', // Default to python if no language specified
        content: match[2].trim()
      });
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text after the last code block
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.substring(lastIndex)
      });
    }
    
    return parts;
  };
  
  // Function to render a message part (text or code)
  const renderMessagePart = (part, partIndex) => {
    if (part.type === 'code') {
      return (
        <div key={partIndex} className="codeBlock">
          <div className="codeHeader">
            <span className="codeLanguage">{part.language}</span>
            <button 
              className="copyButton"
              onClick={() => navigator.clipboard.writeText(part.content)}
            >
              Copy
            </button>
          </div>
          <SyntaxHighlighter
            language={part.language}
            style={vscDarkPlus}
            showLineNumbers={true}
          >
            {part.content}
          </SyntaxHighlighter>
        </div>
      );
    } else {
      return <p key={partIndex} className="textContent">{part.content}</p>;
    }
  };

  // Format timestamp
  const formatTimestamp = () => {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chatWindowContainer">
      {(!chatMessages || chatMessages.length === 0) ? (
        <p className="emptyStateMessage">No messages yet. Start a conversation!</p>
      ) : (
        chatMessages.map((message, idx) => {
          // Added defensive check for message properties
          if (!message || !message.content) {
            console.warn(`Invalid message at index ${idx}:`, message);
            return null;
          }
          
          return (
            <div 
              key={idx} 
              className={`chatMessage ${message.sender}Message`}
              data-time={formatTimestamp()}
            >
              <div className="messageSender">{message.sender}</div>
              <div className="messageContent">
                {parseMessageContent(message.content).map((part, partIndex) => 
                  renderMessagePart(part, partIndex)
                )}
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default ChatWindow;