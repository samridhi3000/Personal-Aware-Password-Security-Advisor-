"""
Personal Data Collection Module
Collects and processes user's personal information
File: personal.py
"""

import tkinter as tk
from tkinter import messagebox
import re


class PersonalDataManager:
    """Manages collection and processing of personal information"""
    
    def collect_personal_data(self, parent):
        """Collect personal information from user through GUI form"""
        dialog = tk.Toplevel(parent)
        dialog.title("Personal Information Collection")
        dialog.geometry("800x700")
        dialog.configure(bg="#1e1e2e")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"800x700+{x}+{y}")
        
        # Create scrollable frame
        canvas = tk.Canvas(dialog, bg="#1e1e2e", highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        tk.Label(scrollable_frame, text="👤 Personal Information", 
                font=("Arial", 20, "bold"),
                bg="#1e1e2e", fg="#00ff88").pack(pady=20)
        
        tk.Label(scrollable_frame, 
                text="This information will be used to analyze password security.\n" + 
                     "All data is encrypted and stored only on your device.",
                font=("Arial", 10),
                bg="#1e1e2e", fg="#888").pack(pady=5)
        
        # Form fields
        entries = {}
        
        def create_field(label_text, field_name, is_required=True):
            """Create a form field with label and entry"""
            frame = tk.Frame(scrollable_frame, bg="#1e1e2e")
            frame.pack(fill="x", padx=50, pady=8)
            
            label = label_text + (" *" if is_required else " (optional)")
            tk.Label(frame, text=label, font=("Arial", 11),
                    bg="#1e1e2e", fg="white", width=20, 
                    anchor="w").pack(side="left")
            
            entry = tk.Entry(frame, font=("Arial", 11), width=40)
            entry.pack(side="left", padx=10)
            entries[field_name] = entry
            
            return entry
        
        # Basic Information
        tk.Label(scrollable_frame, text="━" * 70, 
                bg="#1e1e2e", fg="#444").pack(pady=10)
        tk.Label(scrollable_frame, text="Basic Information", 
                font=("Arial", 12, "bold"),
                bg="#1e1e2e", fg="#00ff88").pack(pady=5)
        
        create_field("Full Name:", "full_name")
        create_field("Nickname:", "nickname", False)
        create_field("Date of Birth (DD/MM/YYYY):", "dob")
        create_field("Phone Number:", "phone")
        create_field("Email Address:", "email")
        
        # Social Media
        tk.Label(scrollable_frame, text="━" * 70, 
                bg="#1e1e2e", fg="#444").pack(pady=10)
        tk.Label(scrollable_frame, text="Social Media Handles", 
                font=("Arial", 12, "bold"),
                bg="#1e1e2e", fg="#00ff88").pack(pady=5)
        
        create_field("Instagram (@username):", "instagram", False)
        create_field("Twitter/X (@username):", "twitter", False)
        create_field("Facebook (name):", "facebook", False)
        
        # Additional Info
        tk.Label(scrollable_frame, text="━" * 70, 
                bg="#1e1e2e", fg="#444").pack(pady=10)
        tk.Label(scrollable_frame, text="Additional Information", 
                font=("Arial", 12, "bold"),
                bg="#1e1e2e", fg="#00ff88").pack(pady=5)
        
        create_field("College/University:", "college", False)
        create_field("City:", "city", False)
        create_field("Favorite Word 1:", "fav_word1", False)
        create_field("Favorite Word 2:", "fav_word2", False)
        create_field("Favorite Word 3:", "fav_word3", False)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom buttons
        btn_frame = tk.Frame(dialog, bg="#2d2d44", height=60)
        btn_frame.pack(side="bottom", fill="x")
        
        result = [None]
        
        def submit():
            """Validate and submit form data"""
            data = {}
            
            # Validate required fields
            required = ["full_name", "dob", "phone", "email"]
            for field in required:
                value = entries[field].get().strip()
                if not value:
                    messagebox.showerror("Error", 
                                       f"Please fill in: {field.replace('_', ' ').title()}")
                    return
                data[field] = value
            
            # Validate DOB format
            if not re.match(r'\d{2}/\d{2}/\d{4}', data["dob"]):
                messagebox.showerror("Error", "Date of birth must be in DD/MM/YYYY format")
                return
            
            # Validate email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data["email"]):
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            # Collect optional fields
            optional = ["nickname", "instagram", "twitter", "facebook", 
                       "college", "city", "fav_word1", "fav_word2", "fav_word3"]
            for field in optional:
                data[field] = entries[field].get().strip()
            
            result[0] = data
            dialog.destroy()
        
        def cancel():
            """Cancel form submission"""
            result[0] = None
            dialog.destroy()
        
        tk.Button(btn_frame, text="💾 Save & Continue", 
                 font=("Arial", 12, "bold"),
                 bg="#00ff88", fg="black", width=20,
                 command=submit).pack(side="left", padx=20, pady=10)
        
        tk.Button(btn_frame, text="Cancel", 
                 font=("Arial", 12),
                 bg="#ff4444", fg="white", width=12,
                 command=cancel).pack(side="right", padx=20, pady=10)
        
        parent.wait_window(dialog)
        return result[0]
    
    def extract_keywords(self, user_data):
        """Extract keywords from personal data for password analysis"""
        if not user_data:
            return []
        
        keywords = []
        
        # Extract from name
        if user_data.get("full_name"):
            name_parts = user_data["full_name"].lower().split()
            keywords.extend(name_parts)
        
        if user_data.get("nickname"):
            keywords.append(user_data["nickname"].lower())
        
        # Extract from DOB
        if user_data.get("dob"):
            dob = user_data["dob"]
            parts = dob.split("/")
            if len(parts) == 3:
                day, month, year = parts
                keywords.extend([day, month, year, day+month, month+year, 
                               day+month+year, year[-2:]])
        
        # Extract from phone
        if user_data.get("phone"):
            phone = re.sub(r'\D', '', user_data["phone"])
            keywords.append(phone)
            if len(phone) >= 4:
                keywords.append(phone[-4:])
                keywords.append(phone[:4])
        
        # Extract from social media
        for field in ["instagram", "twitter", "facebook"]:
            if user_data.get(field):
                handle = user_data[field].replace("@", "").lower()
                keywords.append(handle)
        
        # Extract from other fields
        for field in ["college", "city", "fav_word1", "fav_word2", "fav_word3"]:
            if user_data.get(field):
                keywords.append(user_data[field].lower())
        
        # Remove duplicates and empty strings
        keywords = list(set([k for k in keywords if k]))
        
        return keywords