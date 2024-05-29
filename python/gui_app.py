import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry

# Function to open a file dialog
def browse_file(entry_widget):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

# Function to open a directory dialog
def browse_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

# Function to handle the submit button click
def submit():
    source_file = source_file_entry.get()
    output_dir = output_dir_entry.get()
    date = date_entry.get()
    backup_immediately = backup_var.get()

    if not source_file or not output_dir or (not date and not backup_immediately):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    backup_status = "Yes" if backup_immediately else "No"
    messagebox.showinfo("Information", f"Source File: {source_file}\nOutput Directory: {output_dir}\nDate: {date}\nBackup Immediately: {backup_status}")

# Function to toggle date entry based on checkbox state
def toggle_date_entry():
    if backup_var.get():
        date_entry.config(state='disabled')
    else:
        date_entry.config(state='normal')

# Create the main application window
root = tk.Tk()
root.title("File and Directory Input App")
root.geometry("400x350")  # Set the size of the window

# Source file input
source_file_label = tk.Label(root, text="Source File:")
source_file_label.pack(pady=5)
source_file_entry = tk.Entry(root, width=50)
source_file_entry.pack(pady=5)
source_file_browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(source_file_entry))
source_file_browse_button.pack(pady=5)

# Output directory input
output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.pack(pady=5)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.pack(pady=5)
output_dir_browse_button = tk.Button(root, text="Browse", command=lambda: browse_directory(output_dir_entry))
output_dir_browse_button.pack(pady=5)

# Date input
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.pack(pady=5)
date_entry = DateEntry(root, width=47, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=5)

# Backup immediately checkbox
backup_var = tk.IntVar()
backup_checkbox = tk.Checkbutton(root, text="Backup immediately", variable=backup_var, command=toggle_date_entry)
backup_checkbox.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=20)

# Run the main event loop
root.mainloop()
