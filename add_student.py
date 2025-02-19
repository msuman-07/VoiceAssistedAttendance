import argparse
import sqlite3

def add_student(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        print(f"{name} added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Student '{name}' already exists.")
    finally:
        conn.close()

def remove_student(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    print(f"{name} removed successfully!")

def update_student(old_name, new_name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name = ? WHERE name = ?", (new_name, old_name))
    conn.commit()
    conn.close()
    print(f"{old_name} updated to {new_name} successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage students in the attendance database.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    add_parser = subparsers.add_parser("add", help="Add students")
    add_parser.add_argument("names", type=str, nargs='+', help="List of student names to add.")
    
    remove_parser = subparsers.add_parser("remove", help="Remove a student")
    remove_parser.add_argument("name", type=str, help="Student name to remove.")
    
    update_parser = subparsers.add_parser("update", help="Update a student's name")
    update_parser.add_argument("old_name", type=str, help="Current student name.")
    update_parser.add_argument("new_name", type=str, help="New student name.")
    
    args = parser.parse_args()
    
    if args.command == "add":
        for name in args.names:
            add_student(name)
    elif args.command == "remove":
        remove_student(args.name)
    elif args.command == "update":
        update_student(args.old_name, args.new_name)

# Add students: python script.py add Alice Bob Charlie
# Remove a student: python script.py remove Alice
# Update a student's name: python script.py update Bob Robert