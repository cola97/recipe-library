from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "recipes_json"
RENDERER = BASE_DIR / "render_recipe.py"

json_files = sorted(JSON_DIR.glob("*.json"))

if not json_files:
    print("No JSON files found.")
    raise SystemExit(0)

failed = []

for json_file in json_files:
    print(f"Rendering: {json_file.name}")

    result = subprocess.run([
        sys.executable,
        str(RENDERER),
        str(json_file)
    ])

    if result.returncode != 0:
        failed.append(json_file.name)

print()

if failed:
    print("FAILED:")
    for name in failed:
        print(f"  {name}")
    raise SystemExit(1)

print(f"Successfully rendered {len(json_files)} recipes.")