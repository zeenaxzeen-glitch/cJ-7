# ui/text_ui.py

import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import os
from modules.assistant import ask_cJ


class TextUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("cJ - Neural Core Interface")
        self.geometry("1000x650")
        self.minsize(700, 450)
        self.configure(bg="black")

        # Fullscreen toggle
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        # ---------------- BACKGROUND ----------------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.bg_path = os.path.join(BASE_DIR, "assets", "background1.jpeg")

        self.canvas = tk.Canvas(self, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = None
        self.bg_photo = None
        self.bind("<Configure>", self.resize_background)

        # ------------- GLOW FRAME ----------------
        self.outer_frame = tk.Frame(self.canvas, bg="#00f7ff", bd=0)
        self.inner_frame = tk.Frame(self.outer_frame, bg="#0a0a0a", bd=0)

        self.chat_window = self.canvas.create_window(
            0, 0, anchor="nw", window=self.outer_frame
        )

        self.outer_frame.pack(fill="both", expand=True, padx=3, pady=3)
        self.inner_frame.pack(fill="both", expand=True)

        # ------------- CHAT DISPLAY --------------
        self.chat_display = scrolledtext.ScrolledText(
            self.inner_frame,
            state='disabled',
            wrap=tk.WORD,
            bg="#0a0a0a",
            fg="#00f7ff",
            insertbackground="#00f7ff",
            font=("Consolas", 13),
            bd=0,
            padx=20,
            pady=20
        )
        self.chat_display.pack(fill="both", expand=True)

        # ------------- STATUS BAR ----------------
        self.status = tk.Label(
            self,
            text="● ONLINE",
            fg="#00ff88",
            bg="black",
            font=("Consolas", 10)
        )
        self.status.pack(anchor="w", padx=20)

        # ------------- INPUT FIELD ----------------
        self.input_box = tk.Entry(
            self,
            font=("Consolas", 13),
            bg="#111111",
            fg="white",
            insertbackground="#00f7ff",
            bd=0
        )
        self.input_box.pack(fill="x", padx=20, pady=15)
        self.input_box.bind("<Return>", self.send_message)

        # Glow animation
        self.glow_state = 0
        self.animate_glow()

        self.update_layout()

    # -----------------------------------
    # FULLSCREEN
    # -----------------------------------
    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", True)

    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

    # -----------------------------------
    # BACKGROUND RESIZE
    # -----------------------------------
    def resize_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()

        if width < 10 or height < 10:
            return

        image = Image.open(self.bg_path)
        image = image.resize((width, height))
        self.bg_photo = ImageTk.PhotoImage(image)

        if self.bg_image is None:
            self.bg_image = self.canvas.create_image(
                0, 0, anchor="nw", image=self.bg_photo
            )
        else:
            self.canvas.itemconfig(self.bg_image, image=self.bg_photo)

        self.canvas.lower(self.bg_image)
        self.update_layout()

    # -----------------------------------
    # LAYOUT UPDATE
    # -----------------------------------
    def update_layout(self):
        width = self.winfo_width()
        height = self.winfo_height()

        self.canvas.coords(self.chat_window, 20, 20)
        self.canvas.itemconfig(
            self.chat_window,
            width=width - 40,
            height=height - 150
        )

    # -----------------------------------
    # GLOW ANIMATION
    # -----------------------------------
    def animate_glow(self):
        colors = ["#00f7ff", "#00c3ff", "#0088ff"]
        self.outer_frame.config(bg=colors[self.glow_state])
        self.glow_state = (self.glow_state + 1) % len(colors)
        self.after(300, self.animate_glow)

    # -----------------------------------
    # SEND MESSAGE
    # -----------------------------------
    def send_message(self, event=None):
        question = self.input_box.get().strip()

        if question:
            self.display_message("YOU", question)
            self.input_box.delete(0, tk.END)
            self.status.config(text="● THINKING...", fg="#ffaa00")

            threading.Thread(
                target=self.process_message,
                args=(question,),
                daemon=True
            ).start()

    # -----------------------------------
    # AI PROCESSING
    # -----------------------------------
    def process_message(self, question):
        answer = ask_cJ(question)
        if answer:
            self.after(0, lambda: self.type_writer_effect(answer))


    # -----------------------------------
    # TYPEWRITER EFFECT
    # -----------------------------------
    def type_writer_effect(self, text, index=0):
        if index == 0:
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, "\ncJ ⚡ ")
            self.chat_display.config(state='disabled')

        if index < len(text):
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, text[index])
            self.chat_display.config(state='disabled')
            self.chat_display.see(tk.END)
            self.after(15, lambda: self.type_writer_effect(text, index + 1))
        else:
            self.status.config(text="● ONLINE", fg="#00ff88")

    # -----------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------
    def display_message(self, sender, message):
        self.chat_display.config(state='normal')

        if sender == "YOU":
            self.chat_display.insert(
                tk.END,
                f"\nYOU ➜ {message}\n",
                "user"
            )

        self.chat_display.tag_config("user", foreground="#00ffcc")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')


if __name__ == "__main__":
    app = TextUI()
    app.mainloop()
