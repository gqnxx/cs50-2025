# Example 2: Simple Quiz Game (Python with Tkinter)

"""
Quiz Game - A desktop application for multiple choice questions.

Features:
- Multiple choice questions with 4 options
- Score tracking
- Timer for each question
- Categories (Science, History, Sports, etc.)
- High score persistence

Tech Stack:
- Python Tkinter for GUI
- JSON for question storage
- File I/O for high scores
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import time

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CS50 Quiz Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Game state
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.time_left = 30
        self.timer_running = False
        
        # Load questions
        self.load_questions()
        
        # Create UI
        self.create_widgets()
        
        # Start game
        self.start_game()
    
    def load_questions(self):
        """Load questions from JSON file or create sample questions."""
        sample_questions = [
            {
                "question": "What does CPU stand for?",
                "options": ["Central Processing Unit", "Computer Personal Unit", "Central Processor Unit", "Computer Processing Unit"],
                "correct": 0,
                "category": "Computer Science"
            },
            {
                "question": "Which programming language is known as the 'mother of all languages'?",
                "options": ["Python", "C", "Java", "Assembly"],
                "correct": 1,
                "category": "Computer Science"
            },
            {
                "question": "What year was the World Wide Web invented?",
                "options": ["1989", "1991", "1993", "1995"],
                "correct": 0,
                "category": "Technology"
            },
            {
                "question": "Which company developed the Java programming language?",
                "options": ["Microsoft", "Apple", "Sun Microsystems", "IBM"],
                "correct": 2,
                "category": "Technology"
            },
            {
                "question": "What does HTML stand for?",
                "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlink and Text Markup Language"],
                "correct": 0,
                "category": "Web Development"
            }
        ]
        
        try:
            with open('questions.json', 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            self.questions = sample_questions
            # Save sample questions for future use
            with open('questions.json', 'w') as f:
                json.dump(sample_questions, f, indent=2)
        
        # Shuffle questions
        random.shuffle(self.questions)
    
    def create_widgets(self):
        """Create the main UI components."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="CS50 Quiz Game",
            font=("Arial", 24, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.title_label.pack(pady=(0, 30))
        
        # Score and timer frame
        self.info_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.info_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.score_label = tk.Label(
            self.info_frame,
            text="Score: 0",
            font=("Arial", 16),
            fg='#27ae60',
            bg='#2c3e50'
        )
        self.score_label.pack(side=tk.LEFT)
        
        self.timer_label = tk.Label(
            self.info_frame,
            text="Time: 30",
            font=("Arial", 16),
            fg='#e74c3c',
            bg='#2c3e50'
        )
        self.timer_label.pack(side=tk.RIGHT)
        
        # Question frame
        self.question_frame = tk.Frame(self.main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 18),
            fg='#ecf0f1',
            bg='#34495e',
            wraplength=700,
            justify=tk.CENTER
        )
        self.question_label.pack(pady=30)
        
        # Answer buttons frame
        self.answers_frame = tk.Frame(self.question_frame, bg='#34495e')
        self.answers_frame.pack(pady=(0, 30))
        
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.answers_frame,
                text="",
                font=("Arial", 14),
                width=50,
                height=2,
                command=lambda x=i: self.answer_selected(x),
                bg='#3498db',
                fg='white',
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(pady=5)
            self.answer_buttons.append(btn)
        
        # Control buttons
        self.control_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.control_frame.pack(fill=tk.X)
        
        self.next_button = tk.Button(
            self.control_frame,
            text="Next Question",
            font=("Arial", 14),
            command=self.next_question,
            bg='#27ae60',
            fg='white',
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.restart_button = tk.Button(
            self.control_frame,
            text="Restart Game",
            font=("Arial", 14),
            command=self.restart_game,
            bg='#e67e22',
            fg='white'
        )
        self.restart_button.pack(side=tk.LEFT)
    
    def start_game(self):
        """Start or restart the game."""
        self.current_question = 0
        self.score = 0
        self.update_score()
        self.show_question()
        self.start_timer()
    
    def show_question(self):
        """Display the current question and answers."""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}: {q['question']}")
            
            for i, option in enumerate(q['options']):
                self.answer_buttons[i].config(
                    text=f"{chr(65 + i)}. {option}",
                    state=tk.NORMAL,
                    bg='#3498db'
                )
            
            self.next_button.config(state=tk.DISABLED)
            self.reset_timer()
        else:
            self.end_game()
    
    def answer_selected(self, selected):
        """Handle answer selection."""
        self.timer_running = False
        
        q = self.questions[self.current_question]
        correct = q['correct']
        
        # Color the buttons
        for i, btn in enumerate(self.answer_buttons):
            btn.config(state=tk.DISABLED)
            if i == correct:
                btn.config(bg='#27ae60')  # Green for correct
            elif i == selected and i != correct:
                btn.config(bg='#e74c3c')  # Red for wrong selection
        
        # Update score
        if selected == correct:
            self.score += 10
            self.update_score()
        
        self.next_button.config(state=tk.NORMAL)
    
    def next_question(self):
        """Move to the next question."""
        self.current_question += 1
        self.show_question()
        self.start_timer()
    
    def start_timer(self):
        """Start the question timer."""
        self.timer_running = True
        self.update_timer()
    
    def reset_timer(self):
        """Reset timer for new question."""
        self.time_left = 30
        self.timer_label.config(text=f"Time: {self.time_left}")
    
    def update_timer(self):
        """Update the countdown timer."""
        if self.timer_running and self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running and self.time_left <= 0:
            # Time's up - auto select wrong answer
            self.answer_selected(-1)  # No answer selected
    
    def update_score(self):
        """Update the score display."""
        self.score_label.config(text=f"Score: {self.score}")
    
    def end_game(self):
        """End the game and show results."""
        total_questions = len(self.questions)
        percentage = (self.score // 10) / total_questions * 100
        
        result_text = f"Game Over!\n\n"
        result_text += f"Final Score: {self.score}\n"
        result_text += f"Questions Answered: {self.score // 10}/{total_questions}\n"
        result_text += f"Percentage: {percentage:.1f}%\n\n"
        
        if percentage >= 80:
            result_text += "Excellent work! 🎉"
        elif percentage >= 60:
            result_text += "Good job! 👍"
        elif percentage >= 40:
            result_text += "Not bad, keep practicing! 📚"
        else:
            result_text += "Keep studying! 💪"
        
        messagebox.showinfo("Quiz Complete", result_text)
        
        # Save high score
        self.save_high_score()
    
    def save_high_score(self):
        """Save high score to file."""
        try:
            with open('high_scores.txt', 'r') as f:
                high_score = int(f.read().strip())
        except FileNotFoundError:
            high_score = 0
        
        if self.score > high_score:
            with open('high_scores.txt', 'w') as f:
                f.write(str(self.score))
            messagebox.showinfo("New High Score!", f"Congratulations! New high score: {self.score}")
    
    def restart_game(self):
        """Restart the game with shuffled questions."""
        self.timer_running = False
        random.shuffle(self.questions)
        self.start_game()

def main():
    """Main function to run the quiz game."""
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Usage:
# 1. Save as quiz_game.py
# 2. python quiz_game.py
# 3. Questions are loaded from questions.json (created automatically)
