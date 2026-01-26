import os
import signal
import subprocess
from dotenv import load_dotenv

from parsers import parse_nicopush_uaid, parse_notification
from utils import contains

load_dotenv()
NAMAREC_USER_ID_LIST = os.getenv("NAMAREC_USER_ID_LIST")

processing = True
proc = None

env = os.environ.copy()


def shutdown(_signum, _frame):
    print("Shutting down...")

    global processing
    processing = False
    if proc is not None:
        proc.kill()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

while processing:
    p = subprocess.Popen(
        ["nicopush", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )
    proc = p

    assert p.stdout is not None
    for line in p.stdout:
        print(line)

        info = parse_notification(line)
        if info is None:
            uaid = parse_nicopush_uaid(line)
            if uaid is not None:
                # 次回から指定するUAIDを取得
                env["NICOPUSH_UAID"] = uaid
            continue

        if contains(info["userid"], NAMAREC_USER_ID_LIST):
            row = ",".join([
                info["lvid"],
                info["date"].replace("/", ""),
                info["live_title"],
                info["user_name"],
            ])
            os.system(f"echo {row} >> nicolive.csv")

    p.wait()
