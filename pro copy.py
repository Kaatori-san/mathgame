import tkinter as tk
import random
import time
from pygame import mixer
from PIL import Image, ImageTk

OPERATORS = ["+", "-", "*", "/"]
TOTAL_PROBLEMS = 10
MAX_LIVES = 3

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rivas Game")
        self.center_window(600, 400)
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((600, 400), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        mixer.init()
        self.play_music()
        self.welcome_label = tk.Label(
            self.canvas,
            text="Welcome to the Rivas Game!\nYou only have 3 lives. Answer as many problems as possible!",
            font=("Arial", 14),
            justify="center",
            bg="lightblue",
        )
        self.canvas.create_window(300, 50, window=self.welcome_label)
        self.problem_label = tk.Label(
            self.canvas,
            text="Press Start to Begin",
            font=("Arial", 18),
            bg="lightblue",
        )
        self.canvas.create_window(300, 150, window=self.problem_label)
        self.feedback_label = tk.Label(
            self.canvas,
            text="",
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(300, 200, window=self.feedback_label)
        self.start_button = tk.Button(
            self.canvas,
            text="Start",
            command=self.start_game,
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(300, 250, window=self.start_button)
        self.next_button = tk.Button(
            self.canvas,
            text="Next",
            command=self.next_problem,
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(300, 300, window=self.next_button)
        self.next_button.config(state=tk.DISABLED)
        self.retry_button = tk.Button(
            self.canvas,
            text="Retry",
            command=self.restart_game,
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(300, 350, window=self.retry_button)
        self.retry_button.pack_forget()
        self.score_label = tk.Label(
            self.canvas,
            text="",
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(300, 380, window=self.score_label)
        self.lives = MAX_LIVES
        self.hearts = ["❤️"] * self.lives
        self.lives_label = tk.Label(
            self.canvas,
            text="".join(self.hearts),
            font=("Arial", 14),
            bg="lightblue",
        )
        self.canvas.create_window(500, 50, window=self.lives_label)
        self.options_frame = tk.Frame(self.canvas, bg="lightblue")
        self.canvas.create_window(300, 250, window=self.options_frame)
        self.option_buttons = []
        for i in range(3):
            button = tk.Button(
                self.options_frame,
                text="",
                font=("Arial", 14),
                width=10,
                command=lambda i=i: self.check_answer(i),
                bg="lightblue",
            )
            button.grid(row=0, column=i, padx=5)
            button.grid_remove()
            self.option_buttons.append(button)
        self.wrong_ans = 0
        self.right_ans = 0
        self.current_problem = ""
        self.answer = 0
        self.problem_count = 0
        self.start_time = 0

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")
        self.root.update_idletasks()

    def play_music(self):
        try:
            mixer.music.load("bg_music.mp3")
            mixer.music.play(-1)
        except Exception as e:
            print(f"Error loading music: {e}")

    def play_click_sound(self):
        try:
            click_sound = mixer.Sound("click_sound.mp3")
            click_sound.play()
        except Exception as e:
            print(f"Error loading click sound: {e}")

    def screen_shake(self):
        x_pos = self.root.winfo_x()
        y_pos = self.root.winfo_y()
        for _ in range(5):
            self.root.geometry(f"+{x_pos + 10}+{y_pos}")
            self.root.update()
            time.sleep(0.02)
            self.root.geometry(f"+{x_pos - 10}+{y_pos}")
            self.root.update()
            time.sleep(0.02)
        self.root.geometry(f"+{x_pos}+{y_pos}")

    def generate_problem(self):
        operator = random.choice(OPERATORS)
        if operator in ["+", "-"]:
            left = random.randint(2, 99)
            right = random.randint(2, 99)
        elif operator == "*":
            left = random.randint(2, 15)
            right = random.randint(2, 15)
        else:
            left = random.randint(2, 100)
            right = random.randint(2, 50)
            while left % right != 0 or left < right:
                left = random.randint(2, 100)
                right = random.randint(2, 50)
        expr = f"{left} {operator} {right}"
        answer = eval(expr)
        if answer == int(answer):
            answer = int(answer)
        else:
            answer = round(answer, 2)
        return expr, answer

    def start_game(self):
        self.problem_count = 0
        self.wrong_ans = 0
        self.right_ans = 0
        self.lives = MAX_LIVES
        self.hearts = ["❤️"] * self.lives
        self.lives_label.config(text="".join(self.hearts))
        self.start_time = time.time()
        self.start_button.pack_forget()
        self.welcome_label.pack_forget()
        self.retry_button.pack_forget()
        self.next_button.pack()
        self.next_button.config(state=tk.DISABLED)
        self.next_problem()

    def next_problem(self):
        if self.problem_count < TOTAL_PROBLEMS and self.lives > 0:
            self.next_button.config(state=tk.DISABLED)
            self.current_problem, self.answer = self.generate_problem()
            self.problem_label.config(text=f"Problem {self.problem_count + 1}: {self.current_problem} = ?")
            self.feedback_label.config(text="")
            self.problem_count += 1
            self.generate_choices()
        else:
            self.end_game()

    def generate_choices(self):
        correct_answer = self.answer
        wrong_answers = set()
        while len(wrong_answers) < 2:
            wrong_ans = correct_answer + random.randint(-10, 10)
            if wrong_ans != correct_answer and wrong_ans > 0:
                wrong_answers.add(wrong_ans)
        choices = list(wrong_answers) + [correct_answer]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            self.option_buttons[i].config(text=str(choice), state=tk.NORMAL)
            self.option_buttons[i].grid()

    def check_answer(self, index):
        self.play_click_sound()
        user_answer = self.option_buttons[index].cget("text")
        try:
            if "." in user_answer:
                user_answer = float(user_answer)
            else:
                user_answer = int(user_answer)
        except ValueError:
            self.feedback_label.config(text="Invalid input!", fg="red")
            return
        if user_answer == self.answer:
            self.right_ans += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.wrong_ans += 1
            self.lives -= 1
            self.remove_heart()
            self.feedback_label.config(text=f"Wrong! Answer: {self.answer}", fg="red")
            self.next_button.config(state=tk.NORMAL)
            self.screen_shake()
            if self.lives == 0:
                self.end_game()
                return
        self.disable_buttons()
        self.next_button.config(state=tk.NORMAL)

    def remove_heart(self):
        if self.lives >= 0:
            self.hearts.pop()
            self.lives_label.config(text="".join(self.hearts))

    def disable_buttons(self):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
            button.grid_remove()

    def end_game(self):
        end_time = time.time()
        total_time = round(end_time - self.start_time, 2)
        self.problem_label.config(text="Game Over!")
        self.score_label.config(
            text=f"Score: {self.right_ans} right, {self.wrong_ans} wrong. Time: {total_time} seconds."
        )
        self.disable_buttons()
        self.next_button.pack_forget()
        self.retry_button.pack(pady=5)

    def restart_game(self):
        self.retry_button.pack_forget()
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()