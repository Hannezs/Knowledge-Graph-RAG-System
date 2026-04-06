import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import snapshot_download
import time

repo = 'shibing624/text2vec-base-chinese'
max_retries = 10

for i in range(max_retries):
    try:
        print(f"Attempt {i+1} to download {repo}...")
        snapshot_download(repo_id=repo, resume_download=True)
        print("Download complete!")
        break
    except Exception as e:
        print(f"Failed: {e}")
        time.sleep(2)
