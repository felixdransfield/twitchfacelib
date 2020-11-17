import os
import requests
import face_recognition
from twitch_api import TwitchAPI


def get_active_streams(size = (500, 500)):
    api = TwitchAPI()
    streams = api.helix('streams')['data']
    print('retrieved {0} active streams'.format(len(streams)))
    face_streams = [stream for stream in streams if detect_face(stream, size)]
    print('detected {0} active streams with face cam'.format(len(face_streams)))

    return face_streams


def detect_face(stream, size):
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

#t = get_active_streams()

#print(t)

