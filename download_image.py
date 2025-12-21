import urllib.request
import os

url = "https://mojo.generalmills.com/api/public/content/QGXwx5AWYUakwCeTbdHCZw_webp_base.webp?v=0f9c391b&t=191ddcab8d1c415fa10fa00a14351227"
dest = r"C:\Users\Q'warx\code\ID-Rocketeer.github.io\CookBook\images\corned_beef.webp"

print(f"Downloading {url} to {dest}...")
try:
    urllib.request.urlretrieve(url, dest)
    print("Download successful.")
except Exception as e:
    print(f"Error: {e}")
