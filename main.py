from dotenv import load_dotenv
from requests import post, get
import base64
import json
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = result.json()

    return json_result.get("access_token")


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = result.json()

    return json_result


def input_artist():
    token = get_token()
    json_result = search_for_artist(token, input("Informe artista: "))
    
    return json_result


def artist_info(json_result):
    artist = json_result['artists']['items'][0]

    artist_info = [
        artist['id'],
        artist['genres'],
        artist['followers']['total'],
        artist['popularity']
    ]
    return artist_info


def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = result.json()
        albums =  json_result.get("items", [])
        sorted_albums = sorted(albums, key=lambda x: x['release_date'])
        return sorted_albums
    else:
        print(f"Erro ao obter álbuns: {result.status_code} - {result.text}")
        return []


def print_artist_info():
    json_result = input_artist()
    
    info = artist_info(json_result)

    artist_id = info[0]
    
    token = get_token()
    albums = get_albums_by_artist(token, artist_id)

    print("\nInformações do artista:\n")
    print(f"ID do artista: {info[0]}")
    print(f"Gêneros: {', '.join(info[1])}")
    print(f"Total de seguidores: {info[2]}")
    print(f"Popularidade: {info[3]}")
    
    print("\nÁlbuns do artista:\n")
    if albums:
        for album in albums:
            print(f"- {album['name']} ({album['release_date']})")
    else:
        print("Nenhum álbum encontrado.")

print_artist_info()
