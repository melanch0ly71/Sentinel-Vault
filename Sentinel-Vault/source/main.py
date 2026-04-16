import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity.auth import AuthManager
from identity.database import IdentityDB
from core.processor import VaultProcessor

class SentinelUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sentinel Vault")
        self.geometry("400x500")
        self.auth = AuthManager()
        ctk.set_appearance_mode("dark")
        
        self.label = ctk.CTkLabel(self, 
                                text="Sentinel Vault", 
                                font=("Times New Roman", 24, "bold"), 
                                text_color="#2EB086") # A clean emerald green
        self.label.pack(pady=40)

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self,placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", width=200, command=self.handle_login).pack(pady=10)
        ctk.CTkButton(self, text="Register", width=200, fg_color="transparent", border_width=2, command=self.handle_register).pack(pady=10)

    def handle_login(self):
        u, p = self.user_entry.get(), self.pass_entry.get()
        if self.auth.verify_user(u, p): self.show_controls(p)
        else: messagebox.showerror("Error", "Invalid Login")

    def handle_register(self):
        u, p = self.user_entry.get(), self.pass_entry.get()
        if self.auth.register_user(u, p): messagebox.showinfo("Success", "Registered")
        else: messagebox.showerror("Error", "Failed")

    def show_controls(self, pwd):
        for w in self.winfo_children(): w.destroy()
        ctk.CTkLabel(self, text="Vault Controls", font=("Roboto", 20)).pack(pady=40)
        ctk.CTkButton(self, text="LOCK FOLDER", width=250, command=lambda: self.lock(pwd)).pack(pady=15)
        ctk.CTkButton(self, text="UNLOCK VAULT", width=250, command=lambda: self.unlock(pwd)).pack(pady=15)

    def lock(self, pwd):
        folder = filedialog.askdirectory()
        if folder:
            try:
                VaultProcessor.pack_and_encrypt_folder(folder, folder + ".sentinel", pwd)
                messagebox.showinfo("Success", "Folder Locked!")
            except Exception as e: messagebox.showerror("Error", str(e))

    def unlock(self, pwd):
        file = filedialog.askopenfilename(filetypes=[("Sentinel", "*.sentinel")])
        if file:
            dest = filedialog.askdirectory()
            if dest:
                try:
                    VaultProcessor.decrypt_and_unpack_payload(file, dest, pwd)
                    messagebox.showinfo("Success", "Folder Restored!")
                except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    if not os.path.exists('logs'): os.makedirs('logs')
    IdentityDB()
    SentinelUI().mainloop()