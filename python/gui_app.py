import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import subprocess
import os
import getpass

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
    try:
        source_file = source_file_entry.get()
        output_dir = output_dir_entry.get()
        date = date_entry.get()
        backup_type = backup_type_var.get()
        backup_frequency = frequency_var.get()

        if not source_file or not output_dir or (backup_type == "date" and not date):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        bash_script_path = os.path.join(os.path.dirname(__file__), '..', 'bash', 'backup.sh')
        user = getpass.getuser()

        # Determine the date/frequency for the backup
        if backup_type == "now":
            date = "now"
            try:
                # Execute the bash script immediately
                subprocess.run([bash_script_path, source_file, output_dir, date], check=True)
                messagebox.showinfo("Success", "Backup successfully realized.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to perform immediate backup: {e}")

        else:
            # Schedule the cron job based on the frequency
            if backup_type == "interval":
                cron_schedule = ""
                if backup_frequency == "Daily":
                    cron_schedule = "0 0 * * *"
                elif backup_frequency == "Weekly":
                    cron_schedule = "0 0 * * 1"
                elif backup_frequency == "Monthly":
                    cron_schedule = "0 0 1 * *"
            elif backup_type == "date":
                date_parts = date.split('-')
                cron_schedule = f"0 0 {date_parts[2]} {date_parts[1]} *"

            cron_job = f"{cron_schedule} {bash_script_path} {source_file} {output_dir} {date}"
            cron_command = f"(crontab -l 2>/dev/null; echo \"{cron_job}\") | crontab -"

            try:
                subprocess.run(cron_command, shell=True, check=True, user=user)
                messagebox.showinfo("Success", "Backup operation scheduled.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to schedule backup: {e}")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to enable/disable inputs based on the selected backup type
def update_inputs():
    backup_type = backup_type_var.get()
    if backup_type == "now":
        date_entry.config(state='disabled')
        frequency_daily_button.config(state='disabled')
        frequency_weekly_button.config(state='disabled')
        frequency_monthly_button.config(state='disabled')
    elif backup_type == "interval":
        date_entry.config(state='disabled')
        frequency_daily_button.config(state='normal')
        frequency_weekly_button.config(state='normal')
        frequency_monthly_button.config(state='normal')
    elif backup_type == "date":
        date_entry.config(state='normal')
        frequency_daily_button.config(state='disabled')
        frequency_weekly_button.config(state='disabled')
        frequency_monthly_button.config(state='disabled')

# Create the main application window
root = tk.Tk()
root.title("File and Directory Input App")

# Set the size of the window to 800x800
root.geometry("800x800")

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

# Backup type radio buttons
backup_type_label = tk.Label(root, text="Backup Type:")
backup_type_label.pack(pady=5)
backup_type_var = tk.StringVar(value="now")  # Default value

backup_now_button = tk.Radiobutton(root, text="Backup Immediately", variable=backup_type_var, value="now", command=update_inputs)
backup_now_button.pack(pady=5)

backup_interval_button = tk.Radiobutton(root, text="Backup at Interval", variable=backup_type_var, value="interval", command=update_inputs)
backup_interval_button.pack(pady=5)

backup_date_button = tk.Radiobutton(root, text="Backup at Specific Date", variable=backup_type_var, value="date", command=update_inputs)
backup_date_button.pack(pady=5)

# Date input
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.pack(pady=5)
date_entry = DateEntry(root, width=47, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=5)

# Backup frequency radio buttons (for interval backups)
frequency_label = tk.Label(root, text="Backup Frequency:")
frequency_label.pack(pady=5)
frequency_var = tk.StringVar(value="Daily")  # Default value
frequency_daily_button = tk.Radiobutton(root, text="Daily", variable=frequency_var, value="Daily")
frequency_daily_button.pack(pady=5)
frequency_weekly_button = tk.Radiobutton(root, text="Weekly", variable=frequency_var, value="Weekly")
frequency_weekly_button.pack(pady=5)
frequency_monthly_button = tk.Radiobutton(root, text="Monthly", variable=frequency_var, value="Monthly")
frequency_monthly_button.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=20)

# Initialize input states
update_inputs()

# Run the main event loop
root.mainloop()
