
import json
import webbrowser
from tqdm import tqdm
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

openai.api_key = os.getenv('OPENAI_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

SCOPE = "user-library-read user-library-modify app-remote-control streaming playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

def get_songs_list(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    functions = [
        {
            "name": "get_songs_name_list",
            "description": "Generate songs names based on prompt, 10 to 30",
            "parameters": {
                "type": "object",
                "properties": {
                    "names": {
                        "type": "array",
                        "description": "songs names",
                        "items": {
                            "type": "string"
                        }
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the playlist I will create for that songs"
                    }
                },
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    
    try:
        args = json.loads(response_message['function_call']['arguments'])
        names = args['names']
        title = args['title']
        return names, title
    except:
        return []



def main():
    while True:
        prompt = input('What playlist do you want to generate? (press q to exit) ')
        if prompt == 'q':
            break
        print(f'Sending prompt: {prompt}')
        print('Generating playlist...')
        names, title = get_songs_list(prompt)
        user = sp.current_user()
        resp = sp.user_playlist_create(user=user['id'], name=title, public=False)
        playlist_id = resp['id']
        playlist_url = resp['external_urls']['spotify']

        tracks = []
        for name in tqdm(names):
            resp = sp.search(q=name, limit=1)
            item = resp['tracks']['items'][0]
            item_uri = item['uri']
            tracks.append(item_uri)
        sp.playlist_add_items(playlist_id, items=tracks)
        try:
            # will failed if not playing something currenly
            sp.start_playback(context_uri=f'spotify:playlist:{playlist_id}')
        except:
            pass
        webbrowser.open(playlist_url)

main()