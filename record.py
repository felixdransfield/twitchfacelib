import os
import sys
from multiprocessing import Pool
from subprocess import Popen, PIPE

from streams import get_active_streams

def download(Stream):
        if not os.path.exists(f'data/{Stream.channel}'):
            os.makedirs(f'data/{Stream.channel}')
        print(f'Downloading `{Stream.url}` into data/{Stream.channel}/{Stream.vid}.ts')
        sl_cmd = ['streamlink', '-l', 'debug']
        sl_cmd += Stream._args()
        sl_cmd += [Stream.url, Stream.quality, '-O']

        with open(f'data/{Stream.channel}/{Stream.vid}.ts', 'wb') as fo:
            sl_kwargs = {'stdout': fo,
                         'stderr': PIPE}
            sl_proc = Popen(sl_cmd, **sl_kwargs)
            sl_proc.wait()

            if sl_proc.returncode != 0:
                print(f'WARN: `{sl_cmd}` exited with non-zero '
                      f'code ({sl_proc.returncode})')
                sys.exit(sl_proc.returncode)

def main():
    streams = get_active_streams()
    a_pool = Pool()
    a_pool.map(download, streams)




if __name__ == '__main__':
    main()
