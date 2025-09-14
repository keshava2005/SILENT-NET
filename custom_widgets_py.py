# custom_widgets.py - Custom UI Components

import tkinter as tk
from tkinter import Canvas
from config import COLORS

class MilitaryButton(tk.Button):
    """Custom military-styled button with hover effects."""
    
    def __init__(self, parent, text="", command=None, accent_color=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=COLORS['button_bg'],
            fg=accent_color or COLORS['text_primary'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['accent_green'],
            relief=tk.FLAT,
            font=('Consolas', 10, 'bold'),
            cursor='hand2',
            bd=2,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent_green'],
            **kwargs
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.accent = accent_color or COLORS['text_primary']
    
    def on_enter(self, e):
        self['bg'] = COLORS['button_hover']
        self['fg'] = COLORS['accent_green']
    
    def on_leave(self, e):
        self['bg'] = COLORS['button_bg']
        self['fg'] = self.accent

class StatusIndicator(tk.Frame):
    """Animated status indicator widget."""
    
    def __init__(self, parent, label="STATUS"):
        super().__init__(parent, bg=COLORS['bg_dark'])
        
        # Label
        self.label = tk.Label(
            self, 
            text=label, 
            bg=COLORS['bg_dark'], 
            fg=COLORS['text_dim'], 
            font=('Consolas', 8)
        )
        self.label.pack(side=tk.LEFT, padx=5)
        
        # Canvas for indicator
        self.canvas = Canvas(
            self, 
            width=12, 
            height=12, 
            bg=COLORS['bg_dark'], 
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT)
        self.indicator = self.canvas.create_oval(2, 2, 10, 10, fill=COLORS['text_dim'], outline="")
        
        # Status text
        self.status_text = tk.Label(
            self, 
            text="OFFLINE", 
            bg=COLORS['bg_dark'], 
            fg=COLORS['text_dim'], 
            font=('Consolas', 8)
        )
        self.status_text.pack(side=tk.LEFT, padx=5)
    
    def set_status(self, status="offline"):
        """Update the status indicator."""
        colors = {
            'online': (COLORS['accent_green'], "ONLINE"),
            'offline': (COLORS['text_dim'], "OFFLINE"),
            'warning': (COLORS['accent_amber'], "WARNING"),
            'error': (COLORS['accent_red'], "ERROR")
        }
        color, text = colors.get(status, (COLORS['text_dim'], "UNKNOWN"))
        self.canvas.itemconfig(self.indicator, fill=color)
        self.status_text.config(text=text, fg=color)
        self.pulse(color)
    
    def pulse(self, color):
        """Animate the indicator with a pulse effect."""
        def animate(size=10):
            if size > 12:
                return
            self.canvas.coords(
                self.indicator, 
                6-size/2, 6-size/2, 
                6+size/2, 6+size/2
            )
            self.after(50, lambda: animate(size + 0.5))
        animate()