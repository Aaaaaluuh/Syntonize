# from dotenv import load_dotenv
# import os
# import base64
# from requests import post, get
# import json
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth


# load_dotenv()

# client_id = os.getenv('CLIENT_ID')
# client_secret = os.getenv('CLIENT_SECRET')

# # pegando o token de acesso temporário
# # Primeiro, é necesário fazer um request body -> grant type com as credenciais do client

# def get_token():
#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization" : "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}

#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):
#     return{"Authorization": "Bearer " + token}


# # até aqui era pra conseguir o token temporário de acesso a api do spotify
# # a partir de agora vai ter uma função que nos permite pesquisar por artistas e conseguir as top tracks do artista
# def search_for_atist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"

#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]
#     if len(json_result) == 0:
#         print("n tem artista com esse nome")
#         return None
#     return json_result[0]

# def get_songs_by_artist(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?coutntry=BR"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)["tracks"]
#     return json_result


# # Aqui é a função principal 
# def get_recommendations(token, seed_genres=None, features={}):
#     url = "https://api.spotify.com/v1/recommendations"
#     headers = get_auth_header(token)
    
#     # Parâmetros de consulta com opção de incluir gêneros
#     params = {
#         "limit": 10,  # Define quantas músicas você quer retornar
#     }
    
#     # Incluir gêneros, se fornecidos
#     if seed_genres:
#         params["seed_genres"] = ','.join(seed_genres)
    
#     # Adicionar as features selecionadas aos parâmetros, se fornecidas
#     for feature, value in features.items():
#         params[f"target_{feature}"] = value
    
#     result = get(url, headers=headers, params=params)
#     json_result = json.loads(result.content)
#     return json_result["tracks"]


# def create_playlist(token, user_id, name="Recomendações do App"):
#     url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
#     headers = get_auth_header(token)
#     data = {
#         "name": name,
#         "description": "Playlist criada com recomendações do app",
#         "public": False  # ou True se você quiser que a playlist seja pública
#     }
#     response = post(url, headers=headers, json=data)
#     playlist_id = json.loads(response.content)["id"]
#     return playlist_id


# def add_tracks_to_playlist(token, playlist_id, track_uris):
#     url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
#     headers = get_auth_header(token)
#     data = {
#         "uris": track_uris
#     }
#     post(url, headers=headers, json=data)



# token = get_token()
# result = search_for_atist(token, "gerard way")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)

# # for idx, song in enumerate(songs):
# #     print(f"{idx+1}. {song['name']}")



# # O usuário pode selecionar apenas algumas features e gêneros, ou nenhum
# features = {
#     "danceability": 0.8,  # Somente danceability é fornecido
#     "acousticness": 0.5,  # Deixe como comentário ou remova se não quiser especificar
#     "energy": 0.1,  # Opcional
# }

# genres = None
# # genres = ["metalcore", "pop"]  

# if genres:
#     tracks = get_recommendations(token, seed_genres=genres, features=features)
# else:
#     tracks = get_recommendations(token, features=features)


# for track in tracks:
#     print(f"{track['name']} by {track['artists'][0]['name']}")



# # Após obter as recomendações
# playlist_id = create_playlist(token, user_id)
# track_uris = [track['uri'] for track in tracks]
# add_tracks_to_playlist(token, playlist_id, track_uris)




import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a autenticação do Spotify
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8502/"  # Usado pelo Spotify para redirecionar após login

# Definir os escopos que queremos do usuário
scope = "user-library-read user-top-read playlist-modify-private"

# Inicializa a autenticação OAuth do Spotipy
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
)

# Função para obter o token de acesso
def get_token():
    token_info = sp_oauth.get_access_token(as_dict=False)
    return token_info

# Função para criar header de autenticação
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Função para buscar recomendações de músicas
def get_recommendations(token, seed_genres=None, features=None):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    
    params = {
        "seed_genres": ",".join(seed_genres) if seed_genres else "",
        "limit": 10
    }
    
    # Adiciona features, se forem fornecidas
    if features:
        params.update(features)
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()["tracks"]

# Função para criar playlist no Spotify
def create_playlist(token, user_id, playlist_name):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    data = json.dumps({
        "name": playlist_name,
        "description": "Playlist gerada automaticamente",
        "public": False
    })
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Função principal da interface em Streamlit
def main():
    st.title("Recomendações de Músicas do Spotify")

    # Link para login via Spotify
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[Clique aqui para se autenticar via Spotify]({auth_url})")

    # Obter código de autorização após o login
    code = st.query_params['code']
    
    if code:
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)

        # Pegar dados do usuário
        user_info = sp.current_user()
        st.write(f"Bem-vindo, {user_info['display_name']}!")

        # Escolha de gêneros e características
        seed_genres = st.multiselect("Escolha gêneros", ['pop', 'rock', 'jazz', 'classical', 'hip-hop'])
        acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5)
        danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
        energy = st.slider("Energy", 0.0, 1.0, 0.5)

        # Exibir recomendações com base nas opções do usuário
        if st.button("Mostrar Recomendações"):
            features = {
                "acousticness": acousticness,
                "danceability": danceability,
                "energy": energy
            }
            tracks = get_recommendations(access_token, seed_genres, features)
            for track in tracks:
                st.write(track['name'], "-", track['artists'][0]['name'])

        # Criar playlist baseada nas recomendações
        if st.button("Criar Playlist"):
            playlist = create_playlist(access_token, user_info['id'], "Minhas Recomendações")
            st.write(f"Playlist criada: {playlist['external_urls']['spotify']}")

# Rodar a aplicação Streamlit
if __name__ == '__main__':
    main()
