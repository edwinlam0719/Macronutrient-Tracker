import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

meal_list = None  # Define the meal_list as a global variable
name_entry = None
calories_entry = None
fat_entry = None
protein_entry = None
carbohydrates_entry = None

def add_meal():
    global name_entry, calories_entry, fat_entry, protein_entry, carbohydrates_entry

    name = name_entry.get()
    calories = float(calories_entry.get())
    fat = float(fat_entry.get())
    protein = float(protein_entry.get())
    carbohydrates = float(carbohydrates_entry.get())
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store the meal data in the SQLite database
    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()

    # Create the "meals" table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS meals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        calories FLOAT,
                        fat FLOAT,
                        protein FLOAT,
                        carbohydrates FLOAT,
                        date_added TEXT
                      )''')

    # Insert the meal data into the "meals" table
    cursor.execute('''INSERT INTO meals (name, calories, fat, protein, carbohydrates, date_added)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (name, calories, fat, protein, carbohydrates, current_time))

    conn.commit()
    conn.close()

    # Clear the input fields
    name_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    fat_entry.delete(0, tk.END)
    protein_entry.delete(0, tk.END)
    carbohydrates_entry.delete(0, tk.END)

    # Refresh the meal list
    refresh_meal_list()

def refresh_meal_list():
    global meal_list

    # Clear the meal list
    meal_list.delete(0, tk.END)

    # Retrieve the meal data from the "meals" table
    conn = sqlite3.connect('FitnessApp/userdata.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS meals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        calories FLOAT,
                        fat FLOAT,
                        protein FLOAT,
                        carbohydrates FLOAT,
                        date_added TEXT
                      )''')
    cursor.execute("SELECT name, calories, fat, protein, carbohydrates, date_added FROM meals")
    meals = cursor.fetchall()
    conn.close()

    # Populate the meal list with the retrieved data
    for meal in meals:
        name = meal[0]
        calories = meal[1]
        fat = meal[2]
        protein = meal[3]
        carbohydrates = meal[4]
        date_added = meal[5]
        meal_info = f"{name} - Calories: {calories}, Fat: {fat}, Protein: {protein}, Carbohydrates: {carbohydrates}, Date Added: {date_added}"
        meal_list.insert(tk.END, meal_info)



# Define the global variables for goal entry, days entry, and deficit label
goal_entry = None
days_entry = None
deficit_label = None

def setup_macro_tracker(macro_tracker_tab, notebook):
    global meal_list, name_entry, calories_entry, fat_entry, protein_entry, carbohydrates_entry, goal_entry, days_entry, deficit_label

    # Create and place the widgets in the Macro Tracker tab
    macro_label = tk.Label(macro_tracker_tab, text="Macro Tracker", font=("Arial", 16, "bold"))
    macro_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    goal_label = tk.Label(macro_tracker_tab, text="Weight Goal:")
    goal_label.grid(row=1, column=0, sticky="w")

    goal_entry = tk.Entry(macro_tracker_tab, width=10)
    goal_entry.grid(row=1, column=1, padx=5, sticky="w")

    days_label = tk.Label(macro_tracker_tab, text="Number of Days:")
    days_label.grid(row=2, column=0, sticky="w")

    days_entry = tk.Entry(macro_tracker_tab, width=10)
    days_entry.grid(row=2, column=1, padx=5, sticky="w")

    calculate_button = tk.Button(macro_tracker_tab, text="Calculate", command=calculate_daily_calorie_deficit)
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

    deficit_label = tk.Label(macro_tracker_tab, text="Daily Calorie Deficit:")
    deficit_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 10))

    name_label = tk.Label(macro_tracker_tab, text="Meal Name:", width=10)  # Adjust the width of the meal name label
    name_label.grid(row=5, column=0, sticky="w")

    name_entry = tk.Entry(macro_tracker_tab, width=30)
    name_entry.grid(row=5, column=1, padx=5, sticky="w")

    calories_label = tk.Label(macro_tracker_tab, text="Calories:")
    calories_label.grid(row=6, column=0, sticky="w")

    calories_entry = tk.Entry(macro_tracker_tab, width=10)
    calories_entry.grid(row=6, column=1, padx=5, sticky="w")

    fat_label = tk.Label(macro_tracker_tab, text="Fat (g):")
    fat_label.grid(row=7, column=0, sticky="w")

    fat_entry = tk.Entry(macro_tracker_tab, width=10)
    fat_entry.grid(row=7, column=1, padx=5, sticky="w")

    protein_label = tk.Label(macro_tracker_tab, text="Protein (g):")
    protein_label.grid(row=8, column=0, sticky="w")

    protein_entry = tk.Entry(macro_tracker_tab, width=10)
    protein_entry.grid(row=8, column=1, padx=5, sticky="w")

    carbohydrates_label = tk.Label(macro_tracker_tab, text="Carbohydrates (g):")
    carbohydrates_label.grid(row=9, column=0, sticky="w")

    carbohydrates_entry = tk.Entry(macro_tracker_tab, width=10)
    carbohydrates_entry.grid(row=9, column=1, padx=5, sticky="w")

    add_meal_button = tk.Button(macro_tracker_tab, text="Add Meal", command=add_meal)
    add_meal_button.grid(row=10, column=0, pady=10, sticky="w")

    meal_list_label = tk.Label(macro_tracker_tab, text="Meal List:")
    meal_list_label.grid(row=5, column=2, sticky="w")  # Adjust the row and column for the meal list label

    meal_list = tk.Listbox(macro_tracker_tab, width=50)
    meal_list.grid(row=6, column=2, rowspan=5, padx=5, pady=5, sticky="nsew")  # Adjust the row and column for the meal list

    refresh_meal_list()

    back_button = tk.Button(macro_tracker_tab, text="Back to BMI Calculator", command=lambda: notebook.select(0))
    back_button.grid(row=11, column=0, columnspan=2, pady=10, sticky="w")

    macro_tracker_tab.grid_rowconfigure(6, weight=1)  # Allow the meal list to expand vertically

def calculate_daily_calorie_deficit():
    global goal_entry, days_entry, deficit_label

    try:
        weight_goal = float(goal_entry.get())
        num_days = int(days_entry.get())

        if num_days <= 0:
            raise ValueError("Number of days should be a positive integer.")

        # Retrieve the earliest weight entry from the bmi_records database
        conn = sqlite3.connect('FitnessApp/userdata.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date DATE,
                            bmi FLOAT,
                            category TEXT,
                            weight FLOAT
                          )''')
        cursor.execute("SELECT weight FROM bmi_records ORDER BY date ASC LIMIT 1")
        earliest_weight_entry = cursor.fetchone()

        if earliest_weight_entry is None:
            raise ValueError("No weight entries found in the database.")

        earliest_weight = earliest_weight_entry[0]
        print(earliest_weight)

        conn.close()

       

        daily_deficit = ((weight_goal - earliest_weight) * 3500 / num_days)/10
        deficit_label.config(text=f"Approximate Daily Calorie Intake: {daily_deficit:.2f} calories")
    except ValueError as e:
        deficit_label.config(text=str(e))