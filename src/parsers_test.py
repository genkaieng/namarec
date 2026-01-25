import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from parsers import get_live_url, get_userid  # noqa: E402

NOTIFICATION = '2026/01/25 10:42:03 INFO notification {"body":"「おはよう」を放送","data":{"created_at":"2026-01-25T01:42:00Z","on_click":"https://live.nicovideo.jp/watch/lv349722646?from=webpush\u0026_topic=live_user_program_onairs","tracking_parameter":"live_onair-lv349722646-webpush-nico_account_webpush","ttl":600},"icon":"https://secure-dcdn.cdn.nimg.jp/nicoaccount/usericon/9221/92216320.jpg?1707704685","title":"きょろちゃんさんが生放送を開始"}'


def test_get_userid():
    userid = get_userid(NOTIFICATION)
    assert userid == "92216320"


def test_get_live_url():
    url = get_live_url(NOTIFICATION)
    assert url == "https://live.nicovideo.jp/watch/lv349722646"
