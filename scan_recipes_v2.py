import os
import re

root_dir = r"C:\Users\Q'warx\code\ID-Rocketeer.github.io\CookBook\recipes"

print(f"Scanning {root_dir}...")

recipes = [] # List of (filename, title, content)

# 1. Collect all recipes
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(subdir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title
            match = re.search(r'<span class="title">(.*?)</span>', content, re.IGNORECASE)
            title = match.group(1) if match else "NO_TITLE_FOUND"
            
            recipes.append({
                'filename': file,
                'filepath': filepath,
                'title': title,
                'content': content
            })

# 2. Analyze
all_titles = [r['title'] for r in recipes if r['title'] != "NO_TITLE_FOUND"]

for r in recipes:
    # Check 1: Filename vs Title mismatch
    fn_norm = os.path.splitext(r['filename'])[0].replace('-', ' ').replace('_', ' ').lower()
    tt_norm = r['title'].replace('-', ' ').replace('_', ' ').lower()
    
    # Simple heuristic: if title is not substring of filename AND filename is not substring of title
    # and they are not "very similar"
    # Actually, direct matching is better.
    
    if fn_norm != tt_norm:
         # lenient check: ignore case and whitespace differences
         pass 

    print(f"Checking {r['filename']} (Title: {r['title']})")
    
    if fn_norm.replace(' ', '') != tt_norm.replace(' ', ''):
        print(f"  [MISMATCH] Title '{r['title']}' does not match Filename '{r['filename']}'")

    # Check 2: Content contamination
    # Check if content matches other recipes' names or ingredients suspiciously.
    # The user said "copying an existing file and modifying to the new recipe".
    # Often the "Directions" or "Ingredients" are left over.
    
    # Heuristic: Check for exact content duplicates or near duplicates?
    # Or check if "Title" of another recipe appears in this one?
    
    # Let's search for *other* titles in this content.
    # Only if the other title is "Specific" enough (len > 4).
    for other_title in all_titles:
        if other_title == r['title']: continue
        if len(other_title) < 5: continue # Skip short words like "Tea"
        
        # Check if other_title appears in content, but ignore if it's generic.
        # This might be noisy, but let's see.
        if other_title.lower() in r['content'].lower():
            # Filter out common false positives?
            # e.g. "Sauce" in "Pasta with Sauce"
            pass
            # print(f"  [POTENTIAL] Contains reference to '{other_title}'")
            
    # Check 3: Check for obvious leftovers.
    # Often, the "Directions" might mention the *old* dish.
    # e.g. "Bake the Lasagna" in "Meatloaf".
    if r['title'].lower() not in r['content'].lower():
        print(f"  [ODD] Title '{r['title']}' not found in content body (besides the title tag).")

    # Check 4: Check if 'Ingredients' list seems copied?
    # Hard to tell without semantic understanding.
    
    # Check 5: Look for `content` text that matches `content` text of another recipe exactly?
    # This is "cp" detection.
    
    # Let's try to match content blocks.
    # Extract "Directions" text.
    
    dir_match = re.search(r'Directions:</h3>(.*?)</body>', r['content'], re.DOTALL | re.IGNORECASE)
    if dir_match:
        directions = dir_match.group(1)
        # Check if this exact directions block appears in another file
        for other in recipes:
            if other['filename'] == r['filename']: continue
            other_dir_match = re.search(r'Directions:</h3>(.*?)</body>', other['content'], re.DOTALL | re.IGNORECASE)
            if other_dir_match and directions.strip() == other_dir_match.group(1).strip():
                print(f"  [DUPLICATE DIRECTIONS] Match with {other['filename']}")

    ing_match = re.search(r'Ingredients:</h3>(.*?)<h3>', r['content'], re.DOTALL | re.IGNORECASE)
    if ing_match:
        ingredients = ing_match.group(1)
        for other in recipes:
             if other['filename'] == r['filename']: continue
             other_ing_match = re.search(r'Ingredients:</h3>(.*?)<h3>', other['content'], re.DOTALL | re.IGNORECASE)
             if other_ing_match and ingredients.strip() == other_ing_match.group(1).strip():
                 print(f"  [DUPLICATE INGREDIENTS] Match with {other['filename']}")

