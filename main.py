import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def calculate_bmi():
    feet = int(feet_entry.get())
    inches = int(inches_entry.get())
    weight_pounds = float(weight_entry.get())

    height_inches = feet * 12 + inches
    height_meters = height_inches * 0.0254

    weight_kg = weight_pounds * 0.45359237

    bmi = weight_kg / (height_meters ** 2)
    
    result_label.config(text="BMI: {:.2f}".format(bmi))
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal Weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    category_label.config(text="Category: {}".format(category))

    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE,
                        bmi FLOAT,
                        category TEXT,
                        weight FLOAT
                      )''')
    
    cursor.execute('''SELECT id FROM bmi_records WHERE date = DATE('now')''')
    existing_record = cursor.fetchone()

    if existing_record:
        cursor.execute('''UPDATE bmi_records SET weight = ? WHERE id = ?''', (weight_kg, existing_record[0]))
    else:
        cursor.execute('''INSERT INTO bmi_records (date, bmi, category, weight) VALUES (DATE('now'), ?, ?, ?)''',
                       (bmi, category, weight_kg))
        
    
    
    conn.commit()
    conn.close()
        update_weight_graph()


def update_weight_graph():
    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT date, weight FROM bmi_records ORDER BY date DESC LIMIT 7''')
    records = cursor.fetchall()
    conn.close()

    dates = [record[0] for record in records]
    weights_kg = [record[1] for record in records]

    weights_lb = [weight_kg * 2.20462 for weight_kg in weights_kg]

    if not weights_lb:
        max_weight_lb = 300
    else:
        max_weight_lb = max(weights_lb)

    weight_figure.clear()

    weight_figure.set_figwidth(8)

    weight_plot = weight_figure.add_subplot(111)
    weight_plot.plot(dates, weights_lb, marker='o', linestyle='-', color='b')
    weight_plot.set_xlabel('Date')
    weight_plot.set_ylabel('Weight (lb)')
    weight_plot.set_title('Weight Progress')

    weight_entry_value = weight_entry.get()
    if weight_entry_value:
        weight_entry_lb = float(weight_entry_value)
        y_max = weight_entry_lb + 50
        y_min = weight_entry_lb - 50 if weight_entry_lb > 50 else 0
    else:
        y_max = 300
        y_min = 0

    weight_plot.set_ylim([y_min, y_max])

    weight_plot.spines['top'].set_visible(False)
    weight_plot.spines['right'].set_visible(False)
    weight_plot.grid(color='lightgray', linestyle='--', linewidth=0.5)

    weight_canvas.draw()


def clear_database():
    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS bmi_records''')
    conn.commit()
    conn.close()
    update_weight_graph()
    
def add_weight_entry():
    date = date_entry.get()
    weight_pounds = float(weight_entry.get())

    weight_kg = weight_pounds * 0.45359237

    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE,
                        bmi FLOAT,
                        category TEXT,
                        weight FLOAT
                      )''')

    cursor.execute('''INSERT INTO bmi_records (date, bmi, category, weight) VALUES (?, ?, ?, ?)''',
                   (date, None, None, weight_kg))

    conn.commit()
    conn.close()

    update_weight_graph()

    

def switch_to_macro_tracker():
    notebook.select(1)

window = tk.Tk()
window.title("BMI Calculator")
window_width = 1300
window.geometry(f"{window_width}x480")
window.resizable(False, False)

notebook = ttk.Notebook(window)

bmi_calculator_tab = ttk.Frame(notebook)
notebook.add(bmi_calculator_tab, text="BMI Calculator")
notebook.pack(expand=True, fill=tk.BOTH)
bmi_calculator_tab.grid_columnconfigure(4, weight=1)
bmi_calculator_tab.grid_rowconfigure(0, weight=1)

feet_label = tk.Label(bmi_calculator_tab, text="Height (feet):")
feet_label.grid(row=0, column=0, sticky="e", padx=(10, 5), pady=10)

feet_entry = tk.Entry(bmi_calculator_tab, width=5)
feet_entry.grid(row=0, column=1, padx=5, pady=10)

inches_label = tk.Label(bmi_calculator_tab, text="Height (inches):")
inches_label.grid(row=0, column=2, sticky="e", padx=(5, 10), pady=10)

inches_entry = tk.Entry(bmi_calculator_tab, width=5)
inches_entry.grid(row=0, column=3, padx=(0, 10), pady=10)

weight_label = tk.Label(bmi_calculator_tab, text="Weight (lb):")
weight_label.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=(0, 10))

weight_entry = tk.Entry(bmi_calculator_tab, width=10)
weight_entry.grid(row=1, column=1, padx=5, pady=(0, 10))

calculate_button = tk.Button(bmi_calculator_tab, text="Calculate", command=calculate_bmi)
calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

result_label = tk.Label(bmi_calculator_tab, text="BMI:")
result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

category_label = tk.Label(bmi_calculator_tab, text="Category:")
category_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

clear_button = tk.Button(bmi_calculator_tab, text="Clear Database", command=clear_database)
clear_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

date_label = tk.Label(bmi_calculator_tab, text="Date (YYYY-MM-DD):")
date_label.grid(row=2, column=2, sticky="e", padx=(5, 10), pady=10)

date_entry = tk.Entry(bmi_calculator_tab, width=10)
date_entry.grid(row=2, column=3, padx=(0, 10), pady=10)

add_entry_button = tk.Button(bmi_calculator_tab, text="Add Entry", command=add_weight_entry)
add_entry_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="w")

weight_figure = plt.Figure(figsize=(6, 4), facecolor='steelblue')
weight_canvas = FigureCanvasTkAgg(weight_figure, master=bmi_calculator_tab)
weight_canvas.get_tk_widget().grid(row=0, column=4, rowspan=8, padx=10, pady=10, sticky="nsew")

weight_plot = weight_figure.add_subplot(111)
weight_plot.set_xlabel('Date')
weight_plot.set_ylabel('Weight (lb)')
weight_plot.set_title('Weight Progress')
weight_plot.set_ylim([0, 300])

update_weight_graph()

macro_tracker_tab = ttk.Frame(notebook)
notebook.add(macro_tracker_tab, text="Macro Tracker")

import macro_tracker

macro_tracker.setup_macro_tracker(macro_tracker_tab, notebook)

window.mainloop()
