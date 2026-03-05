from tqdm import tqdm
import os
import time
import subprocess
with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.1)
        pbar.update(10)
