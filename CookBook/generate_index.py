import os
import urllib.parse
import datetime

# Config
root_dir = r"C:\Users\Q'warx\code\ID-Rocketeer.github.io\CookBook"
recipes_dir = os.path.join(root_dir, "recipes")
output_file = os.path.join(root_dir, "index.html")
site_title = "The Collins Family Cookbook"
main_header = "Collins<br/>Cookbook"

def get_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        import re
        match = re.search(r'<span class="title">(.*?)</span>', content)
        if match:
            return match.group(1).strip()
        filename = os.path.basename(file_path)
        return os.path.splitext(filename)[0]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return os.path.splitext(os.path.basename(file_path))[0]

def generate_index():
    print("Generating index...")
    
    html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

<head>
  <title>{site_title}</title>
  <link rel="stylesheet" type="text/css" href="style/index.css" title="index style" />
  <link rel="icon" type="image/png" href="images/favicon.png" />
</head>

<body>
  <h1>{main_header}</h1>

  <!-- Index produced on {datetime.datetime.now()} -->

  <ul>"""

    # 1. Get Categories
    categories = [d for d in os.listdir(recipes_dir) if os.path.isdir(os.path.join(recipes_dir, d))]
    categories.sort()

    for index, category in enumerate(categories):
        cat_path = os.path.join(recipes_dir, category)
        rel_path = f"recipes/{category}"
        
        html += f"""<!-- indexCategory: {rel_path} {index}  -->
    <!-- is_dir ({rel_path}) : true -->
    <!-- processCategory ({rel_path}) -->
    <li>
      <h2>{category}</h2>
      <ul>\n"""
        
        # 2. Get Recipes
        files = [f for f in os.listdir(cat_path) if f.endswith(".html")]
        
        recipe_list = []
        for file in files:
            file_path = os.path.join(cat_path, file)
            title = get_title(file_path)
            # Encode URL parts. Important: Windows path sep to slash
            url = f"recipes/{urllib.parse.quote(category)}/{urllib.parse.quote(file)}"
            recipe_list.append({'title': title, 'url': url})
        
        # Sort by title
        recipe_list.sort(key=lambda x: x['title'])
        
        for r in recipe_list:
            html += f"""        <li><a href="{r['url']}">{r['title']}</a></li>\n"""

        html += """      </ul>
      <br />
    </li>\n"""

    html += """  </ul>
</body>

</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Index generated at {output_file}")

if __name__ == "__main__":
    generate_index()
