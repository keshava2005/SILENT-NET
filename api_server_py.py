# api_server.py - FastAPI Server Module

from fastapi import FastAPI, Request
import uvicorn
import threading
from datetime import datetime
from config import NETWORK_PORT, APP_VERSION, APP_CAPABILITIES

# Create FastAPI app
app = FastAPI()

# Global reference to main application
app_instance = None

def set_app_instance(instance):
    """Set the main application instance."""
    global app_instance
    app_instance = instance

@app.post("/message")
async def receive_message(request: Request):
    """Endpoint to receive encrypted messages."""
    data = await request.json()
    if app_instance:
        app_instance.handle_incoming_message(
            data["sender_id"], 
            data["key"], 
            data["iv"], 
            data["message"],
            data.get("auto_delete", False),
            data.get("priority", False),
            data.get("timestamp")
        )
    return {"status": "message received"}

@app.get("/info")
async def get_info():
    """Endpoint to get peer information."""
    if app_instance:
        return {
            "user_id": app_instance.user_id, 
            "public_key": app_instance.public_key_pem.decode(),
            "version": APP_VERSION,
            "capabilities": APP_CAPABILITIES
        }
    return {"error": "App not initialized"}

@app.get("/ping")
async def ping():
    """Endpoint to check if the service is online."""
    return {"status": "online", "timestamp": datetime.now().isoformat()}

def start_server(host_ip):
    """Start the FastAPI server."""
    print("\n" + "="*50)
    print("◆ SILENTNET TACTICAL COMMUNICATION SYSTEM ◆")
    print("="*50)
    print(f"◆ LOCAL IP ADDRESS: {host_ip}")
    print(f"◆ LISTENING PORT: {NETWORK_PORT}")
    print(f"◆ ENCRYPTION: AES-256 | RSA-4096")
    print("="*50)
    print("◆ Share your IP with trusted operators to connect")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=NETWORK_PORT, log_level="warning")

def run_in_thread(host_ip):
    """Run the server in a separate thread."""
    server_thread = threading.Thread(target=start_server, args=(host_ip,), daemon=True)
    server_thread.start()
    return server_thread