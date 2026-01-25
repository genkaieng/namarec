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
