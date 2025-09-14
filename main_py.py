# main.py - Main Application File

import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import hashlib
import threading
import time
from datetime import datetime

# Import custom modules
from config import *
from encryption import generate_keys, serialize_public_key, deserialize_public_key, encrypt_message, decrypt_message
from database import MessageDatabase
from network import NetworkManager
from ui_manager import UIManager
from custom_widgets import MilitaryButton
import api_server

class SecureChatApp:
    """Main application class that coordinates all modules."""
    
    def __init__(self, root):
        self.root = root
        self.message_count = 0
        self.start_time = datetime.now()
        self.encryption_level = "AES-256 | RSA-4096"
        
        # Initialize components
        self.initialize_user()
        self.initialize_encryption()
        self.initialize_data_structures()
        self.initialize_modules()
        self.setup_ui()
        self.start_services()
    
    def initialize_user(self):
        """Initialize user authentication."""
        self.show_login_dialog()
    
    def show_login_dialog(self):
        """Show the login dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("AUTHENTICATION REQUIRED")
        dialog.geometry("400x250")
        dialog.configure(bg=COLORS['bg_dark'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Label(
            dialog, 
            text="╔══════════════════════════════════╗",
            bg=COLORS['bg_dark'], 
            fg=COLORS['accent_green'], 
            font=('Consolas', 12)
        )
        header.pack(pady=(20, 0))
        
        title = tk.Label(
            dialog, 
            text="SECURE CHANNEL AUTHENTICATION",
            bg=COLORS['bg_dark'], 
            fg=COLORS['accent_green'], 
            font=('Consolas', 12, 'bold')
        )
        title.pack()
        
        footer = tk.Label(
            dialog, 
            text="╚══════════════════════════════════╝",
            bg=COLORS['bg_dark'], 
            fg=COLORS['accent_green'], 
            font=('Consolas', 12)
        )
        footer.pack(pady=(0, 20))
        
        # Callsign entry
        tk.Label(
            dialog, 
            text="ENTER CALLSIGN:",
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary'], 
            font=('Consolas', 10)
        ).pack(pady=10)
        
        self.callsign_entry = tk.Entry(
            dialog, 
            bg=COLORS['bg_light'], 
            fg=COLORS['accent_green'],
            insertbackground=COLORS['accent_green'], 
            font=('Consolas', 12, 'bold'),
            relief=tk.FLAT, 
            justify='center'
        )
        self.callsign_entry.pack(pady=5, padx=40, fill=tk.X)
        self.callsign_entry.focus()
        
        tk.Label(
            dialog, 
            text="Example: ALPHA-1, BRAVO-6, GHOST-9",
            bg=COLORS['bg_dark'], 
            fg=COLORS['text_dim'], 
            font=('Consolas', 8)
        ).pack()
        
        def authenticate():
            callsign = self.callsign_entry.get().strip().upper()
            if not callsign:
                callsign = f"OPERATOR-{os.urandom(2).hex().upper()}"
            self.user_id = callsign
            dialog.destroy()
        
        auth_btn = MilitaryButton(dialog, text="◆ AUTHENTICATE ◆", command=authenticate)
        auth_btn.pack(pady=20)
        
        self.callsign_entry.bind('<Return>', lambda e: authenticate())
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
    
    def initialize_encryption(self):
        """Initialize encryption keys."""
        self.private_key, self.public_key = generate_keys()
        self.public_key_pem = serialize_public_key(self.public_key)
        self.public_key_hash = hashlib.sha256(self.public_key_pem).hexdigest()[:16].upper()
    
    def initialize_data_structures(self):
        """Initialize data structures."""
        self.peers = {}
        self.message_history = {}
        self.auto_delete_time = AUTO_DELETE_TIME
    
    def initialize_modules(self):
        """Initialize all modules."""
        self.db = MessageDatabase(self.user_id)
        self.network = NetworkManager(self)
        self.ui = UIManager(self.root, self)
    
    def setup_ui(self):
        """Setup the user interface."""
        self.ui.create_main_ui()
        self.animate_boot_sequence()
    
    def start_services(self):
        """Start all background services."""
        # Start API server
        api_server.set_app_instance(self)
        api_server.run_in_thread(self.network.local_ip)
        
        # Start monitors
        self.start_status_monitor()
        self.start_auto_delete_monitor()
        self.update_time()
    
    def animate_boot_sequence(self):
        """Display boot sequence animation."""
        messages = [
            "INITIALIZING SECURE CHANNEL...",
            f"GENERATING RSA-4096 KEYPAIR...",
            f"PUBLIC KEY HASH: {self.public_key_hash}",
            "ESTABLISHING ENCRYPTED DATABASE...",
            f"STARTING NETWORK LISTENER ON PORT {NETWORK_PORT}...",
            f"OPERATOR {self.user_id} AUTHENTICATED",
            "SYSTEM READY - CHANNEL SECURE"
        ]
        
        for i, msg in enumerate(messages):
            self.root.after(i * 300, lambda m=msg: self.ui.add_message_to_display(m, msg_type='system'))
        
        self.root.after(len(messages) * 300, lambda: self.ui.network_status.set_status('online'))
        self.root.after(len(messages) * 300 + 100, lambda: self.ui.security_status.set_status('online'))
    
    def update_time(self):
        """Update time display."""
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"MESSAGES: {self.message_count} | UPTIME: {hours:02d}:{minutes:02d}:{seconds:02d}"
        
        self.ui.update_time(current_time, uptime_str)
        self.root.after(1000, self.update_time)
    
    def add_peer(self):
        """Add a new peer connection."""
        dialog = tk.Toplevel(self.root)
        dialog.title("ESTABLISH SECURE CONNECTION")
        dialog.geometry("400x200")
        dialog.configure(bg=COLORS['bg_dark'])
        dialog.resizable(False, False)
        
        tk.Label(
            dialog, 
            text="ENTER PEER IP ADDRESS:",
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'], 
            font=('Consolas', 12)
        ).pack(pady=20)
        
        ip_entry = tk.Entry(
            dialog, 
            bg=COLORS['bg_light'], 
            fg=COLORS['accent_green'],
            insertbackground=COLORS['accent_green'], 
            font=('Consolas', 12),
            relief=tk.FLAT, 
            justify='center'
        )
        ip_entry.pack(pady=10, padx=40, fill=tk.X)
        ip_entry.focus()
        
        def connect():
            peer_ip = ip_entry.get().strip()
            if not peer_ip:
                return
            
            self.ui.add_message_to_display(f"ATTEMPTING CONNECTION TO {peer_ip}...", msg_type='system')
            
            try:
                peer_info = self.network.connect_to_peer(peer_ip)
                if peer_info:
                    peer_id = peer_info['user_id']
                    peer_pub_key_pem = peer_info['public_key'].encode()
                    
                    self.peers[peer_id] = {
                        "ip": peer_ip,
                        "public_key": deserialize_public_key(peer_pub_key_pem),
                        "status": "online",
                        "last_seen": datetime.now()
                    }
                    
                    self.ui.update_peer_list(self.peers)
                    self.ui.add_message_to_display(f"◆ SECURE CHANNEL ESTABLISHED WITH {peer_id} ◆", msg_type='system')
                    dialog.destroy()
            except Exception as e:
                self.ui.add_message_to_display(f"CONNECTION ERROR: {str(e)}", msg_type='error')
        
        MilitaryButton(dialog, text="◆ CONNECT ◆", command=connect).pack(pady=20)
        ip_entry.bind('<Return>', lambda e: connect())
    
    def on_peer_select(self, event):
        """Handle peer selection."""
        selection = self.ui.peers_listbox.curselection()
        if selection:
            index = selection[0]
            peer_text = self.ui.peers_listbox.get(index)
            peer_name = peer_text[2:]  # Remove status indicator
            self.ui.selected_peer.set(peer_name)
            self.ui.add_message_to_display(f"◆ SWITCHED CHANNEL TO {peer_name} ◆", msg_type='system')
    
    def send_message_enter(self, event):
        """Handle Enter key press in message entry."""
        if not event.state & 0x0001:  # Check if Shift is not pressed
            self.send_message()
            return 'break'
    
    def send_message(self):
        """Send an encrypted message."""
        message = self.ui.message_entry.get("1.0", "end-1c").strip()
        recipient_id = self.ui.selected_peer.get()
        
        if not message or not recipient_id:
            return
        
        if len(message) > MESSAGE_CHAR_LIMIT:
            self.ui.add_message_to_display("ERROR: MESSAGE EXCEEDS 1000 CHARACTER LIMIT", msg_type='error')
            return
        
        recipient_info = self.peers.get(recipient_id)
        if not recipient_info:
            self.ui.add_message_to_display("ERROR: RECIPIENT NOT FOUND", msg_type='error')
            return
        
        try:
            # Add priority flag if enabled
            msg_with_metadata = message
            if self.ui.priority_var.get():
                msg_with_metadata = f"[PRIORITY] {message}"
            
            encrypted_key, iv, encrypted_msg = encrypt_message(recipient_info["public_key"], msg_with_metadata)
            
            payload = {
                "sender_id": self.user_id,
                "key": encrypted_key,
                "iv": iv,
                "message": encrypted_msg,
                "auto_delete": self.ui.auto_delete_var.get(),
                "priority": self.ui.priority_var.get(),
                "timestamp": datetime.now().isoformat()
            }
            
            if self.network.send_message(recipient_info['ip'], payload):
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.ui.add_message_to_display(f"[{timestamp}] YOU → {recipient_id}:", msg_type='timestamp')
                self.ui.add_message_to_display(f"  {message}", msg_type='sent')
                
                # Store in history
                if recipient_id not in self.message_history:
                    self.message_history[recipient_id] = []
                self.message_history[recipient_id].append({
                    'type': 'sent',
                    'message': message,
                    'timestamp': datetime.now(),
                    'auto_delete': self.ui.auto_delete_var.get()
                })
                
                self.message_count += 1
                self.ui.message_entry.delete("1.0", tk.END)
                self.ui.update_char_counter()
                
                # Save to database
                self.db.save_message(
                    self.user_id, recipient_id, message, encrypted_key, iv,
                    int(self.ui.priority_var.get()), int(self.ui.auto_delete_var.get())
                )
            else:
                self.ui.add_message_to_display(f"TRANSMISSION FAILED", msg_type='error')
                
        except Exception as e:
            self.ui.add_message_to_display(f"ENCRYPTION ERROR: {str(e)}", msg_type='error')
    
    def handle_incoming_message(self, sender_id, key_b64, iv_b64, msg_b64, auto_delete=False, priority=False, timestamp=None):
        """Handle incoming encrypted message."""
        try:
            decrypted_message = decrypt_message(self.private_key, key_b64, iv_b64, msg_b64)
            
            # Check for priority flag
            if decrypted_message.startswith("[PRIORITY]"):
                priority = True
                decrypted_message = decrypted_message.replace("[PRIORITY] ", "", 1)
            
            msg_time = datetime.fromisoformat(timestamp) if timestamp else datetime.now()
            display_time = msg_time.strftime("%H:%M:%S")
            
            # Display message
            if priority:
                self.ui.add_message_to_display(f"[{display_time}] ⚠ PRIORITY MESSAGE FROM {sender_id}:", msg_type='error')
                self.ui.flash_priority_alert()
            else:
                self.ui.add_message_to_display(f"[{display_time}] {sender_id} → YOU:", msg_type='timestamp')
            
            self.ui.add_message_to_display(f"  {decrypted_message}", msg_type='received')
            
            # Store in history
            if sender_id not in self.message_history:
                self.message_history[sender_id] = []
            self.message_history[sender_id].append({
                'type': 'received',
                'message': decrypted_message,
                'timestamp': msg_time,
                'auto_delete': auto_delete,
                'priority': priority
            })
            
            self.message_count += 1
            
            # Save to database
            self.db.save_message(
                sender_id, self.user_id, decrypted_message, key_b64, iv_b64,
                int(priority), int(auto_delete)
            )
            
        except Exception as e:
            self.ui.add_message_to_display(f"DECRYPTION FAILED FROM {sender_id}: {str(e)}", msg_type='error')
    
    def scan_network(self):
        """Scan the network for peers."""
        self.ui.add_message_to_display("INITIATING NETWORK SCAN...", msg_type='system')
        
        def display_results(found_peers):
            if found_peers:
                self.ui.add_message_to_display(f"SCAN COMPLETE: {len(found_peers)} PEER(S) DETECTED", msg_type='system')
                for ip, peer_id in found_peers:
                    self.ui.add_message_to_display(f"  • {peer_id} at {ip}", msg_type='system')
            else:
                self.ui.add_message_to_display("SCAN COMPLETE: NO PEERS DETECTED", msg_type='system')
        
        self.network.scan_network(lambda results: self.root.after(0, lambda: display_results(results)))
    
    def export_keys(self):
        """Export public keys."""
        filename = self.network.export_public_key(self.user_id, self.public_key_pem, self.public_key_hash)
        self.ui.add_message_to_display(f"PUBLIC KEY EXPORTED TO {filename}", msg_type='system')
    
    def clear_history(self):
        """Clear message history."""
        if messagebox.askyesno("CONFIRM", "Clear all message history? This cannot be undone."):
            self.ui.message_display.config(state='normal')
            self.ui.message_display.delete('1.0', tk.END)
            self.ui.message_display.config(state='disabled')
            self.message_history.clear()
            self.ui.add_message_to_display("MESSAGE HISTORY CLEARED", msg_type='system')
    
    def start_status_monitor(self):
        """Start monitoring peer status."""
        self.network.start_peer_monitor(
            self.peers,
            lambda: self.root.after(0, lambda: self.ui.update_peer_list(self.peers))
        )
    
    def start_auto_delete_monitor(self):
        """Start monitoring for auto-delete messages."""
        def monitor():
            while True:
                current_time = datetime.now()
                for peer_id, messages in self.message_history.items():
                    messages_to_delete = []
                    for msg in messages:
                        if msg.get('auto_delete'):
                            if (current_time - msg['timestamp']).seconds > self.auto_delete_time:
                                messages_to_delete.append(msg)
                    
                    for msg in messages_to_delete:
                        messages.remove(msg)
                        self.root.after(0, lambda p=peer_id: self.ui.add_message_to_display(
                            f"AUTO-DELETED MESSAGE FROM {p}", msg_type='system'
                        ))
                
                time.sleep(AUTO_DELETE_CHECK_INTERVAL)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Try to set window icon
    try:
        root.iconbitmap('silentnet.ico')
    except:
        pass
    
    # Create and run application
    app = SecureChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()