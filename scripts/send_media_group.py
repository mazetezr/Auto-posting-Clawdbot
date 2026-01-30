#!/usr/bin/env python3
"""
Send media group (multiple photos with caption) to Telegram.
Usage: python3 send_media_group.py <chat_id> <caption> <photo_url1> [photo_url2] [photo_url3] ...

Downloads photos to temp folder and sends as media group.
"""

import sys
import json
import os
import urllib.request
import tempfile
import shutil

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

def download_photo(url: str, temp_dir: str, index: int) -> str:
    """Download photo to temp directory, return local path."""
    # Determine extension from URL or default to jpg
    ext = ".jpg"
    if ".png" in url.lower():
        ext = ".png"
    elif ".webp" in url.lower():
        ext = ".webp"

    local_path = os.path.join(temp_dir, f"photo_{index}{ext}")

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")

    with urllib.request.urlopen(req, timeout=30) as response:
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(response, f)

    return local_path

def send_media_group(chat_id: str, caption: str, photo_urls: list) -> dict:
    """Send multiple photos as media group with caption on first photo."""
    if not BOT_TOKEN:
        return {"error": "BOT_TOKEN not set"}

    if not photo_urls:
        return {"error": "No photo URLs provided"}

    # Create temp directory for photos
    temp_dir = tempfile.mkdtemp(prefix="tg_photos_")

    try:
        # Download all photos
        local_photos = []
        for i, url in enumerate(photo_urls[:10]):  # Telegram limit: 10 photos
            try:
                local_path = download_photo(url, temp_dir, i)
                local_photos.append(local_path)
            except Exception as e:
                print(f"Warning: Failed to download {url}: {e}", file=sys.stderr)

        if not local_photos:
            return {"error": "Failed to download any photos"}

        # Build multipart form data
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

        # Build media JSON array
        media_array = []
        for i, _ in enumerate(local_photos):
            media_item = {
                "type": "photo",
                "media": f"attach://photo_{i}"
            }
            if i == 0 and caption:
                media_item["caption"] = caption
                media_item["parse_mode"] = "HTML"
            media_array.append(media_item)

        # Build multipart body
        body_parts = []

        # Add chat_id
        body_parts.append(f"--{boundary}".encode())
        body_parts.append(b'Content-Disposition: form-data; name="chat_id"')
        body_parts.append(b"")
        body_parts.append(chat_id.encode())

        # Add media JSON
        body_parts.append(f"--{boundary}".encode())
        body_parts.append(b'Content-Disposition: form-data; name="media"')
        body_parts.append(b"")
        body_parts.append(json.dumps(media_array).encode())

        # Add photo files
        for i, photo_path in enumerate(local_photos):
            filename = os.path.basename(photo_path)
            with open(photo_path, 'rb') as f:
                photo_data = f.read()

            body_parts.append(f"--{boundary}".encode())
            body_parts.append(f'Content-Disposition: form-data; name="photo_{i}"; filename="{filename}"'.encode())
            body_parts.append(b"Content-Type: image/jpeg")
            body_parts.append(b"")
            body_parts.append(photo_data)

        body_parts.append(f"--{boundary}--".encode())

        body = b"\r\n".join(body_parts)

        # Send request
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMediaGroup"
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            return result

    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "Usage: send_media_group.py <chat_id> <caption> <photo_url1> [photo_url2] ..."
        }))
        sys.exit(1)

    chat_id = sys.argv[1]
    caption = sys.argv[2]
    photo_urls = sys.argv[3:]

    result = send_media_group(chat_id, caption, photo_urls)
    print(json.dumps(result, ensure_ascii=False, indent=2))
