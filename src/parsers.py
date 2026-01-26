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


def parse_notification(s: str):
    slugs = s.strip().split(" ")
    if len(slugs) < 5:
        return None
    [date, time, _, type, *payload] = slugs
    payload = " ".join(payload)
    if type.upper() != "NOTIFICATION":
        return None

    userid = get_userid(payload)
    live_url = get_live_url(payload)
    lvid = get_lvid(live_url) if live_url is not None else None
    user_name = get_user_name(payload)
    live_title = get_live_title(payload)

    return {
        "date": date,
        "time": time,
        "userid": userid,
        "live_url": live_url,
        "lvid": lvid,
        "user_name": user_name,
        "live_title": live_title,
    }


def parse_nicopush_uaid(s: str):
    slugs = s.strip().split(" ")
    if len(slugs) == 2:
        [_, slug] = slugs
        if slug.startswith("UAID="):
            return slug.split("=")[1]
    return None
