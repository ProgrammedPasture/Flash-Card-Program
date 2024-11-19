from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
learn_words = {}
score = 0
streak = 0

try:
    data = pandas.read_csv("learn_words.csv")
    learn_words = data.to_dict(orient="records")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    learn_words = original_data.to_dict(orient="records")


# ---------------------------- Save Progress ------------------------------- #

def is_known():
    """Called when the user marks a word as 'known'."""
    global score, streak
    learn_words.remove(current_card)
    pandas.DataFrame(learn_words).to_csv("learn_words.csv", index=False)

    score += 10  # Increment score for a correct answer
    streak += 1  # Increment streak
    update_status()
    next_card()


def is_unknown():
    """Called when the user marks a word as 'unknown'."""
    global streak
    streak = 0  # Reset streak on an incorrect answer
    update_status()
    next_card()


# ---------------------------- Flip Card ------------------------------- #

def flip_card():
    """Flips the card to show the English translation."""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


# ---------------------------- Pick Word ------------------------------- #

def next_card():
    """Picks the next word for the flashcard."""
    global current_card, flip_timer
    if not learn_words:
        canvas.itemconfig(card_title, text="Game Over!", fill="black")
        canvas.itemconfig(card_word, text=f"Final Score: {score}", fill="black")
        return

    window.after_cancel(flip_timer)
    current_card = random.choice(learn_words)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, flip_card)


# ---------------------------- Update UI ------------------------------- #

def update_status():
    """Updates the score and streak on the screen."""
    score_label.config(text=f"Score: {score}")
    streak_label.config(text=f"Streak: {streak}")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card Language Program")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, next_card)

# Main Canvas Window
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="card_front.png")
card_back_image = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Times New Roman", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Times New Roman", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
check_image = PhotoImage(file="right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=0)

x_image = PhotoImage(file="wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=is_unknown)
x_button.grid(column=1, row=1)

# Score and Streak Labels
score_label = Label(text=f"Score: {score}", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR)
score_label.grid(row=2, column=0)

streak_label = Label(text=f"Streak: {streak}", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR)
streak_label.grid(row=2, column=1)

next_card()

window.mainloop()