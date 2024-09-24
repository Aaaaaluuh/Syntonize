# from dotenv import load_dotenv
# import os
# import base64
# from requests import post, get
# import json
# from spotipy.oauth2 import SpotifyOAuth
# import streamlit as st
# import requests


##### ESSA AUTENTICAÇÃO É MINHA PRÓPRIA #####
# def user_configs():
#     user_config = st.secrets["client"]

#     client_id = user_config['CLIENT_ID']
#     client_secret = user_config['CLIENT_SECRET']

#     return client_id, client_secret

# def get_token():
#     client_id, client_secret = user_configs()
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
# def get_recommendations(token, limit=10, seed_genres=None, features={}):
#     url = "https://api.spotify.com/v1/recommendations"
#     headers = get_auth_header(token)
    
#     # Parâmetros de consulta com opção de incluir gêneros
#     params = {
#         "limit": limit,  # Define quantas músicas você quer retornar
#     }
    
#     # Incluir gêneros, se fornecidos
#     if seed_genres:
#         params["seed_genres"] = ','.join(seed_genres)
    
#     # Adicionar as features selecionadas aos parâmetros, se fornecidas
#     for feature, value in features.items():
#         params[f"target_{feature}"] = value
    
#     # result = get(url, headers=headers, params=params)
#     # json_result = json.loads(result.content)
#     # return json_result["tracks"]

#     result = requests.get(url, headers=headers, params=params)

#     # Verificar se a requisição foi bem-sucedida
#     if result.status_code != 200:
#         st.error(f"Erro na requisição: {result.status_code}")
#         st.write(result.json())  # Para depuração
#         return []

#     # Processar a resposta
#     json_result = result.json()

#     if 'tracks' in json_result:
#         return json_result["tracks"]
#     else:
#         st.warning("Nenhuma recomendação encontrada.")
#         st.write(json_result)  # Mostrar o JSON completo para depuração
#         return []


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



# # Interface em Streamlit
# st.title("Syntonize")

# # Inputs do usuário
# st.header("Escolha as características das músicas")

# # Características das músicas (features)
# danceability = st.slider("Selecione a Dançabilidade:", 0.0, 1.0, 0.5)
# energy = st.slider("Selecione a Energia:", 0.0, 1.0, 0.5)
# # acousticness = st.slider("Selecione a Acusticidade:", 0.0, 1.0, 0.5)
# instrumentalness = st.slider("Selecione a Instrumentalidade:", 0.0, 1.0, 0.5)
# speechiness = st.slider("Selecione a quantidade de fala:", 0.0, 1.0, 0.5)

# # Seleção de gêneros
# genres = st.multiselect(
#     "Selecione até 5 gêneros musicais que você deseja",
#     ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "blues", 
#      "bossanova", "brazil", "breakbeat", "chill", "classical", "club", "country", "dance", "dancehall", "death-metal", 
#      "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dubstep", "electro", "electronic", "emo", "folk", 
#      "forro", "funk", "gospel", "goth", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle",
#      "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", 
#      "iranian", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "metal", "metal-misc", "metalcore", "minimal-techno", "mpb", 
#      "new-age", "new-release", "opera", "pagode", "party", "piano", "pop", "post-dubstep", "progressive-house", "punk", "punk-rock",
#      "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "romance", "sad", "salsa", "samba", "sertanejo", "sleep", "soul", 
#      "soundtracks", "spanish", "study", "summer", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]
# )

# # Botão para gerar recomendações
# if st.button("Gerar Recomendação"):
#     token = get_token()
    
#     # Criando dicionário de features apenas com os valores fornecidos
#     features = {
#         "danceability": danceability,
#         "energy": energy,
#         # "acousticness": acousticness,
#         "instrumentalness": instrumentalness,
#         "speechiness": speechiness
#     }
    
#     # Removendo as features que não foram ajustadas
#     features = {k: v for k, v in features.items() if v is not None}
#     st.write(features)

#     # Verificação de gênero antes da chamada
#     if genres:
#         tracks = get_recommendations(token, seed_genres=genres, features=features)
#     else:
#         tracks = get_recommendations(token, features=features)
    
#     # Exibindo as músicas recomendadas
#     st.header("Músicas Recomendadas")
#     if tracks:
#         for track in tracks:
#             st.write(f"{track['name']} by {track['artists'][0]['name']}")
#     else:
#         st.write("Nenhuma música encontrada com essas características.")



# token = get_token()
# result = search_for_atist(token, "gerard way")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)

# for idx, song in enumerate(songs):
#     print(f"{idx+1}. {song['name']}")

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

########################################################################################################################################



########################################################################################################################################
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import requests
import jwt
import datetime

# Acessar as variáveis diretamente de st.secrets
CLIENT_ID = st.secrets["client"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["client"]["CLIENT_SECRET"]
REDIRECT_URI = 'https://syntonize.streamlit.app'

# Configuração do OAuth
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read user-top-read playlist-modify-private"
)
# Chave secreta para o JWT
JWT_SECRET = "sua_chave_secreta"

# Função para criar token JWT
def create_jwt(user_id, access_token):
    payload = {
        'user_id': user_id,
        'access_token': access_token,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira em 1 hora
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

# Função para decodificar o token JWT
def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado

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

    # Verificar se já existe um token JWT salvo (usuário autenticado)
    jwt_token = st.session_state.get('jwt_token')
    
    if jwt_token:
        # Decodificar o JWT e usar o token de acesso para fazer requisições
        payload = decode_jwt(jwt_token)
        
        if payload:
            access_token = payload['access_token']
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
        else:
            st.error("Sessão expirada. Por favor, faça login novamente.")
    else:
        # Link para login via Spotify
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[Clique aqui para se autenticar via Spotify]({auth_url})")

        # Obter código de autorização após o login
        code = st.experimental_get_query_params().get('code')
        
        if code:
            token_info = sp_oauth.get_access_token(code)
            print(token_info)
            access_token = token_info['access_token']
            user_id = token_info['user_id']

            # Gerar JWT e salvar na sessão
            jwt_token = create_jwt(user_id, access_token)
            st.session_state['jwt_token'] = jwt_token

            st.experimental_rerun()  # Recarregar a página para usar o token JWT

# Rodar a aplicação Streamlit
if __name__ == '__main__':
    main()
