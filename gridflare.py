import os
import subprocess
import json
import shutil
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# Directories
VIDEO_DIR = "video/"
THUMBNAIL_DIR = "thumbnails/"

# Make sure the required directories exist
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# Port for HTTP server
PORT = 8080

# Get the local IP of the machine
def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

local_ip = get_local_ip()

def run_server():
    """Starts the HTTP server and provides the access URL."""
    with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print("\n-------------------------- GridFlare ---------------------------")
        print(f"  Server is running on port >> {PORT}...")
        print("Access it from other devices on the same network via:")
        print(f"    http://{local_ip}:{PORT}")
        print("-----------------------------------------------------------------")
        print("  Press Ctrl+C to stop the server.")
        print("-----------------------------------------------------------------")
        httpd.serve_forever()

def get_video_length(file_path):
    """Get the length of the video in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout.strip())

def move_thumbnail(video_name):
    """Move the downloaded thumbnail from the video folder to the thumbnails folder."""
    thumbnail_name = f"{VIDEO_DIR}{video_name}.webp"
    new_thumbnail_path = f"{THUMBNAIL_DIR}{video_name}.webp"
    
    if os.path.exists(thumbnail_name):
        print(f"Found thumbnail! Moving it to {new_thumbnail_path}")
        shutil.move(thumbnail_name, new_thumbnail_path)
        return new_thumbnail_path
    else:
        print(f"Thumbnail file '{thumbnail_name}' not found!")
        return None

def download_video(url, video_name):
    """Download video and extract relevant metadata."""
    cmd = [
        "yt-dlp",
        "-f", "best",
        "--write-thumbnail",
        "--output", f"{VIDEO_DIR}{video_name}.mp4",
        "--merge-output-format", "mp4",
        "--write-info-json",
        url
    ]
    print(f"Running command: {' '.join(cmd)}")  # Log the command being run
    subprocess.run(cmd)

    # Check if the video file exists
    video_file = f"{VIDEO_DIR}{video_name}.mp4"
    if not os.path.exists(video_file):
        print(f"Error: Video file '{video_file}' does not exist after download!")
        return {}

    # Find the metadata JSON file
    metadata_file = f"{VIDEO_DIR}{video_name}.info.json"
    if not os.path.exists(metadata_file):
        print(f"Error: Metadata file '{metadata_file}' does not exist!")
        return {}

    # Read the metadata JSON file
    with open(metadata_file, "r") as f:
        video_metadata = json.load(f)

    # Extract necessary information from the metadata
    video_data = {
        "id": video_metadata.get("id", ""),
        "title": video_metadata.get("title", ""),
        "length": get_video_length(video_file),  # Get length of video
    }

    # Move the thumbnail file to the thumbnails folder
    thumbnail_path = move_thumbnail(video_name)
    if thumbnail_path:
        video_data["thumbnail"] = thumbnail_path
    else:
        video_data["thumbnail"] = ""  # If no thumbnail, leave empty

    # Read existing video data (if any) from video.json
    if os.path.exists("video.json"):
        with open("video.json", "r") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    # Append the new video data to the existing list
    existing_data.append(video_data)

    # Write the updated data back to video.json
    with open("video.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    os.remove(metadata_file)

    return video_data

def start_video_download():
    """Handles video downloading process."""
    url = input("Enter the video URL: ")
    video_name = input("Enter the name for the video (no spaces, no special chars): ")
    video_data = download_video(url, video_name)
    if video_data:
        print(f"Downloaded and saved video data: {video_data}")
    else:
        print("Error: Video download or processing failed.")

def start_server():
    """Start the local server."""
    run_server()

def show_menu():
    """Display the TUI menu and handle user input."""
    while True:
        print("\n-------------------- GridFlare ---------------------")
        print("1 >> Start HTTP Server")
        print("2 >> Download Video")
        print("3 >> Exit")
        print("------------------------------------------------------")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            print("Choose Port: ")
            start_server()
        elif choice == "2":
            start_video_download()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    show_menu()

