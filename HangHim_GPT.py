import tkinter as tk
import random
from tkinter import messagebox

class HangmanGame:  # Translated class name
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")  # Translated window title
        self.root.configure(bg="#0000AA")
        
        self.max_attempts = 7
        self.attempts = 0
        self.word_list = ["python", "computer", "keyboard", "programming", "challenge"]
        self.secret_word = self.select_random_word()
        self.guesses = []
        self.used_letters = []

        self.word_display = tk.StringVar()
        self.word_display.set("_ " * len(self.secret_word))

        self.init_ui()

    def select_random_word(self):
        return random.choice(self.word_list)

    def init_ui(self):
        self.word_label = tk.Label(self.root, textvariable=self.word_display, font=("Arial", 16), bg="#0000AA", fg="#FFFFFF")
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 16))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.make_guess) 

        self.guess_button = tk.Button(self.root, text="Guess", command=self.make_guess, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.guess_button.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.restart_button.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Attempts remaining: {self.max_attempts}", font=("Arial", 12), bg="#0000AA", fg="#FFFFFF")
        self.attempts_label.pack(pady=10)

        self.used_letters_label = tk.Label(self.root, text="Used letters: ", font=("Arial", 12), bg="#0000AA", fg="#FFFFFF")
        self.used_letters_label.pack(pady=10)

        self.image_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#0000AA", fg="#FFFFFF")
        self.image_label.pack(pady=10)

        self.update_image()

    def make_guess(self,e=None):
        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", "You have exhausted all your attempts. The word was: " + self.secret_word)
            return
        
        guess = self.entry.get().lower()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Input Error", "Please enter a single valid letter.")
            return

        if guess in self.used_letters:
            messagebox.showwarning("Letter Already Used", "You have already used this letter.")
        else:
            self.used_letters.append(guess)

            if guess in self.secret_word:
                self.update_word_display()
                if self.word_display.get() == self.secret_word.replace("", " ").strip():
                    messagebox.showinfo("Victory", "You guessed the word! You won!")
            else:
                self.attempts += 1
                self.attempts_label.config(text=f"Attempts remaining: {self.max_attempts - self.attempts}")
                self.update_image()
        
        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", "You have exhausted all your attempts. The word was: " + self.secret_word)
            self.restart_game()

        self.entry.delete(0, tk.END)
        self.update_used_letters()

    def update_word_display(self):
        word = ""
        for letter in self.secret_word:
            if letter in self.used_letters:
                word += letter + " "
            else:
                word += "_ "
        self.word_display.set(word)

    def update_image(self):
        # ASCII representation of the hangman
        hangman = [
            "  _________     ",
            "  |       |     ",
            f"  |       {' O ' if self.attempts >= 1 else ' '}     ",
            f"  |      {'*-|-*' if self.attempts >= 2 else ' '}    ",
            f"  |      {',-|-,' if self.attempts >= 3 else ' '}    ",
            " _|___           ",
            "|     |__________"
        ]

        # Update the hangman image based on the number of errors (self.attempts)
        image = "\n".join(hangman[:self.attempts + 1])
        self.image_label.config(text=image)

    def update_used_letters(self):
        used_letters_text = "Used letters: " + ", ".join(self.used_letters)
        self.used_letters_label.config(text=used_letters_text)

    def restart_game(self):
        self.attempts = 0
        self.guesses = []
        self.used_letters = []
        self.secret_word = self.select_random_word()
        self.word_display.set("_ " * len(self.secret_word))
        self.attempts_label.config(text=f"Attempts remaining: {self.max_attempts}")
        self.used_letters_label.config(text="Used letters: ")
        self.image_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
