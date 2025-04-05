"""
module: backend.services.ai_handler
description: This module contains the AIHandler class, which is responsible for handling AI-related tasks.
It includes methods for generating text completions using users selected AI model.
author: Karim Garba
date_created: 05-04-25
date_modified: 05-04-25
last_modified_by: Karim Garba
version: 0.1
"""
import ollama

class AIHandler:
    """
    This class handles AI-related tasks, including generating text completions using the selected AI model.
    """
    def __init__(self):
        """
        Initializes the AIHandler class.
        """
        self.models = self.get_models()
        self.selected_model = None

    def get_models(self):
        """
        Retrieves the list of available AI models from the Ollama API.
        Returns:
            list: A list of available AI model names.
        """
        
        models = ollama.list()
        return [model.model for model in models.get("models", [])]
    
    def set_model(self, model_name):
        """
        Sets the selected AI model.
        Args:
            model_name (str): The name of the model to set.
        """
        if model_name in self.models:
            self.selected_model = model_name
        else:
            raise ValueError(f"Model {model_name} is not available.")

    def generate_text(self, prompt):
        """
        Generates text using the selected AI model.
        Args:
            prompt (str): The input prompt for text generation.
        Returns:
            str: The generated text.
        """
        if self.selected_model is None:
            raise ValueError("No model selected.")
        

def main():
    """
    Main function to test the AIHandler class.
    """
    ai_handler = AIHandler()
    print(ai_handler.get_models())

if __name__ == "__main__":
    main()