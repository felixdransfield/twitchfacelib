import os
import requests
import face_recognition

from .twitch_api import TwitchAPI

class Stream(object):
    def __init__(self, channel: str, vid: str, quality: str = 'best',
                 threads: int = 1, oauth: str = None):
        self.channel = channel
        self.url = f'https://twitch.tv/{channel}'
        self.vid = vid
        self.quality = quality
        self.threads = threads
        self.oauth = oauth

    def _args(self) -> list:
        params = {'hls-timeout': 60,
                  'hls-segment-timeout': 60,
                  'hls-segment-attempts': 5,
                  'hls-segment-threads': self.threads}

        if self.oauth:
            params['twitch-oauth-token'] = self.oauth

        return [f'--{key}={value}' for key, value in params.items()]



def get_active_streams():
    api = TwitchAPI()
    streams = api.helix('streams', **{'first': 20})['data']
    print('retrieved {0} active streams'.format(len(streams)))
    face_streams = [Stream(stream['user_name'], stream['id']) for stream in streams if detect_face(stream)]
    print('detected {0} active streams with face cam'.format(len(face_streams)))

    return face_streams


def detect_face(stream, size = (500, 500)):
    face = False
    url = stream['thumbnail_url'].format(width = size[0], height = size[1])
    file = '{0}.jpg'.format(stream['id'])
    with open(file, 'wb') as handle:
        response = requests.get(url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    img = face_recognition.load_image_file(file)
    os.remove(file)
    faces = face_recognition.face_locations(img)
    if len(faces) == 1:
        print("detected a face on {0}'s Stream".format(stream['user_name']))
        face = True

    return face


