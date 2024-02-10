from tkinter import *
from tkinter import messagebox
from pygame import mixer
from gtts import gTTS
import pandas
import random
import os

# Constants
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_WINDOW_BG_COLOR = "#B1DDC6"
WORD_FONT = ("Ariel", 60, "bold")
LANGUAGE_FONT = ("Ariel", 40, "italic")
SELECT_LANGUAGE_FONT = ("Ariel", 20, "italic")
FLIP_TIME = 2500  # Milliseconds
BACK_FONT_COLOR = "white"
FRONT_FONT_COLOR = "black"

back_language = "Español"
back_language_code = "es"
back_language_accent = "es"
front_language = "English"
front_language_code = "en"
front_language_accent = "com"

# File Paths:
initial_data_path = "data/English_data.csv"
ITALIANO_TO_LEARN = "data/Italiano_to_learn.csv"
ENGLISH_TO_LEARN = "data/English_to_learn.csv"
updated_data_path = "data/English_to_learn.csv"

USA_FLAG = "images/flag_usa.png"
SPAIN_FLAG = "images/flag_spain.png"
ITALY_FLAG = "images/flag_italy.png"
FRANCE_FLAG = "images/flag_france.png"
BRAZIL_FLAG = "images/flag_brazil.png"

front_country_name = "USA"
back_country_name = "SPAIN"

# Messages:
SELECT_LANGUAGE_TEXT = "Por favor seleccione el idioma\nque desea practicar:"
NO_MORE_CARDS_MESSAGE = ("¡Ha memorizado todas las cartas en este set!\nLa aplicación se cerrará y su progreso se"
                         " reiniciará cuando salga de esta ventana.")
CONTINUE_MESSAGE = "¿Desea continuar con su progreso guardado?"
CONFIRM_RESET_MESSAGE = "Esta acción borrará todo su progreso. ¿Está seguro de que desea continuar?"
CONFIRM_EXIT_MESSAGE = "¿Está seguro de que desea cerrar la aplicación?"

current_card = {}  # Current Card Dictionary

# Starting Audio
mixer.init()
text_to_speech = gTTS(text="Welcome", lang="en", tld="us")
text_to_speech.save("output.mp3")


def english_to_spanish():
    change_language(target_language="English", target_language_code="en", target_country_name="USA", accent="us",
                    target_country_flag_photoimage=usa_flag_photoimage, word_translated="Word",
                    pronunciation_translated="pronunciation", back_country_flag_photoimage=spain_flag_photoimage)


def italian_to_spanish():
    change_language(target_language="Italiano", target_language_code="it", target_country_name="ITALY",
                    target_country_flag_photoimage=italy_flag_photoimage, word_translated="Parola",
                    pronunciation_translated="pronuncia", back_country_flag_photoimage=spain_flag_photoimage)


def french_to_spanish():
    change_language(target_language="Français", target_language_code="fr", target_country_name="FRANCE",
                    target_country_flag_photoimage=france_flag_photoimage, word_translated="Mot",
                    pronunciation_translated="prononciation", back_country_flag_photoimage=spain_flag_photoimage)


def portuguese_to_spanish():
    change_language(target_language="Português", target_language_code="pt", target_country_name="BRAZIL",
                    accent="com.br", target_country_flag_photoimage=brazil_flag_photoimage, word_translated="Palavra",
                    pronunciation_translated="pronúncia", back_country_flag_photoimage=spain_flag_photoimage)


def change_language(target_language, target_language_code, target_country_name, target_country_flag_photoimage,
                    word_translated, pronunciation_translated, back_country_flag_photoimage, accent="com",
                    translation_language="Español", translation_language_code="es", translation_country_name="SPAIN"):

    global front_language, front_language_code, front_country_name, back_language, back_language_code
    global back_country_name, initial_data_path, updated_data_path, front_card_flag, back_card_flag
    global spain_flag_photoimage, front_language_accent
    front_language = target_language.capitalize()
    front_language_code = target_language_code
    front_language_accent = accent
    front_country_name = target_country_name.upper()
    initial_data_path = f"data/{front_language}_data.csv"
    front_card_flag = target_country_flag_photoimage

    back_language = translation_language.capitalize()
    back_language_code = translation_language_code
    back_country_name = translation_country_name.upper()
    back_card_flag = back_country_flag_photoimage

    canvas.itemconfig(flag, image=target_country_flag_photoimage)
    canvas.itemconfig(language, text=front_language)
    canvas.itemconfig(word, text=word_translated.capitalize())
    canvas.itemconfig(pronunciation, text=f"/{pronunciation_translated.lower()}/")

    updated_data_path = f"data/{front_language}_to_learn.csv"

    root.deiconify()  # Show root window
    language_window.destroy()  # Close language selection window
    ask_user_continue()
    next_card()


def flip_card():
    """Flip the card and shows the translation passed as input"""
    global text_to_speech
    try:
        canvas.itemconfig(word, fill=BACK_FONT_COLOR, text=current_card[back_language])
    except KeyError:
        pass
    else:
        canvas.itemconfig(language, fill=BACK_FONT_COLOR, text=back_language)
        canvas.itemconfig(pronunciation, text="")
        canvas.itemconfig(card, image=card_back)
        canvas.itemconfig(flag, image=back_card_flag)
        canvas.itemconfig(score, fill=BACK_FONT_COLOR)
        text_to_speech.text = current_card[back_language]
        text_to_speech.lang = back_language_code
        text_to_speech.tld = back_language_accent
        text_to_speech.save("output.mp3")
        audio = mixer.Sound("output.mp3")
        audio.play()


def next_card():
    """Generates and shows a new card, then calls the flip_card function after a given time"""
    global current_card, flip_timer, data, to_learn, text_to_speech, front_language_code
    root.after_cancel(flip_timer)  # Cancel the previous timer
    try:
        updated_data = pandas.read_csv(updated_data_path)
        words_to_learn = updated_data.to_dict(orient="records")
        canvas.itemconfig(score, text=f"{len(to_learn) - len(words_to_learn) + 1} / {len(to_learn) + 1}",
                          fill=FRONT_FONT_COLOR)
        if len(words_to_learn) < 2:
            well_done = messagebox.showinfo(message=NO_MORE_CARDS_MESSAGE,
                                            title="🎉🏆¡Buen trabajo! 🏆🎉")
            if well_done:
                no_more_cards()
                return
        else:
            current_card = random.choice(words_to_learn)
    except FileNotFoundError:
        data = pandas.read_csv(initial_data_path)
        to_learn = data.to_dict(orient="records")
        canvas.itemconfig(score, text=f"0 / {len(to_learn)}", fill=FRONT_FONT_COLOR)
        current_card = random.choice(to_learn)
    finally:
        canvas.itemconfig(word, fill=FRONT_FONT_COLOR, text=current_card[front_language])
        canvas.itemconfig(pronunciation, fill=FRONT_FONT_COLOR, text=f"/{current_card['IPA']}/")
        canvas.itemconfig(language, fill=FRONT_FONT_COLOR, text=front_language)
        canvas.itemconfig(card, image=card_front)
        canvas.itemconfig(flag, image=front_card_flag)

        mixer.init()
        text_to_speech.text = current_card[front_language]
        text_to_speech.lang = front_language_code
        text_to_speech.tld = front_language_accent
        text_to_speech.save("output.mp3")
        audio = mixer.Sound("output.mp3")
        audio.play()
        flip_timer = root.after(FLIP_TIME, func=flip_card)


def remove_known_word():
    """Remove words that user marks as known from the words_to_learn file"""
    try:
        updated_data = pandas.read_csv(updated_data_path)
        words_to_learn = updated_data.to_dict(orient="records")
        words_to_learn.remove(current_card)
        words_to_learn = pandas.DataFrame(words_to_learn)
        words_to_learn.to_csv(updated_data_path, mode="w", index=False)
    except FileNotFoundError:
        to_learn.remove(current_card)
        words_to_learn = pandas.DataFrame(to_learn)
        words_to_learn.to_csv(updated_data_path, index=False)
    finally:
        next_card()


def reset_data():
    """"Reset the data to the original (full) data set"""
    try:
        os.remove(updated_data_path)
    except FileNotFoundError:
        pass


def no_more_cards():
    """Reset the data and close window (called when there is only 1 card left)"""
    reset_data()
    root.destroy()


def ask_user_continue():
    """Ask the user if they want to continue from the progress of the last session"""
    if os.path.exists(updated_data_path):
        reset = messagebox.askyesno(title="¿Continuar?",
                                    message=CONTINUE_MESSAGE)
        if not reset:
            confirm_reset = messagebox.askokcancel(title="¿Está seguro?", icon="warning",
                                                   message=CONFIRM_RESET_MESSAGE)
            if confirm_reset:
                reset_data()


def on_closing():
    """"Ask the user if they actually meant to close the app"""
    confirm_exit = messagebox.askokcancel(title="Confirmar Cierre", icon="warning",
                                          message=CONFIRM_EXIT_MESSAGE)
    if confirm_exit:
        root.destroy()


# Read data and convert into a dictionary
data = pandas.read_csv(initial_data_path)
to_learn = data.to_dict(orient="records")

# ---------------------- UI Setup ----------------------------- #
root = Tk()
root.title("Flashcard App")
root.config(bg=BACKGROUND_COLOR, padx=40, pady=50)
root.geometry("+300+50")
flip_timer = root.after(FLIP_TIME, func=flip_card)  # Flip timer

# Images
icon = PhotoImage(file="images/icon_png.png")
root.iconphoto(False, icon)
card_front = PhotoImage(file="images/card_front.png")  # Cards
card_back = PhotoImage(file="images/card_back.png")

right_img = PhotoImage(file="images/right.png")  # Right - Wrong Buttons
wrong_img = PhotoImage(file="images/wrong.png")

usa_flag_photoimage = PhotoImage(file=USA_FLAG)  # Flags
italy_flag_photoimage = PhotoImage(file=ITALY_FLAG)
spain_flag_photoimage = PhotoImage(file=SPAIN_FLAG)
france_flag_photoimage = PhotoImage(file=FRANCE_FLAG)
brazil_flag_photoimage = PhotoImage(file=BRAZIL_FLAG)
front_card_flag = usa_flag_photoimage
back_card_flag = spain_flag_photoimage

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=card_front)  # Card Img
word = canvas.create_text(400, 263, text="Word", fill="black", font=WORD_FONT)  # Word Text
language = canvas.create_text(400, 150, text=front_language, font=LANGUAGE_FONT)  # Language Text
pronunciation = canvas.create_text(400, 340, text="/pronunciation/", font=LANGUAGE_FONT)  # IPA Phonetic Transcription
flag = canvas.create_image(150, 100, image=front_card_flag)  # Flag Img
score = canvas.create_text(670, 60, text="", fill="black", font=SELECT_LANGUAGE_FONT)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons:
unknown_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_button = Button(image=right_img, highlightthickness=0, bd=0, command=remove_known_word)
known_button.grid(row=1, column=1)

# Bind the closing button to the function on_closing to ask the user if he wants to exit
root.protocol("WM_DELETE_WINDOW", on_closing)

# Hide the Root Window until the user chooses a language
root.withdraw()

# --------------------- Select Language Window -------------------------- #
language_window = Toplevel()
language_window.title("Select Language")
language_window.config(bg=LANGUAGE_WINDOW_BG_COLOR, padx=50, pady=50)
language_window.geometry("+420+100")
language_window.iconphoto(False, icon)

# Label: Select your language
select_language_label = Label(language_window, text=SELECT_LANGUAGE_TEXT, bg=LANGUAGE_WINDOW_BG_COLOR,
                              font=SELECT_LANGUAGE_FONT, fg=FRONT_FONT_COLOR)
select_language_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

english_button = Button(language_window, image=usa_flag_photoimage, bd=3, command=english_to_spanish)
english_button.grid(row=1, column=0, padx=20, pady=20)

italian_button = Button(language_window, image=italy_flag_photoimage, bd=3, command=italian_to_spanish)
italian_button.grid(row=1, column=1, padx=20, pady=20)

french_button = Button(language_window, image=france_flag_photoimage, bd=3, command=french_to_spanish)
french_button.grid(row=2, column=0, padx=20, pady=20)

portuguese_button = Button(language_window, image=brazil_flag_photoimage, bd=3, command=portuguese_to_spanish)
portuguese_button.grid(row=2, column=1, padx=20, pady=20)

language_window.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
