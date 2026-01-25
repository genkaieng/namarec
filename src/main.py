import subprocess
import time
import os
from dotenv import load_dotenv

from parsers import get_live_url, get_userid

load_dotenv()

active_procs = []


def rec(url):
    print("start recording...")
    return subprocess.Popen(["nldl", url])


def check_userid(user_id):
    v = os.getenv("NAMAREC_USER_ID_LIST")
    if v is not None:
        if v.split(",") in user_id:
            return True
    return False


def run():
    p = subprocess.Popen(
        ["nicopush", "subscribe"],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    assert p.stdout is not None
    for line in p.stdout:
        print(line)
        userid = get_userid(line)
        if userid is None:
            continue
        if not check_userid(userid):
            continue
        url = get_live_url(line)
        if url is None:
            continue
        proc = rec(url)
        active_procs.append(proc)
        active_procs[:] = [p for p in active_procs if p.poll() is None]

    return p.wait()


while True:
    code = run()
    print(f"process exited: {code}, restarting...")
    time.sleep(1)
