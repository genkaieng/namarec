import subprocess
import time
import os
import signal
from dotenv import load_dotenv

from parsers import get_live_url, get_userid

load_dotenv()

subscribe_proc = None
rec_procs = []
processing = True


def rec(url):
    print("start recording...")
    return subprocess.Popen(["nldl", url])


def check_userid(user_id):
    v = os.getenv("NAMAREC_USER_ID_LIST")
    if v is not None:
        list = v.strip().split(",")
        if user_id in list:
            return True
    return False


def shutdown(_signum, _frame):
    print("shutting down...")

    global processing
    processing = False

    if subscribe_proc is not None and subscribe_proc.poll() is not None:
        subscribe_proc.kill()
    for p in rec_procs:
        if p is not None and p.poll() is not None:
            p.kill()


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
