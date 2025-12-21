import os
import subprocess

# Files that were renamed with case changes
renames = [
    ("CookBook/recipes/Desserts/kringla.html", "CookBook/recipes/Desserts/Kringla.html"),
    ("CookBook/recipes/Drinks/beer.html", "CookBook/recipes/Drinks/Beer.html"),
    ("CookBook/recipes/Entrees/goulash.html", "CookBook/recipes/Entrees/Goulash.html"),
    ("CookBook/recipes/Entrees/lasagna.html", "CookBook/recipes/Entrees/Lasagna.html"),
    ("CookBook/recipes/Entrees/meatloaf.html", "CookBook/recipes/Entrees/Meatloaf.html"),
    ("CookBook/recipes/Entrees/mostaccioli.html", "CookBook/recipes/Entrees/Mostaccioli.html"),
    ("CookBook/recipes/Entrees/spaghetti.html", "CookBook/recipes/Entrees/Spaghetti.html"),
    ("CookBook/recipes/Soups/cheese.html", "CookBook/recipes/Soups/Cheese.html"),
    ("CookBook/recipes/Soups/chili.html", "CookBook/recipes/Soups/Chili.html"),
    ("CookBook/recipes/Soups/clamChowder.html", "CookBook/recipes/Soups/ClamChowder.html"),
]

os.chdir(r"C:\Users\Q'warx\code\ID-Rocketeer.github.io")

for old_path, new_path in renames:
    # Git mv with two-step process to handle case-only renames on Windows
    temp_path = old_path + ".tmp"
    
    print(f"Renaming {old_path} -> {new_path}")
    
    # Step 1: Move to temp name
    result1 = subprocess.run(["git", "mv", old_path, temp_path], capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"  Warning: git mv to temp failed: {result1.stderr}")
        continue
    
    # Step 2: Move to final name
    result2 = subprocess.run(["git", "mv", temp_path, new_path], capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"  Error: git mv to final name failed: {result2.stderr}")
        # Try to revert
        subprocess.run(["git", "mv", temp_path, old_path], capture_output=True, text=True)
    else:
        print(f"  Success!")

print("\nDone! Check git status to verify the renames.")
