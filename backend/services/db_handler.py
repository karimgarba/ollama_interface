"""
module: backend.services.db_handler
description: This module contains the DatabaseHandler class, which is responsible for handling database operations.
author: Karim Garba
date_created: 07-04-25
date_modified: 08-04-25
last_modified_by: Karim Garba
version: 0.2
"""
import json
import os
import sqlite3

from datetime import datetime

class DatabaseHandler:
    """
    This class handles database operations, including creating and managing the database and its tables.
    """
    def __init__(self, db_path='database.db'):
        """
        Initializes the DatabaseHandler class.
        Args:
            db_path (str): The path to the database file.
        """
        self.db_path = os.getenv('DB_PATH', db_path)
        self.connection = None
        self.cursor = None
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        """
        Creates a connection to the SQLite database.
        If the database file does not exist, it will be created.
        """
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None
        self.db_path = None

    def create_tables(self):
        """
        Creates the necessary tables in the database.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                memory TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
            )
        ''')
        self.connection.commit()

    def add_chat_session(self, session_id, model):
        """
        Adds a new chat session to the database.
        Args:
            session_id (str): The ID of the chat session.
            model (str): The AI model used for the chat.
        """
        try:
            self.cursor.execute('''
                INSERT INTO chat_sessions (session_id, model) VALUES (?, ?)
            ''', (session_id, model))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # Session ID already exists, handle as needed
            return False

   

    def add_chat_message(self, session_id, role, content):
        """
        Adds a chat message to the database.
        Args:
            session_id (str): The ID of the chat session.
            role (str): The role of the message sender (e.g., user, assistant).
            content (str): The content of the message.
        """
        self.cursor.execute('''
            INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)
        ''', (session_id, role, content))
        self.connection.commit()

    def add_memory(self, session_id, memory):
        """
        Adds a memory to the database.
        Args:
            session_id (str): The ID of the chat session.
            memory (str): The memory to be stored.
        """
        self.cursor.execute('''
            INSERT INTO memories (session_id, memory) VALUES (?, ?)
        ''', (session_id, memory))
        self.connection.commit()

    def get_chat_history(self, session_id):
        """
        Retrieves the chat history for a given session ID.
        Args:
            session_id (str): The ID of the chat session.
        Returns:
            list: A list of chat messages for the session.
        """
        self.cursor.execute('''
            SELECT * FROM chat_messages WHERE session_id = ? ORDER BY created_at
        ''', (session_id,))
        return [dict(row) for row in self.cursor.fetchall()]
        
    
    def get_memories(self, session_id=None):
        """
        Retrieves the memories, optionally filtered by session ID.
        Args:
            session_id (str, optional): The ID of the chat session.
        Returns:
            list: A list of memories for the session.
        """
        if session_id:
            self.cursor.execute('''
                SELECT * FROM memories WHERE session_id = ? ORDER BY created_at
            ''', (session_id,))
        else:
            self.cursor.execute('''
                SELECT * FROM memories ORDER BY created_at
            ''')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_chat_sessions(self):
        """
        Retrieves all chat sessions from the database.
        Returns:
            list: A list of chat sessions.
        """
        self.cursor.execute('''
            SELECT * FROM chat_sessions ORDER BY created_at DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_chat_session(self, session_id):
        """
        Retrieves a specific chat session from the database.
        Args:
            session_id (str): The ID of the chat session.
        Returns:
            dict: The chat session data.
        """
        self.cursor.execute('''
            SELECT * FROM chat_sessions WHERE session_id = ?
        ''', (session_id,))
        return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None
       
    
    def get_model_chat_sessions(self, model):
        """
        Retrieves all chat sessions for a given model.
        Args:
            model (str): The AI model used for the chat.
        Returns:
            list: A list of chat sessions for the model.
        """
        self.cursor.execute('''
            SELECT * FROM chat_sessions WHERE model = ?
        ''', (model,))
        return [dict(row) for row in self.cursor.fetchall()]
    

