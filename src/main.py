import subprocess
import time
import os
import signal
from dotenv import load_dotenv

from rec import start_rec
from parsers import parse_notification
from utils import contains

load_dotenv()

NICOLIVE_SESSION = os.getenv("NICOLIVE_SESSION")
NAMAREC_USER_ID_LIST = os.getenv("NAMAREC_USER_ID_LIST")

print("[INFO]", "NAMAREC_USER_ID_LIST:", NAMAREC_USER_ID_LIST)

subscribe_proc = None
rec_procs = []
processing = True


# 録画対象のユーザーIDかチェック
def check_userid(user_id):
    if NAMAREC_USER_ID_LIST is None:
        return True
    return contains(user_id, NAMAREC_USER_ID_LIST)


def shutdown(_signum, _frame):
    print("Shutting down...")

    global processing
    processing = False

    for p in rec_procs:
        if p is not None and p.poll() is not None:
            p.kill()
    if subscribe_proc is not None and subscribe_proc.poll() is not None:
        subscribe_proc.kill()


def run():
    global subscribe_proc
    p = subprocess.Popen(
        ["nicopush", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    subscribe_proc = p

    assert p.stdout is not None
    for line in p.stdout:
        if not processing:
            break
        print(line)

        info = parse_notification(line)
        if info is None:
            continue
        if check_userid(info["userid"]):
            filename = "_".join([
                info["date"].replace("/", ""),
                info["live_title"],
                info["user_name"],
                info["lvid"]
            ])
            filename = f"{filename}.mp4"
            if info["live_url"] is not None:
                proc = start_rec(info["live_url"], filename, NICOLIVE_SESSION)
                if proc is None:
                    rec_procs.append(proc)
                    rec_procs[:] = [p for p in rec_procs if p.poll() is None]

    return p.wait()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

while processing:
    code = run()
    if not processing:
        break
    if processing:
        print(f"process exited: {code}, restarting...")
        time.sleep(1)

print("Bye")
