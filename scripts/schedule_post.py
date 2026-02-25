#!/usr/bin/env python3
"""
Schedule a post for later publication.
Usage: python3 schedule_post.py "HH:MM" "текст поста" "url1" "url2" "url3"

Time is in MSK (UTC+3). Creates an at job to publish at specified time.
"""

import sys
import os
import subprocess
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = ""

def schedule_post(time_str: str, caption: str, photo_urls: list) -> dict:
    """Schedule post for publication at specified MSK time."""

    # Parse time (HH:MM format)
    try:
        hour, minute = map(int, time_str.split(":"))
    except:
        return {"error": f"Invalid time format: {time_str}. Use HH:MM"}

    # Get current time in MSK (UTC+3)
    msk = timezone(timedelta(hours=3))
    now_msk = datetime.now(msk)

    # Create target datetime in MSK
    target_msk = now_msk.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # If time already passed today, schedule for tomorrow
    if target_msk <= now_msk:
        target_msk += timedelta(days=1)

    # Convert to UTC for at command
    target_utc = target_msk.astimezone(timezone.utc)
    at_time = target_utc.strftime("%H:%M %Y-%m-%d")

    # Build the command to execute
    urls_args = ' '.join(f'"{url}"' for url in photo_urls)
    # Escape quotes in caption
    escaped_caption = caption.replace('"', '\\"')

    publish_cmd = f'BOT_TOKEN="{BOT_TOKEN}" python3 /root/Bot/scripts/send_media_group.py "{CHANNEL_ID}" "{escaped_caption}" {urls_args}'

    # Create at job
    try:
        process = subprocess.Popen(
            ['at', target_utc.strftime("%H:%M"), target_utc.strftime("%Y-%m-%d")],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=publish_cmd)

        if process.returncode != 0 and "warning" not in stderr.lower():
            return {"error": f"Failed to schedule: {stderr}"}

        return {
            "success": True,
            "scheduled_for": target_msk.strftime("%Y-%m-%d %H:%M MSK"),
            "message": f"Пост запланирован на {target_msk.strftime('%H:%M')} MSK"
        }
    except FileNotFoundError:
        return {"error": "at command not found. Install with: apt install at"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import json

    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "Usage: schedule_post.py 'HH:MM' 'caption' 'url1' [url2] [url3]"
        }))
        sys.exit(1)

    time_str = sys.argv[1]
    caption = sys.argv[2]
    photo_urls = sys.argv[3:]

    result = schedule_post(time_str, caption, photo_urls)
    print(json.dumps(result, ensure_ascii=False, indent=2))
