from requests import Session
import requests
import json

client_id = 'i46n02109k2dwzjjixo6qpah3a8xtu'
client_secret = 'l0ketr91icxhhyl4is5qb4glnt12gj'
id_url_base = 'https://id.twitch.tv/'
api_url_base = 'https://api.twitch.tv/'

def get_app_token(url, client_id, secret):
    params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
    response = requests.post('{0}oauth2/token'.format(id_url_base), params=params)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['access_token']
    else:
        return None

class TwitchAPI:
    @staticmethod
    def _session(token: str) -> Session:
        s = Session()
        s.headers['Acccept'] = 'application/vnd.twitchtv.v5+json'
        s.headers['Client-ID'] = 'i46n02109k2dwzjjixo6qpah3a8xtu'
        s.headers['Authorization'] = f'Bearer {token}'
        return s

    def __init__(self):
        self.oauth = get_app_token(id_url_base, client_id, client_secret)
        self.session = self._session(self.oauth)


    def get(self, namespace: str, method: str, **payload):
        url = f'https://api.twitch.tv/{namespace}/{method}'

        if len(payload.keys()) > 0:
            params = '&'.join([f'{k}={v}' for k, v in payload.items()])
            url += '?' + params

        res = self.session.get(url)

        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(res.text)

    def helix(self, method: str, **payload):
        return self.get('helix', method, **payload)
