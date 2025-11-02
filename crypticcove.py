#!/usr/bin/env python3
"""
Cryptic Cove: Password Strength Checker & Secure Password Generator
----------------------------------------------------------------------------
Educational cybersecurity utility — for ethical use only.
"""

import string
import secrets
import math
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- CORE LOGIC ----------


def check_strength(password: str):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        label = "Weak"
    elif score == 3:
        label = "Medium"
    elif score == 4:
        label = "Strong"
    else:
        label = "Very Strong"
    return score, label


def estimate_entropy(password: str):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if pool == 0:
        pool = len(set(password)) or 1
    return len(password) * math.log2(pool)


def estimate_crack_time(entropy_bits: float, guesses_per_second: float = 1e9):
    expected_guesses = 2 ** (entropy_bits - 1)
    return expected_guesses / guesses_per_second


def pretty_time(seconds: float):
    year = 365 * 24 * 3600
    if seconds < 1:
        return f"{seconds:.3f} sec"
    if seconds < 60:
        return f"{seconds:.1f} sec"
    if seconds < 3600:
        return f"{seconds/60:.1f} min"
    if seconds < 86400:
        return f"{seconds/3600:.1f} hr"
    if seconds < year:
        return f"{seconds/86400:.1f} days"
    if seconds < 100*year:
        return f"{seconds/year:.1f} years"
    return f"{seconds/year:.1e} years"


def generate_password(length=12):
    if length < 4:
        raise ValueError("Password length must be at least 4.")
    classes = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]
    pw = [secrets.choice(c) for c in classes]
    full_pool = ''.join(classes)
    for _ in range(length - len(pw)):
        pw.append(secrets.choice(full_pool))
    secrets.SystemRandom().shuffle(pw)
    return ''.join(pw)

# ---------- GUI SECTION ----------


class CrypticCoveApp:
    def __init__(self, root):
        self.root = root
        root.title("🧩 Cryptic Cove - Password Strength Checker & Generator")
        root.geometry("540x440")
        root.resizable(True, True)

        # Colors and theme
        bg = "#0B0C10"      # deep black-green
        fg = "#1EFF00"      # green
        accent = "#FFFFFF"  # white
        text = "#FFFFFF"    # white

        root.configure(bg=bg)
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background=bg,
                        foreground=text, font=("Open Sans Bold", 25))
        style.configure("Header.TLabel", background=bg,
                        foreground=fg, font=("Open Sans Bold", 25, "bold"))
        style.configure("TButton",
                        background=accent, foreground="#000000",
                        font=("Open Sans Bold", 25, "bold"), padding=6)
        style.map("TButton",
                  background=[("active", fg)],
                  foreground=[("active", "#000000")])

        ttk.Label(root, text="CRYPTIC COVE BY SAHAL KHAN",
                  style="Header.TLabel").pack(pady=(15, 5))
        ttk.Label(root, text="Password Strength Checker & Generator",
                  foreground=accent).pack()

        frame = ttk.Frame(root, style="TFrame")
        frame.pack(pady=25)

        ttk.Label(frame, text="Enter Password:").grid(
            row=0, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(frame, width=35, show="*")
        self.password_entry.grid(row=0, column=1, padx=10)

        self.result_label = ttk.Label(frame, text="", font=(
            "Open Sans Bold", 10, "bold"), foreground=fg)
        self.result_label.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Check Strength", command=self.check_password).grid(
            row=2, column=0, columnspan=2, pady=5)

        ttk.Separator(root, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(root, text="Generate Secure Password",
                  foreground=accent).pack(pady=(5, 5))
        gen_frame = ttk.Frame(root)
        gen_frame.pack()

        ttk.Label(gen_frame, text="Length:").grid(row=0, column=0, padx=5)
        self.length_spin = ttk.Spinbox(gen_frame, from_=8, to=64, width=5)
        self.length_spin.set(12)
        self.length_spin.grid(row=0, column=1, padx=5)

        ttk.Button(gen_frame, text="Generate", command=self.generate).grid(
            row=0, column=2, padx=10)

        self.generated_label = ttk.Label(root, text="", font=(
            "Open Sans Bold", 10, "bold"), wraplength=480, foreground=fg)
        self.generated_label.pack(pady=10)

        ttk.Label(root, text="© 2025 CrypticCove  |  For Ethical Use Only",
                  foreground=text).pack(side="bottom", pady=10)

    def check_password(self):
        pw = self.password_entry.get()
        if not pw:
            messagebox.showwarning(
                "No Input", "Please enter a password to check.")
            return
        score, label = check_strength(pw)
        entropy = estimate_entropy(pw)
        seconds = estimate_crack_time(entropy)
        self.result_label.config(
            text=f"Strength: {label} ({score}/5)\nEntropy: {entropy:.1f} bits\nCrack Time ≈ {pretty_time(seconds)}"
        )

    def generate(self):
        length = int(self.length_spin.get())
        pw = generate_password(length)
        self.generated_label.config(text=f"Generated: {pw}")
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# ---------- MAIN ----------


if __name__ == "__main__":
    root = tk.Tk()
    app = CrypticCoveApp(root)
    root.mainloop()
