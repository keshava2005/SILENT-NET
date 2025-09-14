# config.py - Configuration and Constants

# Military Theme Colors
COLORS = {
    'bg_dark': '#0a0e1a',
    'bg_medium': '#141922',
    'bg_light': '#1e2530',
    'accent_green': '#00ff41',
    'accent_red': '#ff0033',
    'accent_amber': '#ffaa00',
    'text_primary': '#00ff41',
    'text_secondary': '#a0d0a0',
    'text_dim': '#5a7a5a',
    'button_bg': '#1a3a1a',
    'button_hover': '#2a5a2a',
    'border': '#00ff41',
    'warning': '#ff6600',
    'critical': '#ff0000'
}

# Network Configuration
NETWORK_PORT = 8000
NETWORK_TIMEOUT = 3
STATUS_CHECK_INTERVAL = 30  # seconds
AUTO_DELETE_CHECK_INTERVAL = 60  # seconds

# Encryption Settings
RSA_KEY_SIZE = 4096
AES_KEY_SIZE = 32
IV_SIZE = 16

# UI Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_ALPHA = 0.98
MESSAGE_CHAR_LIMIT = 1000
AUTO_DELETE_TIME = 300  # 5 minutes in seconds

# Application Info
APP_NAME = "SILENTNET"
APP_VERSION = "2.0"
APP_CAPABILITIES = ["encryption", "priority", "auto_delete"]