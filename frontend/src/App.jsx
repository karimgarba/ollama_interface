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
  const [selectedModel, setSelectedModel] = useState('');
  const [modelList, setModelList] = useState([]);
  const [chatSessions, setChatSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);

  // Fetch available AI models on mount
  useEffect(() => {
    const fetchModelList = async () => {
      try {
        const response = await api.get('/api/models');
        console.log('Models response:', response.data);
        setModelList(response.data.models || []);
      } catch (error) {
        console.error('error fetching models:', error);
      }
    };
    fetchModelList();
  }, []);

  // Fetch chat sessions on mount
  useEffect(() => {
    fetchChatSessions();
  }, []);

  // Fetch chat sessions
  const fetchChatSessions = async () => {
    try {
      const response = await api.get('/api/sessions');
      
      // Filter out duplicate sessions based on session_id
      const uniqueSessions = [];
      const sessionIds = new Set();
      
      if (response.data && response.data.sessions) {
        response.data.sessions.forEach(session => {
          if (!sessionIds.has(session.session_id)) {
            sessionIds.add(session.session_id);
            uniqueSessions.push(session);
          }
        });
      }
      
      setChatSessions(uniqueSessions);
    } catch (error) {
      console.error('Error fetching sessions:', error.response?.data || error.message);
    }
  };

  // Function to load a chat session
  const loadChatSession = async (sessionId) => {
    try {
      const response = await api.get(`/api/sessions/${sessionId}`);
      setCurrentSessionId(sessionId);
      setChatMessages(response.data.messages || []);
    } catch (error) {
      console.error('error loading session:', error);
    }
  };

  // Create a new chat session
  const createNewSession = async () => {
    // Clear current messages
    setChatMessages([]);
    
    // Generate a new session ID
    const newSessionId = crypto.randomUUID();
    setCurrentSessionId(newSessionId);
    
    try {
      // Add new session to database if a model is selected
      if (selectedModel) {
        await api.post('/api/sessions/create', {
          session_id: newSessionId,
          model_name: selectedModel
        });
        
        // Refresh sessions list
        fetchChatSessions();
      }
    } catch (error) {
      console.error('Error creating new session:', error);
    }
  };

  // Function to send a chat prompt
  const sendChatPrompt = async (promptText) => {
    // Add user message to chat messages
    setChatMessages(prevMessages => [
      ...prevMessages, 
      { sender: 'user', content: promptText }
    ]);
    
    try {
      const response = await api.post('/api/chat', {
        prompt: promptText,
        model_name: selectedModel,
        session_id: currentSessionId
      });
      
      // Add assistant response if available
      if (response.data && response.data.response) {
        setChatMessages(prevMessages => [
          ...prevMessages, 
          { sender: 'assistant', content: response.data.response }
        ]);
      }
      
      // Refresh sessions list
      fetchChatSessions();
    } catch (error) {
      console.error('Error sending prompt:', error.response?.data || error);
    }
  };

  // Function to handle model selection change
  const handleModelChange = async (newModel) => {
    setSelectedModel(newModel);
    try {
      await api.post('/api/models/select', { model_name: newModel });
    } catch (error) {
      console.error('error selecting model:', error);
    }
  };

  return (
    <div className="appContainer">
      <div className="header">
        <DropdownModel
          model_list={modelList}
          selected_model={selectedModel}
          on_model_change={handleModelChange}
        />
      </div>
      <div className="mainContent">
        <div className="sidebar">
          <ChatSidebar 
            chat_sessions={chatSessions} 
            on_select_session={loadChatSession}
            on_create_new_session={createNewSession}
            active_session_id={currentSessionId}
          />
        </div>
        <div className="chatArea">
          <ChatWindow chatMessages={chatMessages} />
          <ChatInput onSendPrompt={sendChatPrompt} />
        </div>
      </div>
    </div>
  );
};

export default App;