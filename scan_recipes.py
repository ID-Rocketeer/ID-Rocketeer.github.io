import os
import re
from bs4 import BeautifulSoup

root_dir = r"C:\Users\Q'warx\code\ID-Rocketeer.github.io\CookBook\recipes"

print(f"Scanning {root_dir}...")

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(subdir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find title in span class="title"
            title_span = soup.find('span', class_='title')
            title_text = title_span.get_text(strip=True) if title_span else "NO_TITLE_SPAN"
            
            # Normalize filename
            filename_no_ext = os.path.splitext(file)[0]
            
            # Simple normalization for comparison (lowercase, remove spaces/hyphens)
            fn_norm = re.sub(r'[\s\-_]', '', filename_no_ext).lower()
            tt_norm = re.sub(r'[\s\-_]', '', title_text).lower()
            
            if fn_norm != tt_norm:
                print(f"MISMATCH: File='{file}' Title='{title_text}'")
            else:
                # Optional: Check if content seems weird?
                pass
