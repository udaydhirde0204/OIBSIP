import string
import secrets
import tkinter as tk
from tkinter import messagebox

def generate_password():
    length_str = entry_length.get().strip()
    
    if not length_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid numeric length.")
        return

    length = int(length_str)
    if length < 4:
        messagebox.showerror("Security Warning", "Password length should be at least 4 characters.")
        return

    # Base Character Pool
    chars = ""
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += string.punctuation

    # Remove Excluded Characters
    exclude_chars = entry_exclude.get().strip()
    if exclude_chars:
        chars = "".join([c for c in chars if c not in exclude_chars])

    if not chars:
        messagebox.showerror("Configuration Error", "Select at least one character set or remove excessive exclusions.")
        return

    # Cryptographically Secure Generation
    password = "".join(secrets.choice(chars) for _ in range(length))
    
    # Update UI Display
    entry_result.config(state="normal")
    entry_result.delete(0, tk.END)
    entry_result.insert(0, password)
    entry_result.config(state="readonly")

    # Evaluate Metrics & Strength
    evaluate_strength(password, length)
    lbl_copy_status.config(text="")  # Clear previous copy status

def evaluate_strength(password, length):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([length >= 8, length >= 12, has_upper, has_lower, has_digit, has_symbol])

    if score <= 2:
        lbl_strength.config(text="Strength: 🔴 Weak", fg="#e74c3c")
    elif score <= 4:
        lbl_strength.config(text="Strength: 🟠 Moderate", fg="#e67e22")
    else:
        lbl_strength.config(text="Strength: 🟢 Strong", fg="#2ecc71")

def copy_to_clipboard():
    password = entry_result.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        lbl_copy_status.config(text="✓ Copied to Clipboard!", fg="#27ae60")
    else:
        messagebox.showwarning("Warning", "No password generated yet.")

# UI Setup
root = tk.Tk()
root.title("OIBSIP - Advanced Password Generator")
root.geometry("420x460")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Title Header
tk.Label(root, text="🔒 Password Generator", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=(15, 5))

# Length Selector Frame
frame_len = tk.Frame(root, bg="#1e1e2e")
frame_len.pack(pady=5)

tk.Label(frame_len, text="Password Length:", font=("Arial", 10, "bold"), bg="#1e1e2e", fg="#a6adc8").pack(side="left", padx=5)
entry_length = tk.Entry(frame_len, width=8, font=("Arial", 11), justify="center", bg="#313244", fg="#ffffff", insertbackground="white")
entry_length.insert(0, "12")
entry_length.pack(side="left", padx=5)

# Custom Options Frame
frame_opts = tk.Frame(root, bg="#1e1e2e")
frame_opts.pack(pady=5, anchor="w", padx=60)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(frame_opts, text="Uppercase Letters (A-Z)", variable=var_upper, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244", activebackground="#1e1e2e").pack(anchor="w", pady=2)
tk.Checkbutton(frame_opts, text="Lowercase Letters (a-z)", variable=var_lower, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244", activebackground="#1e1e2e").pack(anchor="w", pady=2)
tk.Checkbutton(frame_opts, text="Numbers (0-9)", variable=var_digits, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244", activebackground="#1e1e2e").pack(anchor="w", pady=2)
tk.Checkbutton(frame_opts, text="Special Symbols (@#$%)", variable=var_symbols, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244", activebackground="#1e1e2e").pack(anchor="w", pady=2)

# Exclude Specific Characters
frame_ex = tk.Frame(root, bg="#1e1e2e")
frame_ex.pack(pady=5)
tk.Label(frame_ex, text="Exclude Characters:", font=("Arial", 9), bg="#1e1e2e", fg="#a6adc8").pack(side="left", padx=5)
entry_exclude = tk.Entry(frame_ex, width=12, font=("Arial", 10), bg="#313244", fg="#ffffff", insertbackground="white")
entry_exclude.pack(side="left", padx=5)

# Generate Action
tk.Button(root, text="Generate Secure Password", command=generate_password, bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), padx=10, pady=4, bd=0, cursor="hand2").pack(pady=12)

# Output Frame
entry_result = tk.Entry(root, font=("Courier", 12, "bold"), width=30, state="readonly", justify="center", bg="#313244", fg="#a6e3a1")
entry_result.pack(pady=5)

# Metrics Display
lbl_strength = tk.Label(root, text="Strength: -", font=("Arial", 10, "bold"), bg="#1e1e2e", fg="#cdd6f4")
lbl_strength.pack(pady=3)

# Clipboard Controls
tk.Button(root, text="📋 Copy to Clipboard", command=copy_to_clipboard, bg="#45475a", fg="#cdd6f4", font=("Arial", 9, "bold"), bd=0, cursor="hand2").pack(pady=4)
lbl_copy_status = tk.Label(root, text="", font=("Arial", 9, "bold"), bg="#1e1e2e")
lbl_copy_status.pack(pady=2)

root.mainloop()