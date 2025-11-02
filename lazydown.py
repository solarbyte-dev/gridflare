import os
import subprocess
import json
import shutil

VIDEO_DIR = "video/"
THUMBNAIL_DIR = "thumbnails/"

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
    thumbnail_name = f"{VIDEO_DIR}{video_name}.webp"  # yt-dlp downloads it with the video name
    new_thumbnail_path = f"{THUMBNAIL_DIR}{video_name}.webp"  # Saving as .webp

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


def main():
    # Get user input for video URL and name
    url = input("Enter the video URL: ")
    video_name = input("Enter the name for the video (no spaces, no special chars): ")

    # Download and process video
    video_data = download_video(url, video_name)
    if video_data:
        print(f"Downloaded and saved video data: {video_data}")
    else:
        print("Error: Video download or processing failed.")

if __name__ == "__main__":
    main()

