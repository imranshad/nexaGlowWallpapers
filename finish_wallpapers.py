import os
import glob
import shutil
import json

brain_dir = "/Users/developer/.gemini/antigravity/brain/6022c163-96df-4d85-a857-b223772d0062"
base_dir = "/Users/developer/Desktop/dev/NexaGlowWallpapers"
json_path = os.path.join(base_dir, "wallpapers.json")
github_raw_base = "https://raw.githubusercontent.com/imranshad/nexaGlowWallpapers/main"

categories = [
    "Animated", "Art", "Car", "City", "3d", "Games", "Nature", "Pattern", "People", "Animals"
]

chat_files = glob.glob(os.path.join(brain_dir, "*.png"))

registry = {cat: [] for cat in categories}
handled = set()

for filepath in chat_files:
    filename = os.path.basename(filepath)
    parts = filename.split('_')
    if len(parts) >= 2:
        cat_lower = parts[0]
        idx = parts[1]
        
        actual_cat = None
        for c in categories:
            if c.lower() == cat_lower:
                actual_cat = c
                break
                
        if actual_cat:
            cat_dir = os.path.join(base_dir, actual_cat)
            os.makedirs(cat_dir, exist_ok=True)
            dest_filename = f"{idx}.png"
            dest_path = os.path.join(cat_dir, dest_filename)
            
            shutil.copy2(filepath, dest_path)
            print(f"Copied {filename} to {actual_cat}/{dest_filename}")
            
            registry[actual_cat].append((int(idx), f"{github_raw_base}/{actual_cat}/{dest_filename}"))
            handled.add(f"{actual_cat}_{idx}")

# Format the registry properly
final_registry = {}
for cat, items in registry.items():
    items.sort(key=lambda x: x[0])
    final_registry[cat] = [x[1] for x in items]

with open(json_path, 'w') as f:
    json.dump(final_registry, f, indent=2)

print("\nSuccess! 17 images organized, JSON updated.")
