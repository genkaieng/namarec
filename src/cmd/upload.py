import os
from pathlib import Path
import sys
from dotenv import load_dotenv

from gcp import upload_to_gcs

load_dotenv()

args = sys.argv

if len(args) < 2:
    print("Usage: python src/cmd/upload.py <filepath> [OUTPUT_GCS_URI]")
    exit(1)

# アップロードするファイルのパスを引数で受け取る
path = Path(args[1])

OUTPUT_GCS_URI = None
if len(args) >= 3:
    OUTPUT_GCS_URI = args[2]
else:
    OUTPUT_GCS_URI = os.getenv("OUTPUT_GCS_URI")

if OUTPUT_GCS_URI is None:
    print(
        "[WARN] OUTPUT_GCS_URI が設定されていないためアップロード処理がスキップされました。"
    )
    exit(0)

if os.path.exists(path):
    upload_to_gcs(path, OUTPUT_GCS_URI)
    print(f"[OK] {path} -> {OUTPUT_GCS_URI}")
