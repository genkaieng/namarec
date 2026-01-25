import shutil
import subprocess
import threading
from pathlib import Path
from parsers import get_lvid


TMP_DIR = "./tmp"
OUTPUT_DIR = "./dist"


# tmp/がなければ作る
def mkdirTmp():
    Path(TMP_DIR).mkdir(parents=True, exist_ok=True)


# dist/がなければ作る
def mkdirDist():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def start_rec(url, file_name, user_session):
    print("start recording...")

    lvid = get_lvid(url)
    tmp_filepath = Path(TMP_DIR) / f"{lvid}.mp4"
    output_filepath = Path(OUTPUT_DIR) / file_name

    mkdirTmp()

    niconico_user_session = []
    if user_session is not None:
        niconico_user_session = [f"--niconico-user-session={user_session}"]
    streamlink_cmd = [
        "streamlink",
        *niconico_user_session,
        url,
        "best",
        "-O",
    ]
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        "pipe:0",
        "-c", "copy",
        "-f", "mp4",
        "-y",
        str(tmp_filepath),
    ]

    p_stream = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE)
    p_ffmpeg = subprocess.Popen(ffmpeg_cmd, stdin=p_stream.stdout)
    if p_stream.stdout is not None:
        p_stream.stdout.close()

    def watch():
        code_stream = p_stream.wait()
        code_ffmpeg = p_ffmpeg.wait()
        if code_stream == 0 and code_ffmpeg == 0:
            mkdirDist()
            shutil.move(tmp_filepath, output_filepath)
    threading.Thread(target=watch, daemon=True).start()

    return p_stream
