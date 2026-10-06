import requests
from typing import Dict, Tuple

BASE_URL = "https://www.theaudiodb.com/api/v1/json/123/" # 123 is the test key

DEFAULT_HEADERS = {
    "User-Agent": "test.py/1.0 (Python requests script for class project)"
}

def display_artist_info(album: Dict) -> None:
    title = f"{album['strAlbum']} by {album['strArtist']}"
    print(title)
    print("-" * len(title))
    print(f"{'Year:':<8}{album['intYearReleased']}")
    print(f"{'Genre:':<8}{album['strGenre']}")
    print(f"{'Label:':<8}{album['strLabel']}")


def get_request(url: str,
                headers: Dict[str, str]=DEFAULT_HEADERS,
                params: Dict={},
                timeout: int=10) -> Tuple[bool, int, Dict]:
    """
    Args:
        url (str): The path to be appended to the BASE_URL - should not start with slash
        headers (dict): The HTTP headers dictionary
        params (dict): Parameters to build the query string
        timeout (int): How many seconds the client will wait for the server to est. a connection or send data back before throwing an error

    Returns:
        tuple: A tuple of length 3 containing resp.ok (bool), resp.status_code (int), and a dictionary representing the JSON response
        body (or empty if the response body could not be parsed using the json() method)
    """
    resp = requests.get(BASE_URL + url, headers=headers, params=params, timeout=timeout)
    if resp.ok: # Ok == True for any HTTP status code from 200-399
        try: return resp.ok, resp.status_code, resp.json() # Return the JSON parsed into a Python dict
        except: return resp.ok, resp.status_code, {} # Return empty dict if json() fails
    else:
        return resp.ok, resp.status_code, {}

def search_artist_album(artist: str, album: str) -> Tuple[bool, int, Dict]:

    return get_request(url="searchalbum.php", params={"s": artist.lower(), "a": album})


def main():
    ok_status, status_code, response = search_artist_album('Daft Punk', 'Homework')
    print(f"Successful: {ok_status} - {status_code}")

    if 'album' in response.keys():
        try:
            response_dict = response['album'][0]
            display_artist_info(response_dict)
        except TypeError as t:
            print("Album not found")
    else:
        print("album key not there")

if __name__ == "__main__":
    main()
