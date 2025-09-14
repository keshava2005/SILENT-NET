# network.py - Network Operations

import socket
import requests
import threading
import json
from datetime import datetime
from config import NETWORK_PORT, NETWORK_TIMEOUT, STATUS_CHECK_INTERVAL

class NetworkManager:
    """Handle all network-related operations."""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.local_ip = self.get_local_ip()
    
    @staticmethod
    def get_local_ip():
        """Get the local IP address."""
        return socket.gethostbyname(socket.gethostname())
    
    def connect_to_peer(self, peer_ip):
        """Establish connection with a peer."""
        try:
            response = requests.get(
                f"http://{peer_ip}:{NETWORK_PORT}/info", 
                timeout=NETWORK_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to {peer_ip}: {str(e)}")
        return None
    
    def send_message(self, peer_ip, payload):
        """Send an encrypted message to a peer."""
        try:
            response = requests.post(
                f"http://{peer_ip}:{NETWORK_PORT}/message", 
                json=payload, 
                timeout=NETWORK_TIMEOUT
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def scan_network(self, callback):
        """Scan the local network for other SilentNet instances."""
        def scan():
            base_ip = '.'.join(self.local_ip.split('.')[:-1])
            found_peers = []
            
            for i in range(1, 255):
                test_ip = f"{base_ip}.{i}"
                if test_ip == self.local_ip:
                    continue
                
                try:
                    response = requests.get(
                        f"http://{test_ip}:{NETWORK_PORT}/info", 
                        timeout=0.5
                    )
                    if response.status_code == 200:
                        peer_info = response.json()
                        found_peers.append((test_ip, peer_info['user_id']))
                except:
                    pass
            
            callback(found_peers)
        
        thread = threading.Thread(target=scan, daemon=True)
        thread.start()
    
    def start_peer_monitor(self, peers, update_callback):
        """Monitor peer connection status."""
        def monitor():
            import time
            while True:
                for peer_id, peer_info in peers.items():
                    try:
                        response = requests.get(
                            f"http://{peer_info['ip']}:{NETWORK_PORT}/info", 
                            timeout=1
                        )
                        if response.status_code == 200:
                            peer_info['status'] = 'online'
                            peer_info['last_seen'] = datetime.now()
                        else:
                            peer_info['status'] = 'offline'
                    except:
                        peer_info['status'] = 'offline'
                
                update_callback()
                time.sleep(STATUS_CHECK_INTERVAL)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def export_public_key(self, user_id, public_key_pem, key_hash):
        """Export public key to a JSON file."""
        key_data = {
            'user_id': user_id,
            'public_key': public_key_pem.decode(),
            'key_hash': key_hash,
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"{user_id}_public_key.json"
        with open(filename, 'w') as f:
            json.dump(key_data, f, indent=2)
        
        return filename