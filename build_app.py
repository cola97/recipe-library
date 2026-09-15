import json
import shutil
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

JSON_DIR = BASE_DIR / "recipes_json"
HTML_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
APP_RECIPE_DIR = DOCS_DIR / "recipes"

SCHEDULE_SOURCE = BASE_DIR / "meal_schedule.json"


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_title = False
        self.title_parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.inside_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.inside_title = False

    def handle_data(self, data):
        if self.inside_title:
            self.title_parts.append(data)

    @property
    def title(self):
        return "".join(self.title_parts).strip()


def read_html_title(path):
    parser = TitleParser()

    text = path.read_text(
        encoding="utf-8"
    )

    parser.feed(text)

    if parser.title:
        return parser.title

    return path.stem.replace("_", " ").title()


def load_recipe_metadata():
    """
    Load metadata from recipe JSON where available.

    Metadata is indexed by the corresponding HTML filename stem.
    """

    metadata = {}

    if not JSON_DIR.exists():
        return metadata

    for path in sorted(JSON_DIR.glob("*.json")):

        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )
        except Exception as exc:
            raise RuntimeError(
                f"Could not read recipe JSON: {path}\n{exc}"
            )

        if not isinstance(data, dict):
            continue

        recipe = data.get("recipe")

        if not isinstance(recipe, dict):
            continue

        metadata[path.stem] = {
            "id": recipe.get("id", path.stem),
            "title": recipe.get(
                "title",
                path.stem.replace("_", " ").title()
            ),
            "meal_types": recipe.get(
                "meal_types",
                []
            )
        }

    return metadata


def validate_iso_date(value):
    try:
        datetime.strptime(
            value,
            "%Y-%m-%d"
        )

        return True

    except ValueError:
        return False


def build_recipe_library():
    """
    Copy every HTML file from output into docs/recipes
    and create recipes.json.

    Importantly, every HTML file is included even if
    there is no corresponding recipe JSON.
    """

    metadata = load_recipe_metadata()

    if not HTML_DIR.exists():
        raise RuntimeError(
            f"HTML directory does not exist: {HTML_DIR}"
        )

    if APP_RECIPE_DIR.exists():
        shutil.rmtree(APP_RECIPE_DIR)

    APP_RECIPE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    recipes = []

    html_files = sorted(
        HTML_DIR.glob("*.html")
    )

    if not html_files:
        raise RuntimeError(
            "No HTML recipes were found in the output directory."
        )

    for html_path in html_files:

        destination = (
            APP_RECIPE_DIR
            /
            html_path.name
        )

        shutil.copy2(
            html_path,
            destination
        )

        recipe_metadata = metadata.get(
            html_path.stem
        )

        if recipe_metadata:

            recipe_id = recipe_metadata["id"]
            title = recipe_metadata["title"]
            meal_types = recipe_metadata["meal_types"]

        else:

            recipe_id = html_path.stem
            title = read_html_title(html_path)
            meal_types = []

        recipes.append({
            "id": recipe_id,
            "filename": html_path.name,
            "title": title,
            "meal_types": meal_types
        })

    recipes.sort(
        key=lambda recipe: (
            recipe["title"].casefold(),
            recipe["filename"].casefold()
        )
    )

    (DOCS_DIR / "recipes.json").write_text(
        json.dumps(
            recipes,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return recipes


def build_schedule(recipes):

    available = {
        recipe["filename"]: recipe
        for recipe in recipes
    }

    if not SCHEDULE_SOURCE.exists():

        schedule = []

    else:

        schedule = json.loads(
            SCHEDULE_SOURCE.read_text(
                encoding="utf-8"
            )
        )

    if not isinstance(schedule, list):
        raise RuntimeError(
            "meal_schedule.json must contain a JSON array."
        )

    validated = []

    for index, item in enumerate(schedule):

        if not isinstance(item, dict):
            raise RuntimeError(
                f"Schedule entry {index + 1} must be an object."
            )

        date = item.get("date")
        meal_type = item.get("meal_type")
        filename = item.get("file")

        if not isinstance(date, str):
            raise RuntimeError(
                f"Schedule entry {index + 1} has no valid date."
            )

        if not validate_iso_date(date):
            raise RuntimeError(
                f"Invalid date in schedule entry {index + 1}: "
                f"{date}. Use YYYY-MM-DD."
            )

        if not isinstance(meal_type, str) or not meal_type.strip():
            raise RuntimeError(
                f"Schedule entry {index + 1} has no valid meal_type."
            )

        if not isinstance(filename, str) or not filename.strip():
            raise RuntimeError(
                f"Schedule entry {index + 1} has no valid file."
            )

        if filename not in available:
            raise RuntimeError(
                f"Schedule entry {index + 1} references "
                f"a recipe that does not exist:\n{filename}"
            )

        recipe = available[filename]

        known_types = recipe.get(
            "meal_types",
            []
        )

        if (
            known_types
            and meal_type not in known_types
        ):
            raise RuntimeError(
                f"Schedule entry {index + 1} assigns "
                f"'{meal_type}' to {filename}, but the recipe JSON "
                f"declares meal_types as {known_types}."
            )

        validated.append({
            "date": date,
            "meal_type": meal_type,
            "file": filename,
            "recipe_id": recipe["id"],
            "title": recipe["title"]
        })

    validated.sort(
        key=lambda item: (
            item["date"],
            item["meal_type"].casefold(),
            item["title"].casefold()
        )
    )

    (DOCS_DIR / "schedule.json").write_text(
        json.dumps(
            validated,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return validated


def main():

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    recipes = build_recipe_library()

    schedule = build_schedule(
        recipes
    )

    # Prevent GitHub Pages from running these files through Jekyll.
    (DOCS_DIR / ".nojekyll").write_text(
        "",
        encoding="utf-8"
    )

    print()
    print("Recipe app library built successfully.")
    print()
    print(f"Recipes: {len(recipes)}")
    print(f"Scheduled meals: {len(schedule)}")
    print()
    print(f"App directory: {DOCS_DIR}")
    print()


if __name__ == "__main__":
    main()