import subprocess


def upload_to_gcs(filename, dest: str):
    try:
        subprocess.run(["gcloud", "storage", "cp", filename, dest], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] upload failed: {filename} -> {dest}; {e}")
