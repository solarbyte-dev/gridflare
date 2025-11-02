import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import socket

# Make sure the required directories exist
os.makedirs("video", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

PORT = 8080

def get_local_ip():
    # Get the IP address of the machine in the current network
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

local_ip = get_local_ip()

def run_server():
    # Use 0.0.0.0 to bind to all network interfaces, not just localhost
    with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        print(f"Visit: http://{local_ip}:{PORT} (from the local network)")
        print(f"Or you can try: http://{get_local_ip()}:{PORT} from other devices")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()

