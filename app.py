import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import sqlite3
from datetime import datetime

# Database Setup
def initialize_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        date TEXT,
                        time TEXT
                      )''')
    conn.commit()
    conn.close()

# Record Attendance
def record_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Attendance marked for {name}")

# Voice Recognition
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Info", "Listening... Please speak your name.")
            audio = recognizer.listen(source, timeout=5)
            name = recognizer.recognize_google(audio)
            record_attendance(name)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio. Please try again.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not connect to the speech recognition service.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Generate Attendance Report
def view_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()

    report_window = tk.Toplevel(root)
    report_window.title("Attendance Report")

    tk.Label(report_window, text="ID", width=5).grid(row=0, column=0)
    tk.Label(report_window, text="Name", width=20).grid(row=0, column=1)
    tk.Label(report_window, text="Date", width=15).grid(row=0, column=2)
    tk.Label(report_window, text="Time", width=15).grid(row=0, column=3)

    for i, record in enumerate(records):
        tk.Label(report_window, text=record[0], width=5).grid(row=i+1, column=0)
        tk.Label(report_window, text=record[1], width=20).grid(row=i+1, column=1)
        tk.Label(report_window, text=record[2], width=15).grid(row=i+1, column=2)
        tk.Label(report_window, text=record[3], width=15).grid(row=i+1, column=3)

# Main Application
def clear_data():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Attendance data cleared!")

initialize_db()

root = tk.Tk()
root.title("Voice Assistant Attendance")
root.geometry("400x300")

tk.Label(root, text="Voice Assistant Attendance System", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Mark Attendance", command=recognize_voice, width=20).pack(pady=10)

tk.Button(root, text="View Attendance", command=view_attendance, width=20).pack(pady=10)

tk.Button(root, text="Clear Data", command=clear_data, width=20).pack(pady=10)

tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=10)

root.mainloop()
