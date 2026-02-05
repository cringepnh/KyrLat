# -*- coding: utf-8 -*-
"""
KyrLat - Uzbek Cyrillic ↔ Latin Transliterator

A simple GUI application for transliterating text between
Uzbek Cyrillic and Latin scripts.

Author: KyrLat Project
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from transliterate import transliterate


# =============================================================================
# MODERN COLOR SCHEME (Light & Calm)
# =============================================================================

COLORS = {
    # Background colors
    'bg_primary': '#f8f9fa',      # Very light gray (main background)
    'bg_secondary': '#ffffff',    # Pure white
    'bg_input': '#ffffff',        # White input background
    'bg_output': '#f8f9fa',       # Very light gray output
    
    # Text colors
    'text_primary': '#212529',    # Dark gray (main text)
    'text_secondary': '#6c757d',  # Medium gray (secondary text)
    'text_accent': '#495057',     # Darker gray for output
    'text_label': '#343a40',      # Almost black for labels
    
    # Accent colors
    'accent': '#4a90e2',          # Soft blue
    'accent_hover': '#357abd',    # Darker blue on hover
    'border': '#dee2e6',          # Light gray border
    
    # Button colors
    'btn_bg': '#e9ecef',          # Light gray button background
    'btn_hover': '#dee2e6',       # Slightly darker on hover
    'btn_text': '#495057',        # Dark gray button text
}


class TransliteratorApp:
    """Main application class for the transliterator GUI."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.auto_detect_enabled = True
        self.setup_window()
        self.apply_styles()
        self.create_widgets()
        self.setup_live_transliteration()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title("KyrLat — Ўзбек транслитератори")
        self.root.geometry("750x620")
        self.root.minsize(600, 500)
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Set window icon
        try:
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller mode
                icon_path = os.path.join(sys._MEIPASS, "icon.ico")
            else:
                # Development mode
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Icon not found or not supported
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def get_resource_path(self, filename):
        """Get absolute path to resource, works for dev and PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    def apply_styles(self):
        """Apply modern styling to ttk widgets."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame styling
        style.configure(
            "TFrame",
            background=COLORS['bg_primary']
        )
        
        # Label styling
        style.configure(
            "TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_primary'],
            font=("Segoe UI", 10)
        )
        
        style.configure(
            "Title.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['accent'],  # Soft blue title
            font=("Segoe UI", 28, "bold")
        )
        
        style.configure(
            "Subtitle.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_secondary'],
            font=("Segoe UI", 11)
        )
        
        style.configure(
            "Header.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_label'],
            font=("Segoe UI", 10, "bold")
        )
        
        style.configure(
            "Counter.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_secondary'],
            font=("Segoe UI", 9)
        )
        
        style.configure(
            "Status.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['accent'],
            font=("Segoe UI", 9)
        )
        
        # Button styling
        style.configure(
            "Modern.TButton",
            background=COLORS['btn_bg'],
            foreground=COLORS['btn_text'],
            font=("Segoe UI", 10),
            padding=(16, 10),
            borderwidth=0
        )
        style.map(
            "Modern.TButton",
            background=[("active", COLORS['btn_hover'])],
            foreground=[("active", COLORS['accent'])]
        )
        
        # Combobox styling
        style.configure(
            "Modern.TCombobox",
            background=COLORS['bg_input'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['bg_input'],
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['bg_primary'],
            font=("Segoe UI", 10),
            padding=8
        )
        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", COLORS['bg_input'])],
            selectbackground=[("readonly", COLORS['accent'])]
        )
        
        # Checkbutton styling
        style.configure(
            "Modern.TCheckbutton",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_primary'],
            font=("Segoe UI", 10)
        )
        style.map(
            "Modern.TCheckbutton",
            background=[("active", COLORS['bg_primary'])]
        )
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for responsive layout
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Input area
        main_frame.rowconfigure(6, weight=1)  # Output area
        
        # === Title ===
        title_label = ttk.Label(
            main_frame,
            text="KyrLat",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 8))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Ўзбек кириллицаси ↔ лотин транслитератори",
            style="Subtitle.TLabel"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 25))
        
        # === Input Section ===
        input_header_frame = ttk.Frame(main_frame)
        input_header_frame.grid(row=2, column=0, sticky="ew", pady=(10, 8))
        
        input_label = ttk.Label(
            input_header_frame,
            text="Матнни киритинг",
            style="Header.TLabel"
        )
        input_label.pack(side=tk.LEFT)
        
        # Character counter
        self.char_count_label = ttk.Label(
            input_header_frame,
            text="0 белги",
            style="Counter.TLabel"
        )
        self.char_count_label.pack(side=tk.RIGHT)
        
        # Input text area with scrollbar
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = tk.Text(
            input_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            height=7,
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent'],
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['bg_input'],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent'],
            padx=12,
            pady=10
        )
        self.input_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        input_scrollbar = ttk.Scrollbar(
            input_frame,
            orient=tk.VERTICAL,
            command=self.input_text.yview
        )
        input_scrollbar.grid(row=0, column=1, sticky="ns")
        self.input_text.configure(yscrollcommand=input_scrollbar.set)
        
        # === Direction and Auto-detect Section ===
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, pady=12)
        
        # Direction selection with mapping
        direction_label = ttk.Label(
            action_frame,
            text="Йўналиш:",
            style="TLabel"
        )
        direction_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Internal mapping
        self.direction_map = {
            "Lotin → Кирилл": "lat_to_cyr",
            "Кирилл → Lotin": "cyr_to_lat"
        }
        self.direction_map_reverse = {v: k for k, v in self.direction_map.items()}
        
        self.direction_var = tk.StringVar(value="lat_to_cyr")
        self.direction_display_var = tk.StringVar(value="Lotin → Кирилл")
        
        direction_combo = ttk.Combobox(
            action_frame,
            textvariable=self.direction_display_var,
            values=list(self.direction_map.keys()),
            state="readonly",
            width=18,
            style="Modern.TCombobox"
        )
        direction_combo.pack(side=tk.LEFT, padx=(0, 25))
        
        # Bind to trigger transliteration on direction change
        def on_direction_change(event):
            # Sync internal value from display value
            display_value = self.direction_display_var.get()
            self.direction_var.set(self.direction_map[display_value])
            self.on_input_change()
        
        direction_combo.bind("<<ComboboxSelected>>", on_direction_change)
        
        # Auto-detect toggle
        self.auto_detect_var = tk.BooleanVar(value=True)
        auto_detect_check = ttk.Checkbutton(
            action_frame,
            text="Автоаниқлаш",
            variable=self.auto_detect_var,
            command=self.toggle_auto_detect,
            style="Modern.TCheckbutton"
        )
        auto_detect_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Detection status label
        self.detect_status_label = ttk.Label(
            action_frame,
            text="",
            style="Status.TLabel"
        )
        self.detect_status_label.pack(side=tk.LEFT)
        
        # === Output Section ===
        output_label = ttk.Label(
            main_frame,
            text="Натижа",
            style="Header.TLabel"
        )
        output_label.grid(row=5, column=0, sticky="nw", pady=(10, 8))
        
        # Output text area with scrollbar (read-only)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=6, column=0, sticky="nsew", pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(
            output_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            height=7,
            bg=COLORS['bg_output'],
            fg=COLORS['text_accent'],
            insertbackground=COLORS['accent'],
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['bg_input'],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent'],
            padx=12,
            pady=10,
            state=tk.DISABLED
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        output_scrollbar = ttk.Scrollbar(
            output_frame,
            orient=tk.VERTICAL,
            command=self.output_text.yview
        )
        output_scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=output_scrollbar.set)
        
        # === Bottom Buttons ===
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=7, column=0, pady=(10, 0))
        
        # Copy button
        copy_btn = ttk.Button(
            bottom_frame,
            text="📋 Нусха олиш",
            command=self.copy_to_clipboard,
            style="Modern.TButton",
            width=16
        )
        copy_btn.pack(side=tk.LEFT, padx=8)
        
        # Clear button
        clear_btn = ttk.Button(
            bottom_frame,
            text="✕ Тозалаш",
            command=self.clear_all,
            style="Modern.TButton",
            width=16
        )
        clear_btn.pack(side=tk.LEFT, padx=8)
        
        # Swap button
        swap_btn = ttk.Button(
            bottom_frame,
            text="⇅ Алмаштириш",
            command=self.swap_text,
            style="Modern.TButton",
            width=16
        )
        swap_btn.pack(side=tk.LEFT, padx=8)
    
    def setup_live_transliteration(self):
        """Set up live transliteration on input changes."""
        self.input_text.bind("<KeyRelease>", lambda e: self.on_input_change())
        self.input_text.bind("<ButtonRelease>", lambda e: self.on_input_change())
    
    def detect_language(self, text: str) -> str:
        """Detect whether text is mostly Cyrillic or Latin."""
        if not text.strip():
            return self.direction_var.get()
        
        cyrillic_count = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
        latin_count = sum(1 for c in text if ('a' <= c.lower() <= 'z'))
        
        uzbek_latin_markers = ['gʻ', 'oʻ', 'sh', 'ch', 'ng', 'yo', 'yu', 'ya']
        uzbek_latin_count = sum(text.lower().count(marker) for marker in uzbek_latin_markers)
        
        if cyrillic_count > latin_count:
            return 'cyr_to_lat'
        elif latin_count > 0 or uzbek_latin_count > 0:
            return 'lat_to_cyr'
        else:
            return self.direction_var.get()
    
    def update_char_count(self, text: str):
        """Update character counter display."""
        count = len(text.strip())
        self.char_count_label.config(text=f"{count} белги")
    
    def on_input_change(self):
        """Called whenever input text changes."""
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        self.update_char_count(input_content)
        
        if self.auto_detect_var.get():
            detected_direction = self.detect_language(input_content)
            self.direction_var.set(detected_direction)
            # Sync display value
            self.direction_display_var.set(self.direction_map_reverse[detected_direction])
            
            if detected_direction == 'lat_to_cyr':
                self.detect_status_label.config(text="● Lotin")
            else:
                self.detect_status_label.config(text="● Кирилл")
        else:
            self.detect_status_label.config(text="")
        
        self.do_transliterate()
    
    def toggle_auto_detect(self):
        """Toggle auto-detection on/off."""
        if self.auto_detect_var.get():
            self.on_input_change()
        else:
            self.detect_status_label.config(text="")
    
    def do_transliterate(self):
        """Perform transliteration on input text."""
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        if not input_content:
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.configure(state=tk.DISABLED)
            return
        
        direction = self.direction_var.get()
        
        try:
            result = transliterate(input_content, direction)
            
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.configure(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Хатолик", f"Транслитерация хатоси: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy output text to clipboard."""
        self.output_text.configure(state=tk.NORMAL)
        output_content = self.output_text.get("1.0", tk.END).strip()
        self.output_text.configure(state=tk.DISABLED)
        
        if output_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_content)
            # Brief visual feedback
            original_title = self.root.title()
            self.root.title("KyrLat — Нусха олинди ✓")
            self.root.after(1500, lambda: self.root.title(original_title))
    
    def clear_all(self):
        """Clear both input and output areas."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state=tk.DISABLED)
        self.update_char_count("")
    
    def swap_text(self):
        """Swap output text to input and toggle direction."""
        self.output_text.configure(state=tk.NORMAL)
        output_content = self.output_text.get("1.0", tk.END).strip()
        self.output_text.configure(state=tk.DISABLED)
        
        if output_content:
            auto_detect_was_on = self.auto_detect_var.get()
            self.auto_detect_var.set(False)
            
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_content)
            
            current = self.direction_var.get()
            new_direction = "cyr_to_lat" if current == "lat_to_cyr" else "lat_to_cyr"
            self.direction_var.set(new_direction)
            # Sync display value
            self.direction_display_var.set(self.direction_map_reverse[new_direction])
            
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.configure(state=tk.DISABLED)
            
            self.auto_detect_var.set(auto_detect_was_on)
            self.on_input_change()


def main():
    """Entry point for the application."""
    root = tk.Tk()
    app = TransliteratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
