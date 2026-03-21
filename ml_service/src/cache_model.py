import os
from huggingface_hub import snapshot_download


def download_model():
    model_id = "Qwen/Qwen2-VL-2B-Instruct"
    cache_dir = os.getenv("HF_HOME", "/root/.cache/huggingface")

    print(f"Downloading {model_id} to {cache_dir}...")
    snapshot_download(repo_id=model_id, local_files_only=False, cache_dir=cache_dir)
    print("Download complete.")


if __name__ == "__main__":
    download_model()
