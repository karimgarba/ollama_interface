import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DropdownModel from './components/dropdown_model';
import ChatSidebar from './components/chat_sidebar';
import ChatWindow from './components/chat_window';
import ChatInput from './components/chat_input';

// Configure axios with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000'  // Adjust this to your API's actual URL
});

const App = () => {
  const [selected_model, set_selected_model] = useState('');
  const [model_list, set_model_list] = useState([]);
  const [chat_sessions, set_chat_sessions] = useState([]);
  const [current_session_id, set_current_session_id] = useState(null);
  const [chat_messages, set_chat_messages] = useState([]);

  // Fetch available AI models on mount
  useEffect(() => {
    const fetch_model_list = async () => {
      try {
        const response = await api.get('/api/models');
        console.log('Models response:', response.data);
        set_model_list(response.data.models || []);
      } catch (error) {
        console.error('error fetching models:', error);
      }
    };
    fetch_model_list();
  }, []);

  // Fetch chat sessions on mount
  useEffect(() => {
    fetch_chat_sessions();
  }, []);

  // Fetch chat sessions
  const fetch_chat_sessions = async () => {
    try {
      const response = await api.get('/api/sessions');
      
      // Filter out duplicate sessions based on session_id
      const unique_sessions = [];
      const session_ids = new Set();
      
      if (response.data && response.data.sessions) {
        response.data.sessions.forEach(session => {
          if (!session_ids.has(session.session_id)) {
            session_ids.add(session.session_id);
            unique_sessions.push(session);
          }
        });
      }
      
      set_chat_sessions(unique_sessions);
    } catch (error) {
      console.error('Error fetching sessions:', error.response?.data || error.message);
    }
  };

  // Function to load a chat session
  const load_chat_session = async (session_id) => {
    try {
      const response = await api.get(`/api/sessions/${session_id}`);
      set_current_session_id(session_id);
      set_chat_messages(response.data.messages || []);
    } catch (error) {
      console.error('error loading session:', error);
    }
  };

  // Create a new chat session
  const create_new_session = async () => {
    // Clear current messages
    set_chat_messages([]);
    
    // Generate a new session ID
    const new_session_id = crypto.randomUUID();
    set_current_session_id(new_session_id);
    
    try {
      // Add new session to database if a model is selected
      if (selected_model) {
        await api.post('/api/sessions/create', {
          session_id: new_session_id,
          model_name: selected_model
        });
        
        // Refresh sessions list
        fetch_chat_sessions();
      }
    } catch (error) {
      console.error('Error creating new session:', error);
    }
  };

  // Function to send a chat prompt
  const send_chat_prompt = async (prompt_text) => {
    try {
      // Add user message to chat messages
      const new_message = {
        sender: 'user',
        content: prompt_text
      };
      
      set_chat_messages(prev_messages => [...prev_messages, new_message]);
      
      const response = await api.post('/api/chat', {
        prompt: prompt_text,
        model_name: selected_model,
        session_id: current_session_id
      });
      
      // Add assistant response if available
      if (response.data && response.data.response) {
        const assistant_message = {
          sender: 'assistant',
          content: response.data.response
        };
        set_chat_messages(prev_messages => [...prev_messages, assistant_message]);
      }
      
      // Refresh sessions list
      fetch_chat_sessions();
    } catch (error) {
      console.error('Error sending prompt:', error.response?.data || error);
    }
  };

  // Function to handle model selection change
  const handle_model_change = async (new_model) => {
    set_selected_model(new_model);
    try {
      await api.post('/api/models/select', { model_name: new_model });
    } catch (error) {
      console.error('error selecting model:', error);
    }
  };

  return (
    <div className="app_container">
      <div className="header">
        <DropdownModel
          model_list={model_list}
          selected_model={selected_model}
          on_model_change={handle_model_change}
        />
      </div>
      <div className="main_content">
        <div className="sidebar">
          <ChatSidebar 
            chat_sessions={chat_sessions} 
            on_select_session={load_chat_session}
            on_create_new_session={create_new_session}
            active_session_id={current_session_id}
          />
        </div>
        <div className="chat_area">
          <ChatWindow chat_messages={chat_messages} />
          <ChatInput on_send_prompt={send_chat_prompt} />
        </div>
      </div>
    </div>
  );
};

export default App;