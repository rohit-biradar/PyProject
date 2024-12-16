import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Install required libraries dynamically
def install(package):
    try:
        __import__(package)
    except ImportError:
        os.system(f"pip install {package}")

install("pandas")
install("matplotlib")

# Initialize data storage
data = {
    "Day": [],
    "Steps": [],
    "Water": [],
    "Sleep": [],
    "BMI": []
}
dataframe = pd.DataFrame(data)

# Function to update data and charts
def update_data():
    global dataframe  # Declare 'dataframe' as global before its usage
    try:
        steps = int(steps_entry.get() or 0)
        water = float(water_entry.get() or 0)
        sleep = float(sleep_entry.get() or 0)
        weight = float(weight_entry.get() or 0)
        height = float(height_entry.get() or 1) / 100  # Avoid division by zero

        bmi = round(weight / (height ** 2), 2) if height > 0 else 0

        # Update the data
        day = f"Day {len(dataframe) + 1}" if len(dataframe) < 7 else f"Day 7"
        new_row = {
            "Day": day,
            "Steps": steps,
            "Water": water,
            "Sleep": sleep,
            "BMI": bmi
        }

        if len(dataframe) >= 7:
            dataframe.iloc[-1] = new_row  # Replace last row if 7 entries are reached
        else:
            dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)

        # Update summary
        summary_label.config(text=f"Steps: {steps}\nWater: {water} L\nSleep: {sleep} hrs\nBMI: {bmi}")
        last_updated_label.config(text=f"Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Update charts
        update_charts()

        # Clear inputs
        steps_entry.delete(0, tk.END)
        water_entry.delete(0, tk.END)
        sleep_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Function to create doughnut charts
def create_doughnut_chart(ax, value, total, label, color):
    if value > total: value = total
    if value < 0: value = 0
    ax.pie([value, total - value], labels=[f"{label}: {value}", "Remaining"], 
           colors=[color, "#f0f0f0"], startangle=90, counterclock=False, wedgeprops={"width": 0.3})

# Function to update charts
def update_charts():
    for widget in charts_frame.winfo_children():
        widget.destroy()

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    fig.tight_layout(pad=4)

    if not dataframe.empty:
        # Doughnut Charts
        create_doughnut_chart(axes[0, 0], dataframe["Steps"].iloc[-1], 10000, "Steps", "#4CAF50")
        create_doughnut_chart(axes[0, 1], dataframe["Water"].iloc[-1], 3, "Water (L)", "#2196F3")
        create_doughnut_chart(axes[0, 2], dataframe["Sleep"].iloc[-1], 8, "Sleep (hrs)", "#FFC107")

        # Weekly Line Charts (Days on X-axis, Inputs on Y-axis)
        x_values = dataframe["Day"].tolist()  # Days (1 to current count)
        y_steps = dataframe["Steps"].tolist()
        y_water = dataframe["Water"].tolist()
        y_sleep = dataframe["Sleep"].tolist()

        # Steps Line Chart
        axes[1, 0].plot(x_values, y_steps, label="Steps", marker="o", color="#4CAF50")
        axes[1, 0].set_ylim(0, max(y_steps) + 500)  # Set appropriate y-axis range
        axes[1, 0].set_title("Steps")
        axes[1, 0].set_xlabel("Days")
        axes[1, 0].set_ylabel("Steps")
        axes[1, 0].grid(True, linestyle="--", alpha=0.7)
        axes[1, 0].legend()

        # Water Line Chart
        axes[1, 1].plot(x_values, y_water, label="Water (L)", marker="o", color="#2196F3")
        axes[1, 1].set_ylim(0, max(y_water) + 0.5)  # Set appropriate y-axis range
        axes[1, 1].set_title("Water Intake")
        axes[1, 1].set_xlabel("Days")
        axes[1, 1].set_ylabel("Liters")
        axes[1, 1].grid(True, linestyle="--", alpha=0.7)
        axes[1, 1].legend()

        # Sleep Line Chart
        axes[1, 2].plot(x_values, y_sleep, label="Sleep (hrs)", marker="o", color="#FFC107")
        axes[1, 2].set_ylim(0, max(y_sleep) + 1)  # Set appropriate y-axis range
        axes[1, 2].set_title("Sleep")
        axes[1, 2].set_xlabel("Days")
        axes[1, 2].set_ylabel("Hours")
        axes[1, 2].grid(True, linestyle="--", alpha=0.7)
        axes[1, 2].legend()

    else:
        for ax in axes.flat:
            ax.text(0.5, 0.5, "No Data", fontsize=12, ha='center')

    canvas = FigureCanvasTkAgg(fig, master=charts_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Initialize the main application window
root = tk.Tk()
root.title("Health Tracker")
root.geometry("800x600")

# Input Section
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill="x", pady=10)

steps_label = ttk.Label(input_frame, text="Steps:")
steps_label.grid(row=0, column=0, padx=5, pady=5)
steps_entry = ttk.Entry(input_frame)
steps_entry.grid(row=0, column=1, padx=5, pady=5)

water_label = ttk.Label(input_frame, text="Water (L):")
water_label.grid(row=0, column=2, padx=5, pady=5)
water_entry = ttk.Entry(input_frame)
water_entry.grid(row=0, column=3, padx=5, pady=5)

sleep_label = ttk.Label(input_frame, text="Sleep (hrs):")
sleep_label.grid(row=1, column=0, padx=5, pady=5)
sleep_entry = ttk.Entry(input_frame)
sleep_entry.grid(row=1, column=1, padx=5, pady=5)

weight_label = ttk.Label(input_frame, text="Weight (kg):")
weight_label.grid(row=1, column=2, padx=5, pady=5)
weight_entry = ttk.Entry(input_frame)
weight_entry.grid(row=1, column=3, padx=5, pady=5)

height_label = ttk.Label(input_frame, text="Height (cm):")
height_label.grid(row=2, column=0, padx=5, pady=5)
height_entry = ttk.Entry(input_frame)
height_entry.grid(row=2, column=1, padx=5, pady=5)

submit_button = ttk.Button(input_frame, text="Submit", command=update_data)
submit_button.grid(row=2, column=3, padx=5, pady=5)

# Summary Section
summary_frame = ttk.Frame(root, padding=10)
summary_frame.pack(fill="x", pady=10)

summary_label = ttk.Label(summary_frame, text="Enter your data to see the summary", font=("Arial", 12))
summary_label.pack()

last_updated_label = ttk.Label(summary_frame, text="Last Updated: N/A", font=("Arial", 10), foreground="gray")
last_updated_label.pack()

# Charts Section
charts_frame = ttk.Frame(root, padding=10)
charts_frame.pack(fill="both", expand=True)

# Run the main application loop
root.mainloop()
