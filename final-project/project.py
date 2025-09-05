# Final Project Starter Template

"""
CS50 Final Project Template
Replace this with your actual project implementation.

This template provides a basic structure that you can modify for your specific project.
"""

import sqlite3
from datetime import datetime
import json
import os

class ProjectApp:
    """Main application class for your CS50 final project."""
    
    def __init__(self):
        """Initialize the application."""
        self.db_name = 'project.db'
        self.init_database()
        
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Example table - modify for your project
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add more tables as needed for your project
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                data_field TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_user(self, username, email):
        """Create a new user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, email) VALUES (?, ?)',
                (username, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user(self, user_id):
        """Get user information by ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return user
    
    def save_data(self, user_id, data_field, value):
        """Save project-specific data."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO project_data (user_id, data_field, value)
            VALUES (?, ?, ?)
        ''', (user_id, data_field, value))
        
        conn.commit()
        conn.close()
    
    def get_user_data(self, user_id):
        """Get all data for a specific user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data_field, value, created_at 
            FROM project_data 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        
        data = cursor.fetchall()
        conn.close()
        
        return data

def main():
    """Main function - replace with your project's main logic."""
    print("CS50 Final Project")
    print("==================")
    
    # Initialize your application
    app = ProjectApp()
    
    # Your main application logic goes here
    print("Project initialized successfully!")
    print("Replace this with your actual project implementation.")
    
    # Example usage:
    # user_id = app.create_user("testuser", "test@example.com")
    # if user_id:
    #     print(f"Created user with ID: {user_id}")
    #     app.save_data(user_id, "example_field", "example_value")
    #     user_data = app.get_user_data(user_id)
    #     print(f"User data: {user_data}")

if __name__ == "__main__":
    main()

# Project Development Checklist:
# ================================
# 
# 1. Planning Phase:
#    □ Define your project idea clearly
#    □ List all features you want to implement
#    □ Choose your technology stack
#    □ Create mockups or wireframes
#    □ Plan your database schema
# 
# 2. Setup Phase:
#    □ Set up development environment
#    □ Install required libraries/frameworks
#    □ Create project structure
#    □ Initialize version control (git)
# 
# 3. Implementation Phase:
#    □ Implement core functionality first
#    □ Add features incrementally
#    □ Test each feature as you build
#    □ Handle errors gracefully
#    □ Add input validation
# 
# 4. Polish Phase:
#    □ Improve user interface/experience
#    □ Add documentation and comments
#    □ Test edge cases
#    □ Optimize performance
#    □ Add error handling
# 
# 5. Completion Phase:
#    □ Create comprehensive README.md
#    □ Write design document
#    □ Record demonstration video
#    □ Test final version thoroughly
#    □ Prepare for submission
# 
# Remember: Start simple and add complexity gradually!
# Your final project should demonstrate what you've learned in CS50.
