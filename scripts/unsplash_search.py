#!/usr/bin/env python3
"""
Search Unsplash for images by query.
Usage: python3 unsplash_search.py "search query" [count]
Returns JSON with image URLs.
"""

import sys
import json
import os
import urllib.request
import urllib.parse

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

def search_unsplash(query: str, count: int = 3) -> dict:
    if not UNSPLASH_ACCESS_KEY:
        return {"error": "UNSPLASH_ACCESS_KEY not set"}

    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": "landscape"
    })

    url = f"https://api.unsplash.com/search/photos?{params}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Client-ID {UNSPLASH_ACCESS_KEY}")
    req.add_header("Accept-Version", "v1")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            results = []
            for photo in data.get("results", []):
                results.append({
                    "id": photo["id"],
                    "description": photo.get("description") or photo.get("alt_description") or "",
                    "url_regular": photo["urls"]["regular"],
                    "url_small": photo["urls"]["small"],
                    "url_raw": photo["urls"]["raw"],
                    "author": photo["user"]["name"],
                    "author_url": photo["user"]["links"]["html"],
                    "download_url": photo["links"]["download_location"]
                })

            return {
                "total": data.get("total", 0),
                "results": results
            }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: unsplash_search.py 'query' [count]"}))
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    result = search_unsplash(query, count)
    print(json.dumps(result, ensure_ascii=False, indent=2))
