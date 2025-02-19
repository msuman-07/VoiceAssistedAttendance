import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from PIL import Image, ImageTk

class VoiceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Assisted Attendance")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1e1f26")

        self.root.bind("<Escape>", self.exit_app)

        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()
        
        self.speaker = pyttsx3.init()
        
        self.setup_database()
        self.show_login_page()
    
    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

    def exit_app(self, event=None):
        self.root.destroy()

    def handle_enter_key(self, event=None):
        self.verify_login()

    def setup_database(self):
        """ Creates tables if they don't exist """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT,
                time TEXT
            )
        """)
        self.conn.commit()

        self.cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', '1234')")
            self.conn.commit()

    def show_login_page(self):
        """ Displays login page """
        self.clear_root()

        self.root.bind("<Return>", self.handle_enter_key)

        bg_image = Image.open("media/login.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image
        self.canvas.pack(fill="both", expand=True)

        self.header_label = tk.Label(self.root, text="Login", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.2, anchor="center")

        self.login_frame = tk.Frame(self.root, bg="#1e1f26")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="Username:", bg="#1e1f26", fg="white", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text="Password:", bg="#1e1f26", fg="white", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_frame, text="Login", command=self.verify_login, bg="#3c91e6", fg="white", font=("Arial", 14)).grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(self.root, text="Exit", command=self.exit_app, bg="#ff0000", fg="white", font=("Arial", 16)).place(relx=1, rely=0.0, anchor="ne")

    def verify_login(self):
        """ Verifies admin login """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        self.cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    def show_main_page(self):
        """ Displays the main attendance page """
        self.clear_root()

        bg_image = Image.open("media/homepage.png")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image
        self.canvas.pack(fill="both", expand=True)

        self.header_label = tk.Label(self.root, text="Voice-Assisted Attendance", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.0, anchor="n")

        self.attendance_frame = tk.Frame(self.root, bg="#1e1f26")
        self.attendance_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(self.attendance_frame, text="Mark Attendance (Voice)", command=self.mark_attendance, bg="#3c91e6", fg="white", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=20)
        tk.Button(self.attendance_frame, text="View Attendance", command=self.view_attendance, bg="#3c91e6", fg="white", font=("Arial", 16)).grid(row=1, column=0, padx=20, pady=20)
        
        tk.Button(self.root, text="Logout", command=self.show_login_page, bg="#ff0000", fg="white", font=("Arial", 16)).place(relx=1, rely=0.0, anchor="ne")

    def mark_attendance(self):
        """ Uses voice recognition to mark attendance by detecting student names """
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Speak Now", "Say your name clearly to mark attendance.")
            print("Listening for name...")
            try:
                audio = recognizer.listen(source, timeout=5)
                student_name = recognizer.recognize_google(audio).strip().title()  

                self.cursor.execute("SELECT name FROM students WHERE name = ?", (student_name,))
                student = self.cursor.fetchone()

                if student:
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    current_time = datetime.now().strftime("%H:%M:%S")

                    self.cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", 
                                        (student_name, current_date, current_time))
                    self.conn.commit()
                    self.speak(f"Attendance marked for {student_name}!")
                    messagebox.showinfo("Success", f"Attendance marked for {student_name} at {current_time}!")
                else:
                    messagebox.showerror("Error", f"{student_name} not found in the system.")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand voice input.")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not connect to voice recognition service.")
        
    def show_add_student_page(self):
        """ Displays a page to add new students """
        self.clear_root()

        self.header_label = tk.Label(self.root, text="Add Student", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.0, anchor="n")

        self.add_student_frame = tk.Frame(self.root, bg="#1e1f26")
        self.add_student_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.add_student_frame, text="Student Name:", bg="#1e1f26", fg="white", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.student_name_entry = tk.Entry(self.add_student_frame, font=("Arial", 14))
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.add_student_frame, text="Add Student", command=self.add_student, bg="#3c91e6", fg="white", font=("Arial", 14)).grid(row=1, column=0, columnspan=2, pady=15)
        tk.Button(self.add_student_frame, text="Back", command=self.show_main_page, bg="#3c91e6", fg="white", font=("Arial", 14)).grid(row=2, column=0, columnspan=2, pady=10)

    # def add_student(self):
    #     """ Adds a new student to the database """
    #     student_name = self.student_name_entry.get().strip().title()

    #     if not student_name:
    #         messagebox.showerror("Input Error", "Please enter a valid name.")
    #         return

    #     try:
    #         self.cursor.execute("INSERT INTO students (name) VALUES (?)", (student_name,))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", f"{student_name} added successfully!")
    #         self.show_main_page()
    #     except sqlite3.IntegrityError:
    #         messagebox.showerror("Error", "Student already exists.")
    
    def view_attendance(self):
        self.clear_root()

        self.header_label = tk.Label(self.root, text="Attendance Records", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.0, anchor="n")

        self.attendance_table = ttk.Treeview(self.root, columns=("Name", "Date", "Time"), show="headings")
        self.attendance_table.heading("Name", text="Name")
        self.attendance_table.heading("Date", text="Date")
        self.attendance_table.heading("Time", text="Time")

        self.attendance_table.place(relx=0.5, rely=0.5, anchor="center")

        self.cursor.execute("SELECT name, date, time FROM attendance")
        for row in self.cursor.fetchall():
            self.attendance_table.insert("", "end", values=row)

        tk.Button(self.root, text="Back", command=self.show_main_page, bg="#3c91e6", fg="white", font=("Arial", 14)).place(relx=0.5, rely=0.9, anchor="center")

    def clear_root(self):
        """ Clears all widgets from the root window """
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAttendanceApp(root)
    root.mainloop()