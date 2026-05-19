# ui/face_ui.py

import tkinter as tk
from tkinter import ttk
import threading
import math
import cv2
import os
from PIL import Image, ImageTk

from modules.voice import listen
from modules.assistant import ask_cJ


class FaceUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("cJ - Reactor UI")

        # -----------------------------
        # FULLSCREEN + RESIZABLE
        # -----------------------------
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.toggle_fullscreen())

        # -----------------------------
        # VIDEO PATH
        # -----------------------------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(BASE_DIR, "assets", "bg1.mp4")

        self.video = cv2.VideoCapture(video_path)

        # -----------------------------
        # CANVAS
        # -----------------------------
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.video_frame_id = None

        # Animation variables
        self.angle_main = 0
        self.angle_ring2 = 0
        self.angle_ring3 = 0

        self.ring_color = "skyblue"

        self.update_video()
        self.animate_ring()

        # -----------------------------
        # THREE DOT MENU BUTTON
        # -----------------------------
        self.menu_button = tk.Button(
            self,
            text="•••",
            font=("Arial", 18),
            fg="white",
            bg="black",
            bd=0,
            command=self.toggle_menu
        )
        self.menu_button.place(relx=0.5, rely=0.95, anchor="center")

        self.menu_frame = None

        # Start listening thread
        threading.Thread(target=self.listen_loop, daemon=True).start()

    # -----------------------------------
    # FULLSCREEN TOGGLE
    # -----------------------------------
    def toggle_fullscreen(self):
        current = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not current)


    # -----------------------------------
    # VIDEO BACKGROUND
    # -----------------------------------
    def update_video(self):
        ret, frame = self.video.read()

        if not ret:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.after(20, self.update_video)
            return

        width = self.winfo_width()
        height = self.winfo_height()

        frame = cv2.resize(frame, (width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        self.photo = ImageTk.PhotoImage(img)

        if self.video_frame_id is None:
             self.video_frame_id = self.canvas.create_image(
                 0, 0, anchor="nw", image=self.photo
            )
        else:
            self.canvas.itemconfig(self.video_frame_id, image=self.photo)

        self.after(20, self.update_video)



    # -----------------------------------
    # RING ANIMATION (3 LAYERS)
    # -----------------------------------
    def animate_ring(self):

        self.canvas.delete("ring")

        width = self.winfo_width()
        height = self.winfo_height()

        center_x = width // 2
        center_y = height // 2

        # -------- 1_Main Pulsing Ring --------
        base_radius = min(width, height) // 6
        pulse = 15 * math.sin(self.angle_main / 10)
        radius = base_radius + pulse

        self.canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=self.angle_main,
            extent=359,
            style="arc",
            width=5,
            outline="white",
            tags="ring"
        )

        # -------- 2_Main Pulsing Ring --------
        base_radius = min(width, height) // 6
        pulse = 15 * math.sin(self.angle_main / 10)
        radius4 = base_radius - pulse

        self.canvas.create_arc(
            center_x - radius4,
            center_y - radius4,
            center_x + radius4,
            center_y + radius4,
            start=self.angle_ring2,
            extent=359,
            style="arc",
            width=4,
            outline="skyblue",
            tags="ring"
        )

        # -------- Second Rotating Ring --------
        radius2 = base_radius + 40

        self.canvas.create_arc(
            center_x - radius2,
            center_y - radius2,
            center_x + radius2,
            center_y + radius2,
            start=self.angle_ring2,
            extent=300,
            style="arc",
            width=3,
            outline="skyblue",
            tags="ring"
        )

        # -------- Third Rotating Ring --------
        radius3 = base_radius - 40

        self.canvas.create_arc(
            center_x - radius3,
            center_y - radius3,
            center_x + radius3,
            center_y + radius3,
            start=self.angle_ring3,
            extent=250,
            style="arc",
            width=3,
            outline="skyblue",
            tags="ring"
        )

        # Rotate angles
        self.angle_main += 4
        self.angle_ring2 -= 3
        self.angle_ring3 += 5

        self.after(40, self.animate_ring)

    # -----------------------------
    # THREE DOT MENU
    # -----------------------------
    def toggle_menu(self):
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None
            return

        self.menu_frame = tk.Frame(self, bg="#111111")
        self.menu_frame.place(relx=0.5, rely=0.85, anchor="center")

        btn_style = {"fg": "white", "bg": "#222222", "bd": 0, "activebackground": "#333333", "activeforeground": "skyblue"}

        tk.Button(self.menu_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(self.menu_frame, text="Switch to Text UI", command=self.open_text_ui, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(self.menu_frame, text="Exit", command=self.destroy, **btn_style).pack(fill="x", padx=20, pady=5)


    # -----------------------------------
    # LISTEN LOOP
    # -----------------------------------
    def listen_loop(self):
        import time
        while True:
            time.sleep(0.5)

            # 🔥 Only listen if not speaking
            import modules.filter as filter_module
            if filter_module.is_speaking:
                 continue

            question = listen()

            if question:
                threading.Thread(
                    target=self.process_question,
                    args=(question,),
                    daemon=True
                ).start()



    def process_question(self, question):
        ask_cJ(question)

    def open_text_ui(self):
        from ui.text_ui import TextUI
        self.destroy()
        TextUI().mainloop()


if __name__ == "__main__":
    app = FaceUI()
    app.mainloop()
