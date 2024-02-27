import json
from difflib import get_close_matches
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

# Loading data from json file
# in python dictionary
data = json.load(open("dictionary.json"))

def save_data():
    # Save the updated data back to the json file
    with open("dictionary.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

def add_word(word, meaning):
    # Add a new word to the dictionary
    data[word.lower()] = [meaning]
    messagebox.showinfo("Success", f"The word '{word}' has been added to the dictionary.")
    save_data()

def update_meaning(word, new_meaning):
    # Update the meaning of an existing word
    data[word.lower()] = [new_meaning]
    messagebox.showinfo("Success", f"The meaning of '{word}' has been updated.")
    save_data()

def delete_word(word):
    # Delete an existing word from the dictionary
    del data[word.lower()]
    messagebox.showinfo("Success", f"The word '{word}' has been deleted from the dictionary.")
    save_data()

def translate(w):
    # Convert to lower case
    w = w.lower()

    if w in data:
        return data[w]
    elif len(get_close_matches(w, data.keys())) > 0:
        yn = messagebox.askquestion("Did you mean?", f"Did you mean {get_close_matches(w, data.keys())[0]} instead?")
        if yn == "yes":
            return data[get_close_matches(w, data.keys())[0]]
        elif yn == "no":
            return "The word doesn't exist. Please double-check it."
        else:
            return "We didn't understand your entry."
    else:
        return "The word doesn't exist. Please double-check it."

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
        return None

def get_text_input():
    word = entry_word.get()
    return word

def get_input_method():
    method = input_var.get()
    return method

def on_translate():
    input_method = get_input_method()
    if input_method == 1:
        word = get_text_input()
    else:
        word = get_voice_input()
    if word:
        output = translate(word)
        if type(output) == list:
            messagebox.showinfo("Meaning", "\n".join(output))
        else:
            messagebox.showinfo("Meaning", output)

def on_add_word():
    input_method = get_input_method()
    if input_method == 1:
        word = get_text_input()
    else:
        word = get_voice_input()
    if word:
        meaning = entry_meaning.get()
        add_word(word, meaning)

def on_update_meaning():
    input_method = get_input_method()
    if input_method == 1:
        word = get_text_input()
    else:
        word = get_voice_input()
    if word:
        meaning = entry_meaning.get()
        update_meaning(word, meaning)

def on_delete_word():
    input_method = get_input_method()
    if input_method == 1:
        word = get_text_input()
    else:
        word = get_voice_input()
    if word:
        delete_word(word)

# Create GUI window
root = tk.Tk()
root.title("Dictionary Application")
root.geometry("600x400")  # Set window size

# Add background color
root.configure(bg="#C0C0C0")

# Create input method selection
input_var = tk.IntVar()
radio_button_text = [("Type the word", 1), ("Speak the word", 2)]
for text, val in radio_button_text:
    tk.Radiobutton(root, text=text, variable=input_var, value=val, bg="#f0f0f0").pack()

# Create entry for word
label_word = tk.Label(root, text="Enter the word:", bg="#f0f0f0")
label_word.pack()
entry_word = tk.Entry(root)
entry_word.pack()

# Create entry for meaning
label_meaning = tk.Label(root, text="Enter the meaning:", bg="#f0f0f0")
label_meaning.pack()
entry_meaning = tk.Entry(root)
entry_meaning.pack()

# Add colors to buttons
button_colors = ["#FF5733", "#FFBD33", "#33FF57", "#3366FF"]
buttons = []

# Create buttons for actions
button_translate = tk.Button(root, text="Translate", command=on_translate, bg=button_colors[0])
button_translate.pack()
buttons.append(button_translate)

button_add_word = tk.Button(root, text="Add Word", command=on_add_word, bg=button_colors[1])
button_add_word.pack()
buttons.append(button_add_word)

button_update_meaning = tk.Button(root, text="Update Meaning", command=on_update_meaning, bg=button_colors[2])
button_update_meaning.pack()
buttons.append(button_update_meaning)

button_delete_word = tk.Button(root, text="Delete Word", command=on_delete_word, bg=button_colors[3])
button_delete_word.pack()
buttons.append(button_delete_word)

# Run the GUI
root.mainloop()
