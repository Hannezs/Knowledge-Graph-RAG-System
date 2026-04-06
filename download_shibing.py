import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import hf_hub_download
import time

repo = 'shibing624/text2vec-base-chinese'
files = ["config.json", "pytorch_model.bin", "tokenizer.json", "tokenizer_config.json", "vocab.txt", "special_tokens_map.json", "modules.json", "1_Pooling/config.json"]

for f in files:
    for i in range(10):
        try:
            print(f"Downloading {f}...")
            hf_hub_download(repo_id=repo, filename=f, resume_download=True, proxies={"http": None, "https": None})
            break
        except Exception as e:
            print(e)
            time.sleep(1)
