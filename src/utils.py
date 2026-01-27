import re


def contains(v, s):
    return v in s.replace(" ", "").strip().split(",")


def safe_filename(filename: str) -> str:
    s = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", filename)
    s = re.sub(r"\s+", "", s)
    return s
