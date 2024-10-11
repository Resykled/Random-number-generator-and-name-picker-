import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os

# Hauptfenster erstellen
root = tk.Tk()
root.title("Zufallsgenerator")
root.geometry("600x700")  # Fenstergröße vergrößern

# Dateipfade für die Speicherung der Namen und Blacklist
names_file_path = "names_list.txt"
blacklist_file_path = "blacklist.txt"

# Funktion zum Laden der Namen aus einer Datei
def load_names():
    if os.path.exists(names_file_path):
        with open(names_file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

# Funktion zum Speichern der Namen in eine Datei
def save_names():
    with open(names_file_path, "w") as file:
        for name in names_list:
            file.write(name + "\n")

# Funktion zum Laden der Blacklist aus einer Datei
def load_blacklist():
    if os.path.exists(blacklist_file_path):
        with open(blacklist_file_path, "r") as file:
            return set(line.strip() for line in file.readlines())
    return set()

# Funktion zum Speichern der Blacklist in eine Datei
def save_blacklist():
    with open(blacklist_file_path, "w") as file:
        for name in blacklist:
            file.write(name + "\n")

# Variablen für Namens- und Zahlengenerator
names_list = load_names()
blacklist = load_blacklist()

# Funktion für das Hauptmenü
def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    def open_name_generator():
        for widget in root.winfo_children():
            widget.destroy()
        name_generator()

    def open_number_generator():
        for widget in root.winfo_children():
            widget.destroy()
        number_generator()

    tk.Label(root, text="Wählen Sie eine Funktion:", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(root, text="Namensgenerator", command=open_name_generator, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Zahlengenerator", command=open_number_generator, font=("Helvetica", 14)).pack(pady=10)

# GUI-Komponenten für den Namensgenerator
def name_generator():
    def back_to_menu():
        main_menu()

    def generate_name():
        available_names = [name for name in names_list if name not in blacklist]
        if not available_names:
            messagebox.showinfo("Info", "Keine Namen mehr verfügbar.")
            return
        selected_name = random.choice(available_names)
        blacklist.add(selected_name)
        save_blacklist()
        messagebox.showinfo("Zufälliger Name", f"Name: {selected_name}")
        update_name_display()

    def reset_names():
        blacklist.clear()
        save_blacklist()
        messagebox.showinfo("Reset", "Die Liste wurde zurückgesetzt.")
        update_name_display()

    def save_new_names():
        new_names = text_names.get("1.0", tk.END).strip().split("\n")
        global names_list
        names_list = [name.strip() for name in new_names if name.strip()]
        save_names()
        messagebox.showinfo("Gespeichert", "Die Namen wurden gespeichert.")
        update_name_display()

    def load_existing_names():
        text_names.delete("1.0", tk.END)
        text_names.insert(tk.END, "\n".join(names_list))

    def update_name_display():
        listbox_names.delete(0, tk.END)
        for name in names_list:
            if name in blacklist:
                listbox_names.insert(tk.END, name + " (verwendet)")
            else:
                listbox_names.insert(tk.END, name)

    tk.Button(root, text="Menü", command=back_to_menu, font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="w")
    tk.Label(root, text="Geben Sie die Namen ein (jeder Name in einer neuen Zeile):", font=("Helvetica", 14)).grid(row=1, column=0, columnspan=2, pady=10)
    text_names = tk.Text(root, height=15, width=40, font=("Helvetica", 12))
    text_names.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    load_existing_names()

    tk.Button(root, text="Namen speichern", command=save_new_names, font=("Helvetica", 12)).grid(row=3, column=0, pady=10)
    tk.Button(root, text="Name generieren", command=generate_name, font=("Helvetica", 12)).grid(row=3, column=1, pady=10)
    tk.Button(root, text="Namen zurücksetzen", command=reset_names, font=("Helvetica", 12)).grid(row=4, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Aktuelle Namensliste:", font=("Helvetica", 14)).grid(row=5, column=0, columnspan=2, pady=10)
    listbox_names = tk.Listbox(root, height=15, width=50, font=("Helvetica", 12))
    listbox_names.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    update_name_display()

# GUI-Komponenten für den Zahlengenerator
def number_generator():
    def back_to_menu():
        main_menu()

    def generate_number():
        try:
            min_value = int(entry_min.get())
            max_value = int(entry_max.get())
            ignored_numbers = set(map(int, entry_ignore.get().split(',')))
            random_number = random.randint(min_value, max_value)
            while random_number in ignored_numbers:
                random_number = random.randint(min_value, max_value)
            messagebox.showinfo("Zufällige Zahl", f"Zahl: {random_number}")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gültige Zahlen eingeben.")

    tk.Button(root, text="Menü", command=back_to_menu, font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="w")
    tk.Label(root, text="Min Wert:", font=("Helvetica", 14)).grid(row=1, column=0, sticky="e", pady=10)
    entry_min = tk.Entry(root, font=("Helvetica", 12))
    entry_min.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Max Wert:", font=("Helvetica", 14)).grid(row=2, column=0, sticky="e", pady=10)
    entry_max = tk.Entry(root, font=("Helvetica", 12))
    entry_max.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Zahlen ignorieren (Komma getrennt):", font=("Helvetica", 14)).grid(row=3, column=0, sticky="e", pady=10)
    entry_ignore = tk.Entry(root, font=("Helvetica", 12))
    entry_ignore.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(root, text="Zahl generieren", command=generate_number, font=("Helvetica", 12)).grid(row=4, column=0, columnspan=2, pady=20)

# Starte das Hauptmenü
main_menu()
root.mainloop()