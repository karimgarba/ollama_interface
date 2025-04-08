import React from "react";

const ChatSidebar = ({ chat_sessions, on_select_session, on_create_new_session, active_session_id }) => {
    // Function to format session name
    const format_session_name = (session) => {
        // Use timestamp or first few chars of ID for better display
        const short_id = session.session_id.substring(0, 8);
        const date = new Date(session.created_at).toLocaleString();
        return `Chat ${short_id} (${date})`;
    };

    return (
        <div className="chat_sidebar_container">
            <div className="sidebar_header">
                <h3>Chat Sessions</h3>
                <button 
                    onClick={on_create_new_session}
                    className="new_session_button"
                >
                    New Chat
                </button>
            </div>
            <ul className="session_list">
                {chat_sessions.length > 0 ? (
                    chat_sessions.map((session) => (
                        <li 
                            key={`session-${session.session_id}-${session.created_at}`} 
                            onClick={() => on_select_session(session.session_id)}
                            className={`session_item ${session.session_id === active_session_id ? 'active' : ''}`}
                        >
                            {format_session_name(session)}
                        </li>
                    ))
                ) : (
                    <li className="session_item">No chat sessions found</li>
                )}
            </ul>
        </div>
    );
};

export default ChatSidebar;
