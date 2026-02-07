import os
import signal
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from parsers import parse_nicopush_uaid, parse_notification
from utils import contains

load_dotenv()
NAMAREC_USER_ID_LIST = os.getenv("NAMAREC_USER_ID_LIST")
print("NAMAREC_USER_ID_LIST={NAMAREC_USER_ID_LIST}")

OUTPUT_FILE = Path("logs") / "lvids"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.touch(exist_ok=True)

# プロセスとステータスを保持
processing = True
proc = None

env = os.environ.copy()


# ===============================================
# 終了処理
# ===============================================
def shutdown(_signum, _frame):
    print("Shutting down...")

    global processing
    processing = False
    if proc is not None:
        proc.kill()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


# ===============================================
# プッシュ通知受信 → フィルタ → 書き出し
# ===============================================
exists_lvids = []  # 既に書き出し済みのlvidを保持（重複チェックに使う）

while processing:
    p = subprocess.Popen(
        ["nicopush", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    proc = p

    assert p.stdout is not None
    for line in p.stdout:
        print(line)

        info = parse_notification(line)
        if info is None:
            uaid = parse_nicopush_uaid(line)
            if uaid is not None:
                # UAIDを取得（次回から指定する）
                env["NICOPUSH_UAID"] = uaid
            continue

        # 重複チェック
        if info["lvid"] in exists_lvids:
            continue
        if NAMAREC_USER_ID_LIST is not None and contains(
            info["userid"], NAMAREC_USER_ID_LIST
        ):
            row = ",".join(
                [
                    info["lvid"],
                    info["timestamp"].split("T")[0].replace("-", ""),
                    info["live_title"],
                    info["user_name"],
                ]
            )
            os.system(f"echo {row} >> {OUTPUT_FILE}")
            exists_lvids.append(info["lvid"])

    p.wait()
