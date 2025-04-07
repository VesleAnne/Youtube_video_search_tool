import sys
import urllib.parse
import time

from get_subs import main as get_subs_main, extract_video_id
#from id_extractor import extract_video_id
from selenium_parser import scrape_channel_videos

def is_channel_url(url: str) -> bool:
    """
    Checks if the URL likely corresponds to a channel page or is it a single video link
    """
    url_lower = url.lower()
    channel_markers = ("@","/channel/","/c/")
    if any(m in url_lower for m in channel_markers):
        return True 
    return False

def fix_url(url: str) -> str:
    """
    If the passed channel url is not for the videos but for other pages this function changes it and returns an URL ending in /videos.
    """
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.split("/")

    excluded_segments = {"featured", "shorts", "streams", "community", "playlists", "store", ""}
    while len(path_parts) > 1 and path_parts[-1].lower() in excluded_segments:
        path_parts.pop()

    if path_parts[-1].lower() != "videos":
        path_parts.append("videos")

    new_path = "/".join(path_parts)
    fixed_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return fixed_url

def main():
    start_time = time.time()
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1].strip()
    else:
        youtube_url = input("Enter a YouTube URL to a single video or a channel: ").strip()
    
    if is_channel_url(youtube_url):
        channel_url = fix_url(youtube_url)
        print(f"Detected channel URL. Scraping {channel_url} ...")
        video_links = scrape_channel_videos(channel_url)
        print(f"Found {len(video_links)} videos on the channel.")

        for link in video_links:
            video_id = extract_video_id(link)
            if video_id:
                print(f"Extracting subtitles for video_id={video_id}")
                get_subs_main(video_id)
            else:
                print(f"Skipping invalid or unrecognized link: {link}")

    else:
        print("Detected single video URL.")
        video_id = extract_video_id(youtube_url)

        if video_id:
            print(f"Extracting subtitles for video_id={video_id}")
            get_subs_main(video_id)
        else:
                print("Could not extract a valid video ID from the provided URL.")      

    end_time = time.time()
    total_time = end_time - start_time

    minutes = int(total_time) // 60
    seconds = int(total_time) % 60

    print(f"\n\n===== Total time spent: {minutes}m {seconds}s")

if __name__ == "__main__":
    main()