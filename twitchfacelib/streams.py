import os
import requests
import numpy as np
import face_recognition

from PIL import Image
from io import BytesIO

from .twitch_api import TwitchAPI

class Stream(object):
    def __init__(self, channel: str, vid: str, faceloc: tuple,
                duration: int = 10, quality: str = 'best',
                oauth: str = None):
        self.channel = channel
        self.url = f'https://twitch.tv/{channel}'
        self.vid = vid
        self.faceloc = faceloc
        self.duration = duration
        self.quality = quality
        self.oauth = oauth

    def _args(self) -> list:
        params = {'hls-timeout': 60,
                  'hls-segment-timeout': 60,
                  'hls-segment-attempts': 5,
                  }

        if self.oauth:
            params['twitch-oauth-token'] = self.oauth

        return [f'--{key}={value}' for key, value in params.items()]



def get_active_streams():
    api = TwitchAPI()
    streams = api.helix('streams', **{'first': 20})['data']
    print('retrieved {0} active streams'.format(len(streams)))
    face_streams = []
    for stream in streams:
        faces = detect_face(stream)
        if len(faces) == 1:
            print("detected a face on {0}'s Stream".format(stream['user_name']))
            face_streams.append(Stream(stream['user_name'], stream['id'], faces))
    print('detected {0} active streams with face cam'.format(len(face_streams)))

    return face_streams


def detect_face(stream, size = (1920, 1080)):
    url = stream['thumbnail_url'].format(width = size[0], height = size[1])
    file = '{0}.jpg'.format(stream['id'])
    # with open(file, 'wb') as handle:
    response = requests.get(url, stream=True)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    #     for block in response.iter_content(1024):
    #         if not block:
    #             break
    #         handle.write(block)
    # img = face_recognition.load_image_file(file)
    # os.remove(file)
    faceloc = face_recognition.face_locations(img)

    return faceloc


