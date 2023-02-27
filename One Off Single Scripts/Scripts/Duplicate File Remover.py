import os
import hashlib
import tkinter as tk
from tkinter import filedialog

class DuplicateFileRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Remover")
        self.root.geometry("500x200")
        self.label1 = tk.Label(self.root, text="Select a folder to remove duplicates from:")
        self.label1.pack(pady=10)
        self.btn1 = tk.Button(self.root, text="Browse", command=self.browse_directory)
        self.btn1.pack(pady=10)
        self.btn2 = tk.Button(self.root, text="Remove Duplicates", command=self.remove_duplicates)
        self.btn2.pack(pady=10)

    def browse_directory(self):
        self.folder_path = filedialog.askdirectory()
        self.label1.config(text="Folder selected: " + self.folder_path)

    def get_file_hash(self, file_path):
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def remove_duplicates(self):
        if not hasattr(self, "folder_path"):
            return
        hash_dict = {}
        for dirpath, _, filenames in os.walk(self.folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_hash = self.get_file_hash(file_path)
                if file_hash in hash_dict:
                    os.remove(file_path)
                else:
                    hash_dict[file_hash] = file_path

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFileRemover(root)
    root.mainloop()
