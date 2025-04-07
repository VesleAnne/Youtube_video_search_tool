import urllib.parse

def extract_video_id(url: str) -> str:
    """
    Extracts the 'v=' parameter from a YouTube watch URL.
    e.g. https://www.youtube.com/watch?v=abcd1234 => abcd1234
    
    Returns None if not found.
    """
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    if 'v' in query_params and len(query_params['v']) > 0:
        return query_params['v'][0]
    else:
        return None
