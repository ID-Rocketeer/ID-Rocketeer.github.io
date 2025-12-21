import os
import re

# Directory to scan
root_dir = r"C:\Users\Q'warx\code\ID-Rocketeer.github.io\CookBook\recipes"

def to_camel_case(filename):
    # Remove extension
    name, ext = os.path.splitext(filename)
    # Split by space, underscore, hyphen
    words = re.split(r'[\s\-_]+', name)
    # Capitalize first letter of each word
    camel_name = "".join(word.capitalize() for word in words if word)
    return camel_name + ext

print(f"Scanning {root_dir} for files to rename...")

count = 0
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if not file.endswith(".html"):
            continue
            
        old_path = os.path.join(subdir, file)
        
        if " " in file or "-" in file or "_" in file:
            new_name = to_camel_case(file)
        else:
            # No separators. Just ensure first letter is Upper.
            # Don't use .capitalize() because it lowers the rest!
            name, ext = os.path.splitext(file)
            if name:
                new_name = name[0].upper() + name[1:] + ext
            else:
                new_name = file

        new_path = os.path.join(subdir, new_name)
        
        if old_path != new_path:
            print(f"Renaming: '{file}' -> '{new_name}'")
            try:
                os.rename(old_path, new_path)
                count += 1
            except Exception as e:
                print(f"FAILED to rename {file}: {e}")

print(f"Renamed {count} files.")
