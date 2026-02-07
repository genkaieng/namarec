import shutil
import signal
import subprocess
import threading
from pathlib import Path
from dotenv import load_dotenv

from utils import safe_filename

load_dotenv()

INPUT_FILE = Path("logs") / "lvids"
INPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
INPUT_FILE.touch(exist_ok=True)

DIST_DIR = Path("dist")

NICOLIVE_BASE_URL = "https://live.nicovideo.jp/watch/"

# プロセスを保持
proc = []
p_tail = None


# ===============================================
# 終了処理
# ===============================================
def shutdown(_signum, _frame):
    print("Shutting down...")

    # 録画プロセスを終了
    for p in proc:
        p.kill()

    # tailプロセスを終了
    if p_tail is not None:
        p_tail.kill()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


# ===============================================
# tail → 録画処理
# ===============================================
def start_rec(lvid, filename: str):
    print(f"start recording: {lvid}")

    url = NICOLIVE_BASE_URL + lvid
    streamlink_cmd = [
        "streamlink",
        url,
        "best",
        "-O",
    ]
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        "pipe:0",
        "-c",
        "copy",
        "-f",
        "mp4",
        "-y",
        f"{lvid}.mp4",
    ]
    p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(ffmpeg_cmd, stdin=p1.stdout)

    proc.append(p1)

    def watch():
        p1.wait()
        p2.wait()
        shutil.move(f"{lvid}.mp4", DIST_DIR / filename)
        print(f"[OK] {DIST_DIR / filename}")

    threading.Thread(target=watch, daemon=True).start()


p = subprocess.Popen(["tail", "-F", INPUT_FILE], stdout=subprocess.PIPE, text=True)
p_tail = p

assert p.stdout is not None
for line in p.stdout:
    [lvid, *slugs] = line.strip().split(",")
    filename = safe_filename("_".join([*slugs, lvid]) + ".mp4")

    start_rec(lvid=lvid, filename=filename)
