import json
import spotipy
import webbrowser
import time

username = '31udbix627s4wm3uky4gcjg5fp5q'
clientID = '911feac999f345f9a24c72cc94aa32db'
clientSecret = '4c1d601467f44daeb752726a6af48131'
redirectURI = 'http://google.com/' 
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
# To print the response in readable format.
print(json.dumps(user,sort_keys=True, indent=4))
while True:
    res="What song do you want to me play?"
    song_name=ai.text_to_speech(res)
    if song_name== True:
        # Get the Song Name.
        searchQuery = song_name
        # Search for the Song.
        searchResults = spotifyObject.search(searchQuery,1,0,"track")
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        webbrowser.open(song)
        print('Song has opened in your browser.')
        time.sleep(180)
        res="do you want to continue?"
        decision=ai.text_to_speech(res)
        if decision==yes:
            pass
        else:
            break