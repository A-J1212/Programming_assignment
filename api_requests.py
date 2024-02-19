import requests
import yaml 
from pprint import pprint

# Load secrets from a YAML file
with open('secrets.yml', 'r') as file:
    secrets = yaml.safe_load(file)

client_id = secrets['Client_ID']
client_secret = secrets['Client_secret']
redirect_uri = 'http://localhost:3000'
scope = 'user-read-private'

# Spotify URL for authentication
AUTH_URL = 'https://accounts.spotify.com/api/token'

# Make a POST request to get the access token
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

# Convert the response to JSON
auth_response_data = auth_response.json()

# Save the access token
access_token = auth_response_data['access_token']

# Base URL for Spotify API
BASE_URL = 'https://api.spotify.com/v1/'

# Use the access token to access the Spotify Web API; this example searches for "The Beatles".
headers = {
    'Authorization': f'Bearer {access_token}',
}
response = requests.get(BASE_URL + 'search', headers=headers, params={'q': 'The Beatles', 'type': 'artist'})

# This is the response from the API
response_data = response.json()


# Example of parsing the artist data
artists = response_data['artists']['items']

for artist in artists:
    print(f"Artist Name: {artist['name']}, Popularity: {artist['popularity']}, Link: {artist['external_urls']['spotify']}")
