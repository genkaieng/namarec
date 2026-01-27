import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from utils import contains, safe_filename  # noqa: E402

ID_LIST = "11111,22222,33333,44444"


def test_contains():
    assert contains("11111", ID_LIST)
    assert contains("22222", ID_LIST)


def test_not_contains():
    assert not contains("99999", ID_LIST)


def test_contains_empty():
    assert not contains("22222", "")


def test_safe_filename():
    assert safe_filename("test.mp4") == "test.mp4"
    assert safe_filename("t e s t.mp4") == "test.mp4"
    assert safe_filename("t/e\\st.mp4") == "test.mp4"
