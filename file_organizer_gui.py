import os
import shutil
import sys  # New import for path handling
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser # New import to open web links

# A dictionary to map file extensions to folder names.
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'Videos': ['.mp4', '.mkv', '.mov', '.avi'],
    'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
    'Archives': ['.zip', '.rar'],
    'Audio': ['.mp3', '.wav'],
}

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file, whether running
    as a script or as a PyInstaller-packaged executable.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If not running as a bundled executable, use the script's directory
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def organize_files(source_path, status_label):
    """
    Organizes files in the specified directory into subfolders based on file type.
    This version updates a GUI label instead of printing to the console.
    """
    try:
        if not os.path.isdir(source_path):
            messagebox.showerror("Error", "The specified path is not a valid directory.")
            return

        status_label.config(text="Starting to organize files...")
        root.update_idletasks() # Force GUI to update

        for filename in os.listdir(source_path):
            # Skip directories to avoid errors.
            full_path = os.path.join(source_path, filename)
            if os.path.isdir(full_path):
                continue

            file_extension = os.path.splitext(filename)[1].lower()
            
            found = False
            for folder, extensions in file_types.items():
                if file_extension in extensions:
                    destination_folder = os.path.join(source_path, folder)
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    
                    shutil.move(full_path, destination_folder)
                    status_label.config(text=f"Moved '{filename}' to '{folder}'")
                    root.update_idletasks()
                    found = True
                    break
            
            if not found:
                other_folder = os.path.join(source_path, 'Others')
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(full_path, other_folder)
                status_label.config(text=f"Moved '{filename}' to 'Others'")
                root.update_idletasks()

        status_label.config(text="File organization complete!")
        messagebox.showinfo("Success", "File organization complete!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="An error occurred.")


def browse_for_folder():
    """Opens a file dialog to let the user select a folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)


def run_organizer():
    """Gets the path from the entry field and starts the organizing process."""
    source_path = path_entry.get()
    if source_path:
        organize_files(source_path, status_label)
    else:
        messagebox.showwarning("Warning", "Please select a folder to organize.")

def open_github_profile(event):
    """Function to open the GitHub profile link."""
    webbrowser.open_new("https://github.com/salmanrahman7")

# --- GUI Setup ---
if __name__ == '__main__':
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("450x250") # Increased window height to accommodate new labels
    root.resizable(False, False)
    
    # Set the custom icon for the window.
    # This uses a helper function to find the file even when it's packaged.
    try:
        icon = tk.PhotoImage(file=get_resource_path('organizer.png'))
        root.iconphoto(False, icon)
    except tk.TclError:
        # If the icon file is not found or there's an error, just continue without an icon.
        pass

    # Main frame for padding
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Path entry and label
    path_label = tk.Label(main_frame, text="Folder Path:", font=("Arial", 10))
    path_label.pack(anchor="w")

    path_frame = tk.Frame(main_frame)
    path_frame.pack(fill="x", pady=(0, 10))

    path_entry = tk.Entry(path_frame, width=40, font=("Arial", 10))
    path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    browse_button = tk.Button(path_frame, text="Browse", command=browse_for_folder, font=("Arial", 10))
    browse_button.pack(side="left")

    # Organize button
    organize_button = tk.Button(main_frame, text="Organize Files", command=run_organizer, font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049")
    organize_button.pack(fill="x", pady=(10, 5))

    def on_enter(event):
        organize_button.config(bg="#3e8e41") # A slightly darker shade of green

    def on_leave(event):
        organize_button.config(bg="#4CAF50") # Revert to original color

    organize_button.bind("<Enter>", on_enter)
    organize_button.bind("<Leave>", on_leave)

    # Status label for feedback
    status_label = tk.Label(main_frame, text="", fg="dark green", font=("Arial", 10))
    status_label.pack(pady=(5, 0))

    # --- New Labels for GitHub and Copyright ---
    # GitHub Profile Link
    github_label = tk.Label(main_frame, text="Developed by @salmanrahman7", fg="blue", cursor="hand2")
    github_label.pack(pady=(5, 0))
    github_label.bind("<Button-1>", open_github_profile)

    # Copyright Notice
    copyright_label = tk.Label(main_frame, text="© 2025 Salmanur Rahman. All rights reserved.", font=("Arial", 8))
    copyright_label.pack(pady=(0, 5))
    
    root.mainloop()
