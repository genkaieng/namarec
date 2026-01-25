import re


def get_userid(s):
    m = re.search(r'"icon":"([^"]+)"', s)
    if m is None:
        return None
    icon_url = m.group(1)
    m = re.search(r"(\d+)\.jpg", icon_url)
    if m is None:
        return None
    return m.group(1)


def get_live_url(s):
    m = re.search(r'"on_click":"([^"]+)"', s)
    if m is None:
        return None
    url = m.group(1)
    return url.split("?")[0]


def get_lvid(s):
    m = re.search(r"(lv\d+)", s)
    if m is None:
        return None
    lvid = m.group(1)
    return lvid


def get_live_title(s):
    m = re.search(r'"body":"([^"]+)"', s)
    if m is None:
        return None
    body = m.group(1)
    title = re.sub(r"」を放送", "", body[1:])
    return title


def get_user_name(s):
    m = re.search(r'"title":"([^"]+)"', s)
    if m is None:
        return None
    title = m.group(1)
    user_name = re.sub(r"さんが生放送を開始$", "", title)
    return user_name


def parse_notification(s):
    slugs = s.split(" ")
    if len(slugs) != 5:
        return None
    [date, time, _, type, notification] = slugs
    if type.upper() != "NOTIFICATION":
        return None

    userid = get_userid(notification)
    live_url = get_live_url(notification)
    lvid = get_lvid(live_url)
    user_name = get_user_name(notification)
    live_title = get_live_title(notification)

    return {"date": date, "time": time, "userid": userid, "live_url": live_url, "lvid": lvid, "user_name": user_name, "live_title": live_title}
