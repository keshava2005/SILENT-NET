# database.py - Database Operations

import sqlite3
from datetime import datetime

class MessageDatabase:
    """Handle all database operations for message storage."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect(
            f'{user_id}_messages.db', 
            check_same_thread=False
        )
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create the messages table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                recipient TEXT,
                message TEXT,
                iv TEXT,
                key TEXT,
                priority INTEGER DEFAULT 0,
                auto_delete INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_message(self, sender, recipient, message, key, iv, priority=0, auto_delete=0):
        """Save a message to the database."""
        self.cursor.execute('''
            INSERT INTO messages (sender, recipient, message, key, iv, priority, auto_delete)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sender, recipient, message, key, iv, priority, auto_delete))
        self.conn.commit()
    
    def get_messages(self, peer_id=None, limit=100):
        """Retrieve messages from the database."""
        if peer_id:
            self.cursor.execute('''
                SELECT sender, recipient, message, timestamp 
                FROM messages 
                WHERE sender = ? OR recipient = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (peer_id, peer_id, limit))
        else:
            self.cursor.execute('''
                SELECT sender, recipient, message, timestamp 
                FROM messages 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        return self.cursor.fetchall()
    
    def delete_old_messages(self, days=7):
        """Delete messages older than specified days."""
        self.cursor.execute('''
            DELETE FROM messages 
            WHERE timestamp < datetime('now', '-? days')
        ''', (days,))
        self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        self.conn.close()