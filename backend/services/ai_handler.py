"""
module: backend.services.ai_handler
description: This module contains the AIHandler class, which is responsible for handling AI-related tasks.
It includes methods for generating text completions using users selected AI model.
author: Karim Garba
date_created: 05-04-25
date_modified: 08-04-25
last_modified_by: Karim Garba
version: 0.1
"""
import ollama
import uuid
import os

from .db_handler import DatabaseHandler

class AIHandler:
    """
    This class handles AI-related tasks, including generating text completions using the selected AI model.
    """
    def __init__(self, db_handler=None):
        """
        Initializes the AIHandler class.
        Args:
            db_handler (DatabaseHandler): An instance of the DatabaseHandler class.
        """
        self.models = self.get_models()
        self.current_model = None
        self.chat_history = []
        self.current_session_id = str(uuid.uuid4())

        if db_handler:
            self.db_handler = db_handler
        else:
            db_path = os.getenv('DB_PATH', 'assistant.db')
            self.db_handler = DatabaseHandler(db_path=db_path)

    def get_models(self):
        """
        Retrieves the list of available AI models from the Ollama API.
        Returns:
            list: A list of available AI model names.
        """
        try:
            models = ollama.list()
            return [model.model for model in models.get("models", [])]
        except Exception as e:
            print(f"Error retrieving models: {e}")
            return []
        
    
    def set_model(self, model_name):
        """
        Sets the selected AI model.
        Args:
            model_name (str): The name of the model to set.
        """
        if model_name in self.models:
            self.current_model = model_name
        else:
            raise ValueError(f"Model {model_name} is not available.")
        
    def clear_chat_history(self):
        """
        Clears the chat history.
        """
        self.chat_history = []

        self.current_session_id = str(uuid.uuid4())
        if self.current_model:
            self.db_handler.add_chat_session(self.current_session_id, self.current_model)

    def add_to_chat_history(self, role, content):
        """
        Adds a message to the chat history.
        Args:
            role (str): The role of the message sender (e.g., user, assistant).
            content (str): The message to add to the chat history.
        """
        message = {
            "role": role,
            "content": content
        }
        self.chat_history.append(message)

        if self.current_model:
            self.db_handler.add_chat_session(self.current_session_id, self.current_model)
            self.db_handler.add_chat_message(self.current_session_id, role, content)


    def set_session_id(self, session_id):
        """
        Sets the session ID for the current chat.
        Args:
            session_id (str): The session ID to set.
        """
        self.current_session_id = session_id
        self.chat_history = self.db_handler.get_chat_history(session_id)

    
    def generate_response(self, prompt, system_prompt=None):
        """
        Generates a response from the AI model based on the provided prompt and chat history.

        Args:
            prompt (str): The user prompt.
            system_prompt (str, optional): A system prompt to guide the AI's response.
        Returns:
            str: The generated response from the AI model.
        """

        if not self.current_model:
            raise ValueError("No model selected. Please select a model before generating a response.")
        
        self.add_to_chat_history("user", prompt)
        messsages = []

        if "python" in prompt.lower() or "code" in prompt.lower():
            # Add system guidance for code formatting if the prompt mentions code
            code_formatting_guidance = """
            When providing code examples, especially Python code, format them using markdown code blocks with 
            language specification. For example:
            ```python
            def example_function():
                return "Hello World"
            ```
            """
            
            if system_prompt:
                system_prompt += "\n" + code_formatting_guidance
            else:
                system_prompt = code_formatting_guidance

        if system_prompt:
            messsages.append({"role": "system", "content": system_prompt})

        for message in self.chat_history:
            messsages.append({"role": message["role"], "content": message["content"]})
        
        try:
            response = ollama.chat(
                model=self.current_model,
                messages=messsages,
            )
            
            assistant_response = response["message"]["content"]
            self.add_to_chat_history("assistant", assistant_response)
            
            return assistant_response
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, but I couldn't generate a response at this time."
        
    def get_sessions(self):
        """
        Retrieves all chat sessions from the database.
        Returns:
            list: A list of chat sessions.
        """
        return self.db_handler.get_chat_sessions()
    
    def get_session(self, session_id):
        """
        Retrieves a specific chat session from the database.
        Args:
            session_id (str): The ID of the chat session.
        Returns:
            dict: The chat session data.
        """
        return self.db_handler.get_chat_session(session_id)
    


def test_ai_handler():
    """
    Test function for the AIHandler class.
    """
    db_handler = DatabaseHandler(db_path='test_assistant.db')
    ai_handler = AIHandler(db_handler=db_handler)

    # Test model retrieval
    models = ai_handler.get_models()
    assert isinstance(models, list), "Models should be a list."

    # Test model selection
    if models:
        ai_handler.set_model(models[0])
        assert ai_handler.current_model == models[0], "Model selection failed."

    # Test chat history management
    ai_handler.clear_chat_history()
    assert len(ai_handler.chat_history) == 0, "Chat history should be empty after clearing."

    # Test adding to chat history
    ai_handler.add_to_chat_history("user", "Hello!")
    assert len(ai_handler.chat_history) == 1, "Chat history should contain one message."

    # Test generating response
    response = ai_handler.generate_response("Hello!")
    assert isinstance(response, str), "Response should be a string."

    # Test session management
    ai_handler.set_session_id(ai_handler.current_session_id)
    sessions = ai_handler.get_sessions()
    assert isinstance(sessions, list), "Sessions should be a list."

    # Test getting a specific session
    if sessions:
        session = ai_handler.get_session(sessions[0]['session_id'])
        assert isinstance(session, dict), "Session should be a dictionary."

    # Clean up test database
    db_handler.connection.close()
    os.remove('test_assistant.db')

def main():
    """
    Main function to test the AIHandler class.
    """
    test_ai_handler()
    print("All tests passed!")

if __name__ == "__main__":
    main()