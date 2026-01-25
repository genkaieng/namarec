import subprocess
import time
import os
import signal
from dotenv import load_dotenv

from parsers import get_live_url, get_userid
from utils import contains

load_dotenv()
print("NAMAREC_USER_ID_LIST", os.getenv("NAMAREC_USER_ID_LIST"))

subscribe_proc = None
rec_procs = []
processing = True


def rec(url):
    print("start recording...")
    return subprocess.Popen(["nldl", url])


def check_userid(user_id):
    list = os.getenv("NAMAREC_USER_ID_LIST")
    return list is not None and contains(user_id, list)


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
        text=True,
        bufsize=1,
    )
    subscribe_proc = p

    assert p.stdout is not None
    for line in p.stdout:
        if not processing:
            break
        print(line)
        userid = get_userid(line)
        url = get_live_url(line)
        if userid is None or url is None:
            continue
        if not check_userid(userid):
            continue
        proc = rec(url)
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
