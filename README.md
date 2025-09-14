# 🔐 SilentNet - Military Grade Secure Communication System

A peer-to-peer encrypted messaging application with advanced security features.

## 📁 Project Structure

```
SilentNet/
│
├── main.py              # Main application entry point
├── config.py            # Configuration and constants
├── encryption.py        # Encryption/decryption module
├── database.py          # Database operations
├── network.py           # Network operations
├── api_server.py        # FastAPI server module
├── ui_manager.py        # UI management module
├── custom_widgets.py    # Custom UI components
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## 🚀 Features

### Security
- **RSA-4096** asymmetric encryption for key exchange
- **AES-256** symmetric encryption for messages
- **SHA-256** hashing for key fingerprinting
- End-to-end encryption
- Auto-delete messages (5-minute timer)
- Secure local database storage

### Communication
- Peer-to-peer messaging
- Priority message system with alerts
- Message history per peer
- Multiline message support (Shift+Enter)
- 1000 character limit with counter
- Timestamp for all messages

### UI/UX
- Military-themed tactical interface
- Dark mode with green accent colors
- Animated status indicators
- Boot sequence animation
- Flash alerts for priority messages
- Real-time clock and uptime display

### Network
- Automatic network scanning
- Peer status monitoring
- Connection health checks
- IP-based peer discovery
- RESTful API endpoints

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

## 📖 How to Use

### Starting the Application

1. **Launch the application:**
   - Run `python main.py`
   - Enter your callsign (e.g., ALPHA-1, BRAVO-6)
   - The system will initialize and display your IP address

2. **Connect to Peers:**
   - Click "ESTABLISH CONNECTION"
   - Enter the peer's IP address
   - The secure channel will be established automatically

3. **Send Messages:**
   - Select a peer from the list
   - Type your message in the compose area
   - Optional: Enable AUTO-DELETE or HIGH PRIORITY
   - Click "TRANSMIT" or press Enter

### Advanced Features

- **Network Scan:** Automatically discover peers on your local network
- **Export Keys:** Save your public key for secure sharing
- **Clear History:** Securely delete all message history

## 🏗️ Module Breakdown

### `main.py`
- Main application controller
- Coordinates all modules
- Handles user authentication
- Manages application lifecycle

### `config.py`
- Centralized configuration
- Color schemes
- Network settings
- Application constants

### `encryption.py`
- RSA key generation
- AES encryption/decryption
- Key serialization
- Cryptographic operations

### `database.py`
- SQLite database management
- Message persistence
- Query operations
- Data retrieval

### `network.py`
- Network scanning
- Peer connectivity
- Message transmission
- Status monitoring

### `api_server.py`
