"""
GDPR Consent Module
Handles user consent for data collection
File: consent.py
"""

import tkinter as tk
from tkinter import messagebox


class ConsentManager:
    """Manages GDPR-compliant consent for data collection"""

    def show_consent_dialog(self, parent):
        """Display GDPR consent dialog with mandatory checkboxes"""
        dialog = tk.Toplevel(parent)
        dialog.title("Privacy & Consent Agreement")
        dialog.geometry("700x600")
        dialog.configure(bg="#1e1e2e")
        dialog.transient(parent)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")

        # Header
        tk.Label(
            dialog,
            text="📋 Privacy & Consent Agreement",
            font=("Arial", 20, "bold"),
            bg="#1e1e2e",
            fg="#00ff88",
        ).pack(pady=20)

        # ===== Scrollable info text area =====
        info_container = tk.Frame(dialog, bg="#1e1e2e")
        info_container.pack(fill="both", expand=False, padx=30, pady=(0, 10))

        canvas = tk.Canvas(
            info_container,
            bg="#1e1e2e",
            highlightthickness=0,
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            info_container,
            orient="vertical",
            command=canvas.yview,
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        text_frame = tk.Frame(canvas, bg="#1e1e2e")
        canvas.create_window((0, 0), window=text_frame, anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        text_frame.bind("<Configure>", _on_configure)

        # Information text
        info_text = """
Welcome to Personal-Aware Password Security Advisor!

This educational tool helps you understand password security by analyzing 
your passwords against your personal information. To provide this service, 
we need to collect and store some personal data.

WHAT WE COLLECT:
- Personal information (name, date of birth, contact details)
- Social media handles and usernames
- Favorite words and common phrases you use

HOW WE USE YOUR DATA:
- Generate personalized security analysis
- Demonstrate dictionary attack patterns
- Create strong password recommendations
- Educational demonstration purposes ONLY

YOUR RIGHTS & GUARANTEES:
✓ All data is encrypted with AES-128-CBC + HMAC
✓ Protected by PBKDF2 (100,000 iterations)
✓ Data stored ONLY on your local device
✓ No cloud synchronization or transmission
✓ You can delete your data at any time
✓ This is an educational prototype, not production software

IMPORTANT DISCLAIMER:
This is a B.Tech cybersecurity mini-project for educational purposes. 
While we implement industry-standard encryption, this is NOT intended 
for storing real sensitive passwords or data.
        """

        tk.Label(
            text_frame,
            text=info_text,
            font=("Arial", 10),
            bg="#1e1e2e",
            fg="white",
            justify="left",
            wraplength=620,
        ).pack(pady=10)

        # ===== Consent checkboxes frame =====
        checkbox_frame = tk.Frame(dialog, bg="#2d2d44", relief="ridge", bd=2)
        checkbox_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            checkbox_frame,
            text="Please read and accept all terms:",
            font=("Arial", 11, "bold"),
            bg="#2d2d44",
            fg="#00ff88",
        ).pack(pady=10)

        # Checkbox variables
        consent_vars = []
        consent_texts = [
            "I consent to the collection of my personal information for security analysis",
            "I consent to the analysis of my social media handles and usernames",
            "I understand that my data will be stored ONLY on this device",
            "I understand this is for educational demonstration purposes ONLY",
        ]

        for text in consent_texts:
            var = tk.BooleanVar()
            consent_vars.append(var)

            cb = tk.Checkbutton(
                checkbox_frame,
                text=text,
                variable=var,
                font=("Arial", 10),
                bg="#2d2d44",
                fg="white",
                selectcolor="#1e1e2e",
                activebackground="#2d2d44",
                activeforeground="white",
                wraplength=700,
                justify="left",
            )
            cb.pack(anchor="w", padx=20, pady=5)

        # ===== Button frame =====
        btn_frame = tk.Frame(dialog, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        result = [False]  # Mutable container for result

        def accept():
            """Handle accept button click"""
            if all(var.get() for var in consent_vars):
                result[0] = True
                dialog.destroy()
            else:
                messagebox.showwarning(
                    "Incomplete",
                    "You must accept all terms to continue.\n\n"
                    "This is required for GDPR compliance.",
                )

        def decline():
            """Handle decline button click"""
            result[0] = False
            dialog.destroy()

        tk.Button(
            btn_frame,
            text="✓ Accept All & Continue",
            font=("Arial", 12, "bold"),
            bg="#00ff88",
            fg="black",
            width=20,
            command=accept,
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="✗ Decline",
            font=("Arial", 12, "bold"),
            bg="#ff4444",
            fg="white",
            width=15,
            command=decline,
        ).pack(side="left", padx=10)

        # Wait for dialog to close
        parent.wait_window(dialog)

        return result[0]
