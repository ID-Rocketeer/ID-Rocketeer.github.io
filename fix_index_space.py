import os

def fix_index_space(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the specific pattern where the space might have been lost
    new_content = content.replace('.gif" border="0">INDEX</a>', '.gif" border="0"> INDEX</a>')
    
    if new_content != content:
        print(f"Fixed space in {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

recipes_dir = r"C:\Users\Qwarx\code\ID-Rocketeer.github.io\CookBook\recipes"
for subdir, dirs, files in os.walk(recipes_dir):
    for file in files:
        if file.endswith(".html"):
            fix_index_space(os.path.join(subdir, file))
