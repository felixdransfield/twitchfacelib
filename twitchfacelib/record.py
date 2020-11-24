
"""Usage: twitchfacelib record [options] --oauth=<token> [--] <channel>
Parameters:
  channel       Name of the channel. Can be found in the URL: twitch.tv/<channel>
  quality       Resolution and framerate of the recording. To get all available
                values use `streamlink https://twitch.tv/<channel>`.
Options:
  --oauth <token>   Twitch OAuth token. You need to extract it from the site's
                    cookie named "auth-token".
  -o <name>         Name of the output file. For more information see
                    `twitch_utils concat --help`.
  -j <threads>      Number of simultaneous downloads of live segments. [default: 4]
  -y, --force       Overwrite output file without confirmation.
  --debug           Forward output of streamlink and ffmpeg to stderr.
"""

import os
import time
from multiprocessing import Pool
from subprocess import run, Popen, PIPE
from .streams import get_active_streams

def download(Stream):
        if not os.path.exists(f'twitchfacelib/data/{Stream.channel}'):
            os.makedirs(f'twitchfacelib/data/{Stream.channel}')
        print(f'Downloading `{Stream.url}` into twitchfacelib/data/{Stream.channel}/{Stream.vid}.ts')
        sl_cmd = ['streamlink', '-l', 'debug']
        sl_cmd += Stream._args()
        sl_cmd += [Stream.url, Stream.quality, '-O']

        infile = f'twitchfacelib/data/{Stream.channel}/{Stream.vid}.ts'
        outfile = f'twitchfacelib/data/{Stream.channel}/{Stream.vid}.mp4'
        ffmpeg_cmd = ['ffmpeg', '-i', infile, outfile]

        with open(infile, 'wb') as fo:
            sl_kwargs = {'stdout': fo,
                         'stderr': PIPE}
            sl_proc = Popen(sl_cmd, **sl_kwargs)
            time.sleep(Stream.duration)
            sl_proc.terminate()
            print(f"recorded for {Stream.duration} minute(s)")


        # print("Converting to mp4")
        # ffmpeg_proc = run(ffmpeg_cmd)
        # print(ffmpeg_proc)
        # if ffmpeg_proc.returncode == 0:
        #     ffmpeg_proc.terminate()




def main(argv=None):
    streams = get_active_streams()
    a_pool = Pool()
    a_pool.map(download, streams)
    a_pool.terminate()
    print("done")





if __name__ == '__main__':
    main()
