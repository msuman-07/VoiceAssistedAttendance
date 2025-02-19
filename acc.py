import sqlite3
import tkinter as tk
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                     )''')
    conn.commit()
    conn.close()


def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Admin registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def remove_user():
    username = entry_username.get()
    
    if not username:
        messagebox.showerror("Error", "Please enter a username to remove.")
        return
    
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Admin removed successfully!")

def update_password():
    username = entry_username.get()
    new_password = entry_password.get()
    
    if not username or not new_password:
        messagebox.showerror("Error", "Please enter both username and new password.")
        return
    
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE admins SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password updated successfully!")

create_table()

# Tkinter GUI
root = tk.Tk()
root.title("Admin Management")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Admin Management Portal for Attendance Marker", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=20)

tk.Label(frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_username = tk.Entry(frame, font=("Arial", 12))
entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=5)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Register", command=register_user, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Remove", command=remove_user, font=("Arial", 12), bg="#f44336", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Update Password", command=update_password, font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5).grid(row=0, column=2, padx=10)

root.mainloop()