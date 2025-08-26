import sqlite3

conn=sqlite3.connect("gamehub.db")
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )''')
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,           
                title TEXT NOT NULL
            )''')
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS SCORE (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                game_id INTEGER,
                score INTEGER,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(player_id) REFERENCES players(id),
                FOREIGN KEY(game_id) REFERENCES games(id)
            )''')
conn.commit()
conn.close()
print("Database and tables created successfully.")

import tkinter as tk
from tkinter import messagebox

def on_login():
    username = entry_username.get()
    password = entry_password.get()

    conn=sqlite3.connect("gamehub.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    conn.close()

def on_register():
    username=entry_username.get()
    password=entry_password.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        return
    conn=sqlite3.connect("gamehub.db")
    cur=conn.cursor()
    try:
        cur.execute("insert into users(username,password) values(?,?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Successful", "You can now log in.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Registration Failed", "Username already exists.")
    conn.close()

root = tk.Tk()
root.title("GameHub Login")
root.geometry("1000x1000")
root.resizable(False, False)
root.configure(bg="#f0f0f0")
root.eval('tk::PlaceWindow . center')

username=tk.Label(root, text="Username:", bg="#f0f0f0").pack(pady=10)
entry_username=tk.Entry(root)
entry_username.pack()
password=tk.Label(root, text="Password:", bg="#f0f0f0").pack(pady=10)
entry_password=tk.Entry(root, show="*")
entry_password.pack()

btn_login=tk.Button(root, text="Login", command=on_login, bg="#4CAF50", fg="white").pack(pady=10)
btn_register=tk.Button(root, text="Register", command=on_register, bg="#2196F3", fg="white").pack(pady=5)
btn_exit=tk.Button(root, text="Exit", command=root.quit, bg="#f44336", fg="white").pack(pady=5)
root.mainloop()

# connect to the game
# Example: Add a simple game launcher window after successful login

def launch_gamehub():
    hub = tk.Tk()
    hub.title("GameHub")
    hub.geometry("600x400")
    hub.configure(bg="#e0e0e0")

    tk.Label(hub, text="Select a Game to Play", font=("Arial", 18), bg="#e0e0e0").pack(pady=20)

    import subprocess

    def launch_quizapp():
        try:
            subprocess.Popen(["python", "quizapp.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch quizapp.py: {e}")

    def launch_snake():
        try:
            subprocess.Popen(["python", "snake.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch snake.py: {e}")

    tk.Button(hub, text="quizapp", command=launch_quizapp, width=20, height=2, bg="#8bc34a").pack(pady=10)
    tk.Button(hub, text="Snake", command=launch_snake, width=20, height=2, bg="#ff9800").pack(pady=10)
    tk.Button(hub, text="Exit", command=hub.destroy, width=20, height=2, bg="#f44336").pack(pady=10)

    hub.mainloop()

# To connect this, call launch_gamehub() after successful login:
# Replace 'root.destroy()' in on_login() with:
#   root.destroy()
#   launch_gamehub()
launch_gamehub()
    
   