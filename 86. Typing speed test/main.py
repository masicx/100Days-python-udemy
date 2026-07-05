"""
Typing Speed Test - Desktop GUI application
--------------------------------------------
Shows the user a sample paragraph, times how long they take to type it,
and reports words-per-minute (WPM) and accuracy, with live character-by-
character highlighting as they type.

Standard library only - no extra installs needed.

Run with:
    python typing_speed_test.py
"""

import random
import time
import tkinter as tk
from tkinter import ttk


SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog while the sun sets "
    "slowly behind the distant mountains.",

    "Practice makes perfect, and the only way to type faster is to "
    "keep your fingers moving across the keyboard every single day.",

    "Python is a versatile programming language used for web "
    "development, data science, automation, and building desktop apps.",

    "A journey of a thousand miles begins with a single step, and "
    "every expert typist was once a beginner who kept practicing.",

    "Reading a little every day and typing a little every day will "
    "improve both your vocabulary and your speed behind the keyboard.",

    "The early bird catches the worm, but the second mouse gets the "
    "cheese, so patience and timing both matter in the end.",

    "Keep your wrists relaxed, your eyes on the screen, and your mind "
    "focused, and your typing speed will improve faster than you think.",
]


class TypingSpeedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.geometry("820x520")
        self.minsize(650, 450)
        self.configure(bg="#1e1e2e")

        self.sample_text = ""
        self.start_time = None
        self.finished = False
        self.timer_job = None

        self._build_layout()
        self.new_text()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        header = tk.Frame(self, bg="#1e1e2e")
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(header, text="Typing Speed Test", font=("Segoe UI", 20, "bold"),
                 bg="#1e1e2e", fg="#f5f5f5").pack(side="left")

        ttk.Button(header, text="New Text", command=self.new_text).pack(side="right", padx=4)
        ttk.Button(header, text="Restart Same Text", command=self.restart_same).pack(side="right", padx=4)

        # Sample text display
        sample_frame = tk.Frame(self, bg="#2a2a3d", bd=0)
        sample_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.sample_widget = tk.Text(sample_frame, height=5, wrap="word",
                                      font=("Consolas", 15), bd=0, padx=14, pady=14,
                                      bg="#2a2a3d", fg="#cfcfe8", state="disabled",
                                      cursor="arrow")
        self.sample_widget.pack(fill="both", expand=True)

        self.sample_widget.tag_config("correct", foreground="#4ade80")
        self.sample_widget.tag_config("incorrect", foreground="#f87171",
                                       background="#4b1d1d")
        self.sample_widget.tag_config("pending", foreground="#9a9ac0")
        self.sample_widget.tag_config("cursor", background="#565694")

        # Input box
        tk.Label(self, text="Type here:", font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#f5f5f5").pack(anchor="w", padx=22)

        self.input_widget = tk.Text(self, height=5, wrap="word", font=("Consolas", 15),
                                     bd=0, padx=14, pady=14, bg="#f5f5f5", fg="#1e1e2e",
                                     insertbackground="#1e1e2e")
        self.input_widget.pack(fill="x", padx=20, pady=(4, 14))
        self.input_widget.bind("<KeyRelease>", self.on_key)
        self.input_widget.bind("<<Paste>>", lambda e: "break")  # discourage pasting

        # Live stats
        stats = tk.Frame(self, bg="#1e1e2e")
        stats.pack(fill="x", padx=20)

        self.time_var = tk.StringVar(value="Time: 0.0s")
        self.wpm_var = tk.StringVar(value="WPM: 0")
        self.acc_var = tk.StringVar(value="Accuracy: 100%")

        for var in (self.time_var, self.wpm_var, self.acc_var):
            tk.Label(stats, textvariable=var, font=("Segoe UI", 13, "bold"),
                     bg="#1e1e2e", fg="#facc15").pack(side="left", padx=(0, 30))

        # Result banner
        self.result_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.result_var, font=("Segoe UI", 14, "bold"),
                 bg="#1e1e2e", fg="#60a5fa", wraplength=760, justify="left").pack(
            anchor="w", padx=20, pady=(14, 0))

    # ------------------------------------------------------------------
    # Test lifecycle
    # ------------------------------------------------------------------
    def new_text(self):
        self.sample_text = random.choice(SAMPLE_TEXTS)
        self._reset_state()

    def restart_same(self):
        self._reset_state()

    def _reset_state(self):
        self.start_time = None
        self.finished = False
        self.result_var.set("")
        self.time_var.set("Time: 0.0s")
        self.wpm_var.set("WPM: 0")
        self.acc_var.set("Accuracy: 100%")

        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        self.sample_widget.config(state="normal")
        self.sample_widget.delete("1.0", "end")
        self.sample_widget.insert("1.0", self.sample_text)
        self.sample_widget.tag_add("pending", "1.0", "end")
        self.sample_widget.config(state="disabled")

        self.input_widget.config(state="normal")
        self.input_widget.delete("1.0", "end")
        self.input_widget.focus_set()

    # ------------------------------------------------------------------
    # Typing logic
    # ------------------------------------------------------------------
    def on_key(self, event=None):
        if self.finished:
            return

        typed = self.input_widget.get("1.0", "end-1c")

        # Start the timer on the very first character typed
        if self.start_time is None and len(typed) > 0:
            self.start_time = time.time()
            self._tick()

        self._highlight(typed)

        if len(typed) >= len(self.sample_text):
            self._finish(typed)

    def _highlight(self, typed):
        self.sample_widget.config(state="normal")
        self.sample_widget.tag_remove("correct", "1.0", "end")
        self.sample_widget.tag_remove("incorrect", "1.0", "end")
        self.sample_widget.tag_remove("pending", "1.0", "end")
        self.sample_widget.tag_remove("cursor", "1.0", "end")

        sample = self.sample_text
        compare_len = min(len(typed), len(sample))

        for i in range(compare_len):
            start = f"1.0+{i}c"
            end = f"1.0+{i+1}c"
            tag = "correct" if typed[i] == sample[i] else "incorrect"
            self.sample_widget.tag_add(tag, start, end)

        if compare_len < len(sample):
            self.sample_widget.tag_add("pending", f"1.0+{compare_len}c", "end")
            self.sample_widget.tag_add("cursor", f"1.0+{compare_len}c", f"1.0+{compare_len+1}c")

        self.sample_widget.config(state="disabled")

    def _tick(self):
        if self.finished or self.start_time is None:
            return
        elapsed = time.time() - self.start_time
        typed = self.input_widget.get("1.0", "end-1c")
        wpm = self._calc_wpm(typed, elapsed)
        self.time_var.set(f"Time: {elapsed:.1f}s")
        self.wpm_var.set(f"WPM: {wpm}")
        self.acc_var.set(f"Accuracy: {self._calc_accuracy(typed)}%")
        self.timer_job = self.after(200, self._tick)

    def _calc_wpm(self, typed, elapsed):
        if elapsed <= 0:
            return 0
        words = len(typed) / 5.0  # standard: 1 "word" = 5 characters
        minutes = elapsed / 60.0
        return round(words / minutes) if minutes > 0 else 0

    def _calc_accuracy(self, typed):
        sample = self.sample_text
        compare_len = min(len(typed), len(sample))
        if compare_len == 0:
            return 100
        correct = sum(1 for i in range(compare_len) if typed[i] == sample[i])
        return round(100 * correct / compare_len)

    def _finish(self, typed):
        self.finished = True
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        elapsed = time.time() - self.start_time if self.start_time else 0
        wpm = self._calc_wpm(typed, elapsed)
        accuracy = self._calc_accuracy(typed)

        self.time_var.set(f"Time: {elapsed:.1f}s")
        self.wpm_var.set(f"WPM: {wpm}")
        self.acc_var.set(f"Accuracy: {accuracy}%")

        self.result_var.set(
            f"Done! You typed at {wpm} words per minute with {accuracy}% accuracy "
            f"in {elapsed:.1f} seconds. Click 'New Text' or 'Restart Same Text' to try again."
        )
        self.input_widget.config(state="disabled")


if __name__ == "__main__":
    app = TypingSpeedApp()
    app.mainloop()