# ui_manager.py - UI Management Module

import tkinter as tk
from tkinter import scrolledtext, messagebox, Checkbutton, BooleanVar
from datetime import datetime
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_ALPHA, MESSAGE_CHAR_LIMIT
from custom_widgets import MilitaryButton, StatusIndicator

class UIManager:
    """Manage all UI components and interactions."""
    
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.setup_window()
        self.create_variables()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title(f"SILENTNET | {self.app.user_id} | SECURE")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS['bg_dark'])
        self.root.resizable(True, True)
        self.root.attributes('-alpha', WINDOW_ALPHA)
    
    def create_variables(self):
        """Initialize UI variables."""
        self.selected_peer = tk.StringVar()
        self.auto_delete_var = BooleanVar(value=False)
        self.priority_var = BooleanVar(value=False)
    
    def create_main_ui(self):
        """Create the main UI structure."""
        self.create_status_bar()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel
        left_panel = tk.Frame(main_container, bg=COLORS['bg_medium'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        self.create_control_panel(left_panel)
        
        # Right Panel
        right_panel = tk.Frame(main_container, bg=COLORS['bg_medium'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.create_communication_area(right_panel)
    
    def create_status_bar(self):
        """Create the top status bar."""
        status_frame = tk.Frame(self.root, bg=COLORS['bg_dark'], height=60)
        status_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        # Title Frame
        title_frame = tk.Frame(status_frame, bg=COLORS['bg_dark'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title = tk.Label(
            title_frame, 
            text="◆ SILENTNET TACTICAL COMMS ◆",
            bg=COLORS['bg_dark'], 
            fg=COLORS['accent_green'],
            font=('Consolas', 16, 'bold')
        )
        title.pack(anchor='w')
        
        self.encryption_label = tk.Label(
            title_frame,
            text=f"ENCRYPTION: {self.app.encryption_level} | KEY HASH: {self.app.public_key_hash}",
            bg=COLORS['bg_dark'], 
            fg=COLORS['text_secondary'],
            font=('Consolas', 9)
        )
        self.encryption_label.pack(anchor='w')
        
        # Status Container
        status_container = tk.Frame(status_frame, bg=COLORS['bg_dark'])
        status_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.network_status = StatusIndicator(status_container, "NETWORK")
        self.network_status.pack(side=tk.LEFT, padx=10)
        
        self.security_status = StatusIndicator(status_container, "SECURITY")
        self.security_status.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(
            status_container, 
            text="", 
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary'], 
            font=('Consolas', 10)
        )
        self.time_label.pack(side=tk.LEFT, padx=20)
    
    def create_control_panel(self, parent):
        """Create the left control panel."""
        # User Info Section
        user_frame = tk.LabelFrame(
            parent, 
            text=" OPERATOR INFO ",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'], 
            font=('Consolas', 10, 'bold'),
            relief=tk.RIDGE, 
            bd=1
        )
        user_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            user_frame, 
            text=f"CALLSIGN: {self.app.user_id}",
            bg=COLORS['bg_medium'],
            fg=COLORS['text_primary'], 
            font=('Consolas', 10)
        ).pack(anchor='w', padx=10, pady=5)
        
        self.session_label = tk.Label(
            user_frame, 
            text="SESSION: ACTIVE",
            bg=COLORS['bg_medium'],
            fg=COLORS['text_secondary'], 
            font=('Consolas', 9)
        )
        self.session_label.pack(anchor='w', padx=10, pady=2)
        
        # Network Peers Section
        peers_frame = tk.LabelFrame(
            parent, 
            text=" NETWORK PEERS ",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'], 
            font=('Consolas', 10, 'bold'),
            relief=tk.RIDGE, 
            bd=1
        )
        peers_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        add_peer_btn = MilitaryButton(
            peers_frame, 
            text="▼ ESTABLISH CONNECTION ▼",
            command=self.app.add_peer, 
            accent_color=COLORS['accent_amber']
        )
        add_peer_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Peer List
        peer_container = tk.Frame(peers_frame, bg=COLORS['bg_medium'])
        peer_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(peer_container, bg=COLORS['bg_medium'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.peers_listbox = tk.Listbox(
            peer_container, 
            bg=COLORS['bg_light'], 
            fg=COLORS['text_primary'],
            selectbackground=COLORS['button_hover'], 
            selectforeground=COLORS['accent_green'],
            font=('Consolas', 10), 
            relief=tk.FLAT, 
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.peers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.peers_listbox.yview)
        self.peers_listbox.bind('<<ListboxSelect>>', self.app.on_peer_select)
        
        # Operations Section
        ops_frame = tk.LabelFrame(
            parent, 
            text=" OPERATIONS ",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'], 
            font=('Consolas', 10, 'bold'),
            relief=tk.RIDGE, 
            bd=1
        )
        ops_frame.pack(fill=tk.X, padx=10, pady=5)
        
        MilitaryButton(
            ops_frame, 
            text="◈ NETWORK SCAN",
            command=self.app.scan_network,
            accent_color=COLORS['text_secondary']
        ).pack(fill=tk.X, padx=10, pady=5)
        
        MilitaryButton(
            ops_frame, 
            text="◈ EXPORT KEYS",
            command=self.app.export_keys,
            accent_color=COLORS['text_secondary']
        ).pack(fill=tk.X, padx=10, pady=5)
        
        MilitaryButton(
            ops_frame, 
            text="◈ CLEAR HISTORY",
            command=self.app.clear_history,
            accent_color=COLORS['accent_red']
        ).pack(fill=tk.X, padx=10, pady=5)
        
        # Statistics
        self.stats_label = tk.Label(
            parent, 
            text="MESSAGES: 0 | UPTIME: 00:00:00",
            bg=COLORS['bg_medium'], 
            fg=COLORS['text_dim'],
            font=('Consolas', 8)
        )
        self.stats_label.pack(side=tk.BOTTOM, pady=10)
    
    def create_communication_area(self, parent):
        """Create the main communication area."""
        # Message Display
        display_frame = tk.LabelFrame(
            parent, 
            text=" SECURE CHANNEL ",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'], 
            font=('Consolas', 10, 'bold'),
            relief=tk.RIDGE, 
            bd=1
        )
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.message_display = scrolledtext.ScrolledText(
            display_frame,
            state='disabled',
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_green'],
            font=('Consolas', 11),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure message tags
        self.message_display.tag_configure('system', foreground=COLORS['text_dim'], font=('Consolas', 10, 'italic'))
        self.message_display.tag_configure('sent', foreground=COLORS['accent_green'])
        self.message_display.tag_configure('received', foreground=COLORS['text_primary'])
        self.message_display.tag_configure('error', foreground=COLORS['accent_red'])
        self.message_display.tag_configure('timestamp', foreground=COLORS['text_dim'], font=('Consolas', 9))
        
        # Input Area
        input_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        compose_frame = tk.LabelFrame(
            input_frame, 
            text=" COMPOSE MESSAGE ",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'], 
            font=('Consolas', 10, 'bold'),
            relief=tk.RIDGE, 
            bd=1
        )
        compose_frame.pack(fill=tk.X)
        
        # Text Entry
        entry_container = tk.Frame(compose_frame, bg=COLORS['bg_light'], relief=tk.SUNKEN, bd=1)
        entry_container.pack(fill=tk.X, padx=10, pady=10)
        
        self.message_entry = tk.Text(
            entry_container, 
            height=3,
            bg=COLORS['bg_light'], 
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_green'], 
            font=('Consolas', 11),
            relief=tk.FLAT, 
            wrap=tk.WORD
        )
        self.message_entry.pack(fill=tk.X, padx=5, pady=5)
        self.message_entry.bind('<Return>', self.app.send_message_enter)
        self.message_entry.bind('<Shift-Return>', lambda e: None)
        self.message_entry.bind('<KeyRelease>', self.update_char_counter)
        
        # Options
        options_frame = tk.Frame(compose_frame, bg=COLORS['bg_medium'])
        options_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        auto_delete_check = Checkbutton(
            options_frame, 
            text="AUTO-DELETE (5 MIN)",
            variable=self.auto_delete_var,
            bg=COLORS['bg_medium'], 
            fg=COLORS['text_secondary'],
            selectcolor=COLORS['bg_light'], 
            font=('Consolas', 9)
        )
        auto_delete_check.pack(side=tk.LEFT, padx=5)
        
        priority_check = Checkbutton(
            options_frame, 
            text="HIGH PRIORITY",
            variable=self.priority_var,
            bg=COLORS['bg_medium'], 
            fg=COLORS['accent_amber'],
            selectcolor=COLORS['bg_light'], 
            font=('Consolas', 9)
        )
        priority_check.pack(side=tk.LEFT, padx=5)
        
        self.char_counter = tk.Label(
            options_frame, 
            text="0/1000",
            bg=COLORS['bg_medium'],
            fg=COLORS['text_dim'], 
            font=('Consolas', 9)
        )
        self.char_counter.pack(side=tk.LEFT, padx=20)
        
        send_btn = MilitaryButton(
            options_frame, 
            text="◆ TRANSMIT ◆",
            command=self.app.send_message,
            accent_color=COLORS['accent_green']
        )
        send_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_char_counter(self, event=None):
        """Update the character counter."""
        text_length = len(self.message_entry.get("1.0", "end-1c"))
        self.char_counter.config(text=f"{text_length}/{MESSAGE_CHAR_LIMIT}")
        if text_length > MESSAGE_CHAR_LIMIT:
            self.char_counter.config(fg=COLORS['accent_red'])
        else:
            self.char_counter.config(fg=COLORS['text_dim'])
    
    def add_message_to_display(self, message, msg_type='system'):
        """Add a message to the display."""
        def _add():
            self.message_display.config(state='normal')
            
            if msg_type == 'system':
                self.message_display.insert(tk.END, f"◆ {message} ◆\n", 'system')
            elif msg_type == 'error':
                self.message_display.insert(tk.END, f"⚠ {message}\n", 'error')
            elif msg_type == 'timestamp':
                self.message_display.insert(tk.END, f"{message}\n", 'timestamp')
            elif msg_type == 'sent':
                self.message_display.insert(tk.END, f"{message}\n", 'sent')
            elif msg_type == 'received':
                self.message_display.insert(tk.END, f"{message}\n", 'received')
            else:
                self.message_display.insert(tk.END, f"{message}\n")
            
            self.message_display.config(state='disabled')
            self.message_display.yview(tk.END)
        
        self.root.after(0, _add)
    
    def update_peer_list(self, peers):
        """Update the peer list display."""
        self.peers_listbox.delete(0, tk.END)
        for peer_name, peer_info in peers.items():
            status = "●" if peer_info.get('status') == 'online' else "○"
            self.peers_listbox.insert(tk.END, f"{status} {peer_name}")
        
        if peers and not self.selected_peer.get():
            self.selected_peer.set(list(peers.keys())[0])
            self.peers_listbox.selection_set(0)
    
    def update_time(self, current_time, uptime_str):
        """Update the time display."""
        self.time_label.config(text=current_time)
        self.stats_label.config(text=uptime_str)
    
    def flash_priority_alert(self):
        """Flash the window for priority messages."""
        original_bg = self.root.cget('bg')
        for i in range(3):
            self.root.after(i * 200, lambda: self.root.configure(bg=COLORS['accent_red']))
            self.root.after(i * 200 + 100, lambda: self.root.configure(bg=original_bg))