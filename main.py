import requests
import tkinter as tk
from tkinter import messagebox
import html


# ---------------- API FUNCTION ----------------
def fetch_questions(difficulty):
    url = f"https://opentdb.com/api.php?amount=10&category=9&difficulty={difficulty}&type=multiple"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except Exception:
        messagebox.showerror("Error", "Unable to fetch questions. Check internet connection.")
        return None


# ---------------- GAME LOGIC ----------------
def start_quiz():
    global questions, question_index, score

    difficulty = difficulty_var.get()
    if not difficulty:
        messagebox.showwarning("Select Difficulty", "Please choose a difficulty level.")
        return

    questions = fetch_questions(difficulty)
    if not questions:
        return

    question_index = 0
    score = 0
    show_question()


def show_question():
    global current_correct_answer

    q = questions[question_index]

    question_text.set(f"Q{question_index + 1}: {html.unescape(q['question'])}")

    options = q["incorrect_answers"] + [q["correct_answer"]]
    import random
    random.shuffle(options)

    for i in range(4):
        option_buttons[i].config(text=html.unescape(options[i]))

    current_correct_answer = html.unescape(q["correct_answer"])
    score_label.config(text=f"Score: {score}")


def check_answer(selected):
    global question_index, score

    if selected == current_correct_answer:
        score += 1
        messagebox.showinfo("Correct!", "Nice job!")
    else:
        messagebox.showinfo("Wrong!", f"Correct answer was:\n{current_correct_answer}")

    question_index += 1

    if question_index < len(questions):
        show_question()
    else:
        messagebox.showinfo("Quiz Complete", f"Final Score: {score}/10")
        question_text.set("Quiz finished. Select difficulty and start again.")


# ---------------- UI SETUP ----------------
window = tk.Tk()
window.title("Trivia Quizzer")
window.config(padx=30, pady=30)

questions = []
question_index = 0
score = 0
current_correct_answer = ""


# Difficulty selection
difficulty_var = tk.StringVar()

tk.Label(text="Select Difficulty:", font=("Arial", 12)).pack()

tk.Radiobutton(text="Easy", variable=difficulty_var, value="easy").pack()
tk.Radiobutton(text="Medium", variable=difficulty_var, value="medium").pack()
tk.Radiobutton(text="Hard", variable=difficulty_var, value="hard").pack()


# Start button
tk.Button(text="Start Quiz", command=start_quiz).pack(pady=10)


# Question display
question_text = tk.StringVar()
question_label = tk.Label(textvariable=question_text, wraplength=400, font=("Arial", 14))
question_label.pack(pady=20)


# Answer buttons
option_buttons = []
for i in range(4):
    btn = tk.Button(width=30, command=lambda i=i: check_answer(option_buttons[i].cget("text")))
    btn.pack(pady=5)
    option_buttons.append(btn)


# Score display
score_label = tk.Label(text="Score: 0", font=("Arial", 12))
score_label.pack(pady=10)


window.mainloop()