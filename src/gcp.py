import subprocess


def upload_to_gcs(filename, dest: str) -> bool:
    try:
        subprocess.run(["gcloud", "storage", "cp", filename, dest], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] upload failed: {filename} -> {dest}; {e}")
        return False
