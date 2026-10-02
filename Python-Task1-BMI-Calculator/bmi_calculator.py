import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        
        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Height and Weight must be greater than zero.")
            return

        # Unit Conversion if Imperial
        if unit_var.get() == "Imperial":
            # Weight in lbs to kg, Height in inches to meters
            bmi = (weight / (height ** 2)) * 703
        else:
            bmi = weight / (height ** 2)

        # Determine Category & Styles
        if bmi < 18.5:
            category = "Underweight"
            color = "#3498db"  # Blue
            suggestion = "Eat nutrient-rich foods and consult a nutritionist."
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
            color = "#2ecc71"  # Green
            suggestion = "Great job! Maintain your balanced diet and workout routine."
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            color = "#e67e22"  # Orange
            suggestion = "Consider adding light daily exercise and watching calorie intake."
        else:
            category = "Obese"
            color = "#e74c3c"  # Red
            suggestion = "Focus on healthy habits and consult a healthcare professional."

        # Update Display
        lbl_bmi_val.config(text=f"{bmi:.1f}", fg=color)
        lbl_category.config(text=f"Category: {category}", fg=color)
        lbl_tip.config(text=f"Tip: {suggestion}")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def reset_fields():
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    lbl_bmi_val.config(text="--.-", fg="#2c3e50")
    lbl_category.config(text="Category: --", fg="#2c3e50")
    lbl_tip.config(text="")

def update_units():
    if unit_var.get() == "Imperial":
        lbl_weight.config(text="Weight (lbs):")
        lbl_height.config(text="Height (inches):")
    else:
        lbl_weight.config(text="Weight (kg):")
        lbl_height.config(text="Height (meters):")

# App Setup
root = tk.Tk()
root.title("OIBSIP - Advanced Interactive BMI Calculator")
root.geometry("420x450")
root.configure(bg="#f4f6f7")
root.resizable(False, False)

# Unit Selector
unit_frame = tk.Frame(root, bg="#f4f6f7")
unit_frame.pack(pady=10)

unit_var = tk.StringVar(value="Metric")
tk.Radiobutton(unit_frame, text="Metric (kg, m)", variable=unit_var, value="Metric", command=update_units, bg="#f4f6f7", font=("Arial", 10, "bold")).pack(side="left", padx=10)
tk.Radiobutton(unit_frame, text="Imperial (lbs, in)", variable=unit_var, value="Imperial", command=update_units, bg="#f4f6f7", font=("Arial", 10, "bold")).pack(side="left", padx=10)

# Input Box Frame
input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
input_frame.pack(pady=10, padx=20, fill="x")

lbl_weight = tk.Label(input_frame, text="Weight (kg):", bg="#ffffff", font=("Arial", 10, "bold"))
lbl_weight.grid(row=0, column=0, padx=15, pady=10, sticky="w")
entry_weight = tk.Entry(input_frame, font=("Arial", 11), width=12)
entry_weight.grid(row=0, column=1, padx=15, pady=10)

lbl_height = tk.Label(input_frame, text="Height (meters):", bg="#ffffff", font=("Arial", 10, "bold"))
lbl_height.grid(row=1, column=0, padx=15, pady=10, sticky="w")
entry_height = tk.Entry(input_frame, font=("Arial", 11), width=12)
entry_height.grid(row=1, column=1, padx=15, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=10)

btn_calc = tk.Button(btn_frame, text="Calculate BMI", command=calculate_bmi, bg="#2980b9", fg="white", font=("Arial", 10, "bold"), padx=10, pady=3, bd=0, cursor="hand2")
btn_calc.pack(side="left", padx=5)

btn_reset = tk.Button(btn_frame, text="Reset", command=reset_fields, bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"), padx=10, pady=3, bd=0, cursor="hand2")
btn_reset.pack(side="left", padx=5)

# Output Display Frame
result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
result_frame.pack(pady=10, padx=20, fill="both", expand=True)

lbl_bmi_val = tk.Label(result_frame, text="--.-", font=("Arial", 32, "bold"), bg="#ffffff", fg="#2c3e50")
lbl_bmi_val.pack(pady=(10, 0))

lbl_category = tk.Label(result_frame, text="Category: --", font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50")
lbl_category.pack(pady=5)

lbl_tip = tk.Label(result_frame, text="", font=("Arial", 9, "italic"), bg="#ffffff", fg="#555555", wraplength=350)
lbl_tip.pack(pady=(0, 10))

root.mainloop()