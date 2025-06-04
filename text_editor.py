from tkinter.colorchooser import askcolor

import tkinter as tk
from tkinter import filedialog

# Create main window
root = tk.Tk()
root.title("Smart Text Editor")
root.geometry("800x600")

# Text area
text_area = tk.Text(root, font=("Arial", 14))
text_area.grid(row=1, column=0, sticky="nsew")

# Function to change font size
def change_font_size(*args):
    size = int(font_size_var.get())
    text_area.config(font=("Arial", size))  # Change font size without affecting the toolbar
    
# Functions
def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

    

def update_status(event=None):
    text_content = text_area.get(1.0, tk.END)
    words = len(text_content.split())
    characters = len(text_content.replace(" ", "").replace("\n", ""))
    status_bar.config(text=f"Words: {words} | Characters: {characters}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))

# Now the Menu Bar can safely use these
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)


    
# Toolbar Frame
toolbar = tk.Frame(root)
toolbar.grid(row=0, column=0, sticky="ew")


# Font Size Option
font_size_var = tk.StringVar(value="14")  # Default size

font_size_dropdown = tk.OptionMenu(toolbar, font_size_var, "10", "12", "14", "16", "18", "20", "24", "28", "32")
font_size_dropdown.pack(side='left', padx=5, pady=5)
font_size_var.trace("w", change_font_size)

# Font Family Option
font_family_var = tk.StringVar(value="Arial")
font_family_dropdown = tk.OptionMenu(toolbar, font_family_var, "Arial", "Times New Roman", "Courier", "Helvetica")
font_family_dropdown.pack(side='left', padx=5, pady=5)

# Function to change font family
def change_font_size(*args):
    size = int(font_size_var.get())
    family = font_family_var.get()
    text_area.config(font=(family, size))

font_size_var.trace("w", change_font_size)




# Status Bar
status_bar = tk.Label(root, text="Words: 0 | Characters: 0", anchor='w')
status_bar.grid(row=2, column=0, sticky="ew")

# Function to set bold
def set_bold():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "bold" in current_tags:
            text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            text_area.tag_add("bold", "sel.first", "sel.last")
            text_area.tag_configure("bold", font=(font_family_var.get(), int(font_size_var.get()), "bold"))

    except tk.TclError:
        messagebox.showwarning("No Text Selected", "Please select text to bold.")

# Function to set italic
def set_italic():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "italic" in current_tags:
            text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            text_area.tag_add("italic", "sel.first", "sel.last")
            text_area.tag_configure("italic", font=(font_family_var.get(), int(font_size_var.get()), "italic"))
    except tk.TclError:
        messagebox.showwarning("No Text Selected", "Please select text to italicize.")

# Function to set underline
def set_underline():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "underline" in current_tags:
            text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            text_area.tag_add("underline", "sel.first", "sel.last")
            text_area.tag_configure("underline", font=(font_family_var.get(), int(font_size_var.get()), "underline"))
    except tk.TclError:
        messagebox.showwarning("No Text Selected", "Please select text to underline.")

# Function to change the text color
def change_text_color():
    color = askcolor()[1]  # askcolor returns a tuple (rgb, hex)
    if color:
        try:
            text_area.tag_add("colored", "sel.first", "sel.last")
            text_area.tag_configure("colored", foreground=color)  # Change text color
        except tk.TclError:
            messagebox.showwarning("No Text Selected", "Please select text to color.")


# Bold Button
bold_btn = tk.Button(toolbar, text="Bold", command=set_bold)
bold_btn.pack(side='left', padx=5, pady=5)

# Italic Button
italic_btn = tk.Button(toolbar, text="Italic", command=set_italic)
italic_btn.pack(side='left', padx=5, pady=5)

# Underline Button
underline_btn = tk.Button(toolbar, text="Underline", command=set_underline)
underline_btn.pack(side='left', padx=5, pady=5)

# Text Color Button
color_btn = tk.Button(toolbar, text="Text Color", command=change_text_color)
color_btn.pack(side='left', padx=5, pady=5)

def clear_formatting():
    try:
        text_area.tag_remove("bold", "sel.first", "sel.last")
        text_area.tag_remove("italic", "sel.first", "sel.last")
        text_area.tag_remove("underline", "sel.first", "sel.last")
        text_area.tag_remove("colored", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showwarning("No Text Selected", "Please select text to clear formatting.")

# Clear Formatting Button
clear_btn = tk.Button(toolbar, text="Clear Formatting", command=clear_formatting)
clear_btn.pack(side='left', padx=5, pady=5)

def change_bg_color():
    color = askcolor()[1]
    if color:
        text_area.config(bg=color)

# Background Color Button
bg_color_btn = tk.Button(toolbar, text="Background", command=change_bg_color)
bg_color_btn.pack(side='left', padx=5, pady=5)

def toggle_word_wrap():
    current_wrap = text_area.cget("wrap")
    if current_wrap == "word":
        text_area.config(wrap="none")
        word_wrap_btn.config(relief="raised")
    else:
        text_area.config(wrap="word")
        word_wrap_btn.config(relief="sunken")

word_wrap_btn = tk.Button(toolbar, text="Word Wrap", command=toggle_word_wrap, relief="sunken")
word_wrap_btn.pack(side='left', padx=5, pady=5)



text_area.bind("<KeyRelease>", update_status)

# Shortcut Keys
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())

# Run the application
root.mainloop()
