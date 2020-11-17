import os
from time import sleep
from subprocess import Popen, PIPE
from multiprocessing import Process
import dateutil.parser as dateparser

from twitch_api import TwitchAPI
from streams import get_active_streams

class Stream(object):
    def __init__(self, url: str, quality: str = 'best',
                 threads: int = 1, oauth: str = None):
        self.url = url
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

    def download(self, channel: str, dest: str):
        if not os.path.exists(f'data/{channel}'):
            os.makedirs(f'data/{channel}')
        print(f'Downloading `{self.url}` into {dest}')

        sl_cmd = ['streamlink', '-l', 'debug']
        sl_cmd += self._args()
        sl_cmd += [self.url, self.quality, '-O']

        with open(f'data/{channel}/{dest}', 'wb') as fo:
            sl_kwargs = {'stdout': fo,
                         'stderr': PIPE}
            sl_proc = Popen(sl_cmd, **sl_kwargs)
            sl_proc.wait()

            if sl_proc.returncode != 0:
                print(f'WARN: `{sl_cmd}` exited with non-zero '
                      f'code ({sl_proc.returncode})')
                sys.exit(sl_proc.returncode)
def main():
    api = TwitchAPI()
    streams = get_active_streams()
    for s in streams:
        channel = s['user_name']
        vods = api.helix('videos', user_id=s['user_id'],
                         first=1, type='archive')['data']

        if len(vods) == 0:
            print(f'ERR: No VODs found on channel')
            sys.exit(1)

        stream_date = dateparser.isoparse(s['started_at'])
        vod_date = dateparser.isoparse(vods[0]['created_at'])

        if vod_date < stream_date:
            print(f'ERR: Live VOD is not available yet')
            sys.exit(1)

        v = vods[0]["id"]

        stream = Stream(f'https://twitch.tv/{channel}',
                        quality= 'best',
                        threads=1)

        print('Starting to record the live stream...')
        p_stream = Process(target=stream.download, args=(channel, f'{v}.ts',))
        p_stream.start()

        p_stream.join()
        sleep(10)

    print("got to this pint")
    p_stream.close()

    print('Stream ended')


if __name__ == '__main__':
    main()
