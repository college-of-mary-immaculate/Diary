import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime

class DiaryEntry:
    def __init__(self, date, time, entry):
        self.date = date
        self.time = time
        self.entry = entry

def insertion_sort(entries):
    for i in range(1, len(entries)):
        key = entries[i]
        j = i - 1
        while j >= 0 and (entries[j].date > key.date or (entries[j].date == key.date and entries[j].time > key.time)):
            entries[j + 1] = entries[j]
            j -= 1
        entries[j + 1] = key

def add_entry(diary, entry):
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    diary.append(DiaryEntry(today_date, current_time, entry))
    insertion_sort(diary)

def save_entry(diary, entry_text):
    if entry_text.strip():
        add_entry(diary, entry_text)
        now = datetime.now()
        with open("diary.txt", "a") as f:
            f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')}\n{entry_text}\n")
        messagebox.showinfo("Success", "Entry saved successfully!")
    else:
        messagebox.showwarning("Warning", "Diary entry is empty!")

def view_entry(entry_content):
    entry_window = tk.Toplevel()
    entry_window.title("DIARY")
    entry_window.geometry("700x500")
    entry_window.resizable(False, False)

    clouds_image = tk.PhotoImage(file="clouds.png")
    clouds_label = tk.Label(entry_window, image=clouds_image)
    clouds_label.place(relx=0.5, rely=0.5, anchor="center")
    clouds_label.image = clouds_image

    entry_text = tk.Text(entry_window, height=20, width=80)
    entry_text.place(relx=0.5, rely=0.5, anchor="center")
    entry_text.insert("1.0", entry_content)
    entry_text.config(state=tk.DISABLED)

def display_entries(diary):
    entries_window = tk.Toplevel()
    entries_window.title("DIARY")
    entries_window.geometry("700x500")
    entries_window.resizable(False, False)

    clouds_image = tk.PhotoImage(file="clouds.png")
    clouds_label = tk.Label(entries_window, image=clouds_image)
    clouds_label.place(relx=0.5, rely=0.5, anchor="center")
    clouds_label.image = clouds_image

    frame = tk.Frame(entries_window, bg="light blue")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox = tk.Listbox(frame, bg="light blue", font="15")
    listbox.pack(fill=tk.BOTH, expand=True)

    for entry in diary:
        listbox.insert(tk.END, f"{entry.date} {entry.time}")
        listbox.insert(tk.END, "-" * 50)

    def on_listbox_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            entry_index = selected_index[0] // 2
            selected_entry = diary[entry_index]
            view_entry(selected_entry.entry)

    listbox.bind('<<ListboxSelect>>', on_listbox_select)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DIARY")
        self.geometry("700x500")
        self.resizable(False, False)
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Lucida Calligraphy", size=20)
        self.diary = []
        self.password_entry = None
        self.__show_first_window()

    def __show_first_window(self):
        clouds_image = tk.PhotoImage(file="clouds.png")
        clouds_label = tk.Label(image=clouds_image)
        clouds_label.place(relx=0.5, rely=0.5, anchor="center")
        clouds_image.image = clouds_image

        first_window_label = tk.Label(text="A leap of faith", fg="purple", bg="light pink")
        first_window_label.place(relx=0.5, rely=0.2, anchor="center")

        first_window_label = tk.Label(text="can take you somewhere.", fg="purple", bg="light pink")
        first_window_label.place(relx=0.5, rely=0.3, anchor="center")

        entry_var = tk.StringVar()
        self.password_entry = tk.Entry(textvariable=entry_var, font=("Sans Serif", 20), fg="black", bg="white", show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        login_button = tk.Button(text="Log In", font="15", fg="black", background="light blue", command=self.__login)
        login_button.place(relx=0.4, rely=0.6, anchor="center")

        create_password_button = tk.Button(text="New password", font="15", fg="black", background="pink", command=self.__create_password_window)
        create_password_button.place(relx=0.6, rely=0.6, anchor="center")

    def __login(self):
        password = self.password_entry.get()
        try:
            with open("password.txt", "r") as f:
                saved_password = f.read().strip()
            if password == saved_password:
                messagebox.showinfo("Result", "Welcome!")
                self.__show_diary_window()
            else:
                messagebox.showinfo("Result", "Oops! Wrong password.")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No password set. Please create a new password.")

    def __create_password_window(self):
        password_window = tk.Toplevel()
        password_window.title("Create New")
        password_window.geometry("400x300")
        password_window.resizable(False, False)

        create_password_label = tk.Label(password_window, text="Please type your desired password.", font="15", fg="black")
        create_password_label.place(relx=0.5, rely=0.3, anchor="center")

        password_entry_var = tk.StringVar()
        password_entry = tk.Entry(password_window, textvariable=password_entry_var, font=("Sans Serif", 15), bg="white")
        password_entry.place(relx=0.5, rely=0.5, anchor="center")

        def __save_new_password():
            new_password = password_entry_var.get()
            if new_password:
                with open("password.txt", "w") as f:
                    f.write(new_password)
                messagebox.showinfo("Success", "Password created successfully!")
                password_window.destroy()
                self.__show_first_window()
            else:
                messagebox.showwarning("Warning", "Password cannot be empty!")

        save_button = tk.Button(password_window, text="SAVE", font=("Sans Serif", 15), fg="black", bg="white", command=__save_new_password)
        save_button.place(relx=0.5, rely=0.7, anchor="center")

    def __show_diary_window(self):
        self.title("DIARY")
        self.geometry("700x500")
        self.resizable(False, False)
        self.__add_diary_elements()

    def __add_diary_elements(self):
        self.clouds_image = tk.PhotoImage(file="clouds.png")
        self.clouds_label = tk.Label(self, image=self.clouds_image)
        self.clouds_label.place(relx=0.5, rely=0.5, anchor="center")

        frame = tk.Frame(self, background="light blue")
        frame.pack(padx=10, pady=10)

        label = tk.Label(frame, text="Today's Entry:", bg="light blue")
        label.pack()

        self.entry_text = tk.Text(frame, height=17, width=80)
        self.entry_text.pack()

        save_button = tk.Button(frame, text="Save Entry", font="15", height="0", width="15", bg="light pink", command=self.save_entry)
        save_button.pack(pady=5)

        clear_button = tk.Button(frame, text="Clear Entry", font="15", height="0", width="15",bg="light pink", command=lambda: self.entry_text.delete("1.0", "end"))
        clear_button.pack(pady=5)

        show_entries_button = tk.Button(frame, text="Show Entries", font="15", height="0", width="15", bg="light pink", command=lambda: display_entries(self.diary))
        show_entries_button.pack(pady=5)

    def save_entry(self):
        entry_text = self.entry_text.get("1.0", "end-1c")
        save_entry(self.diary, entry_text)
        self.entry_text.delete("1.0", "end")

if __name__ == '__main__':
    app = App()
    app.mainloop()