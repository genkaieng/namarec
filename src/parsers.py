import re


def get_userid(s: str):
    m = re.search(r'"icon":"([^"]+)"', s)
    if m is None:
        return None
    icon_url = m.group(1)
    m = re.search(r"(\d+)\.jpg", icon_url)
    if m is None:
        return None
    return m.group(1)


def get_live_url(s: str):
    m = re.search(r'"on_click":"([^"]+)"', s)
    if m is None:
        return None
    url = m.group(1)
    return url.split("?")[0]


def get_lvid(s: str):
    m = re.search(r"(lv\d+)", s)
    if m is None:
        return None
    lvid = m.group(1)
    return lvid


def get_live_title(s: str):
    m = re.search(r'"body":"([^"]+)"', s)
    if m is None:
        return None
    body = m.group(1)
    title = re.sub(r"」を放送", "", body[1:])
    return title


def get_user_name(s: str):
    m = re.search(r'"title":"([^"]+)"', s)
    if m is None:
        return None
    title = m.group(1)
    user_name = re.sub(r"さんが生放送を開始$", "", title)
    return user_name


def get_created_at(s: str):
    m = re.search(r'"created_at":"([^"]+)"', s)
    if m is None:
        return None
    return m.group(1)


def parse_notification(s: str):
    slugs = s.strip().split(" ")
    if len(slugs) < 2:
        return None
    if slugs[0].upper() != "NOTIFICATION:":
        return None
    [_, *payload] = slugs
    payload = " ".join(payload)

    userid = get_userid(payload)
    live_url = get_live_url(payload)
    lvid = get_lvid(live_url) if live_url is not None else None
    user_name = get_user_name(payload)
    live_title = get_live_title(payload)
    created_at = get_created_at(payload)

    return {
        "timestamp": created_at,
        "userid": userid,
        "live_url": live_url,
        "lvid": lvid,
        "user_name": user_name,
        "live_title": live_title,
    }


def parse_nicopush_uaid(s: str):
    slugs = s.strip().split(" ")
    if len(slugs) < 4:
        return None
    if slugs[-1].startswith("UAID="):
        return slugs[-1].split("=")[1]
    return None
