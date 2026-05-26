import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection config
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="312186846khai.",
    database="game_manager"
)
cursor = conn.cursor()

# --- Helper functions ---
def fetch_games():
    cursor.execute("SELECT games.game_id, games.title, games.genre, games.platform, games.release_year, owners.name FROM games LEFT JOIN owners ON games.owner_id = owners.owner_id")
    return cursor.fetchall()

def fetch_owners():
    cursor.execute("SELECT * FROM owners")
    return cursor.fetchall()


def refresh_game_table():
    for row in game_table.get_children():
        game_table.delete(row)
    for row in fetch_games():
        game_table.insert('', 'end', values=row)


def add_game():
    title = title_entry.get()
    genre = genre_entry.get()
    platform = platform_entry.get()
    year = year_entry.get()
    owner = owner_combo.get()

    if not title:
        messagebox.showerror("Error", "Title is required")
        return

    owner_id = owner_dict.get(owner)
    cursor.execute("INSERT INTO games (title, genre, platform, release_year, owner_id) VALUES (%s, %s, %s, %s, %s)",
                   (title, genre, platform, year, owner_id))
    conn.commit()
    refresh_game_table()
    clear_entries()


def update_game():
    selected = game_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a game to update")
        return
    game_id = game_table.item(selected)['values'][0]
    title = title_entry.get()
    genre = genre_entry.get()
    platform = platform_entry.get()
    year = year_entry.get()
    owner = owner_combo.get()
    owner_id = owner_dict.get(owner)
    cursor.execute("UPDATE games SET title=%s, genre=%s, platform=%s, release_year=%s, owner_id=%s WHERE game_id=%s",
                   (title, genre, platform, year, owner_id, game_id))
    conn.commit()
    refresh_game_table()
    clear_entries()


def delete_game():
    selected = game_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a game to delete")
        return
    game_id = game_table.item(selected)['values'][0]
    cursor.execute("DELETE FROM games WHERE game_id=%s", (game_id,))
    conn.commit()
    refresh_game_table()
    clear_entries()


def on_game_select(event):
    selected = game_table.focus()
    if selected:
        values = game_table.item(selected)['values']
        title_entry.delete(0, tk.END)
        title_entry.insert(0, values[1])
        genre_entry.delete(0, tk.END)
        genre_entry.insert(0, values[2])
        platform_entry.delete(0, tk.END)
        platform_entry.insert(0, values[3])
        year_entry.delete(0, tk.END)
        year_entry.insert(0, values[4])
        owner_combo.set(values[5])


def clear_entries():
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    platform_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    owner_combo.set('')


# --- GUI setup ---
root = tk.Tk()
root.title("Game Collection Manager")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Form
form_frame = tk.Frame(root, bg="#f0f0f0")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Title:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky='e')
title_entry = tk.Entry(form_frame, width=30)
title_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Genre:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky='e')
genre_entry = tk.Entry(form_frame, width=30)
genre_entry.grid(row=1, column=1)

tk.Label(form_frame, text="Platform:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky='e')
platform_entry = tk.Entry(form_frame, width=30)
platform_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Release Year:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky='e')
year_entry = tk.Entry(form_frame, width=30)
year_entry.grid(row=3, column=1)

# Owner dropdown
tk.Label(form_frame, text="Owner:", bg="#f0f0f0").grid(row=4, column=0, padx=5, pady=5, sticky='e')
owners = fetch_owners()
owner_dict = {name: oid for oid, name, _ in owners}
owner_combo = ttk.Combobox(form_frame, values=list(owner_dict.keys()), state='readonly', width=28)
owner_combo.grid(row=4, column=1)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Game", command=add_game, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update Game", command=update_game, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete Game", command=delete_game, width=15, bg="#f44336", fg="white").grid(row=0, column=2, padx=10)

# Table
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

cols = ("ID", "Title", "Genre", "Platform", "Year", "Owner")
game_table = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
for col in cols:
    game_table.heading(col, text=col)
    game_table.column(col, anchor="center")
game_table.pack()
game_table.bind("<ButtonRelease-1>", on_game_select)

refresh_game_table()
root.mainloop()
