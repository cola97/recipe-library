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

        return "".join(
            self.title_parts
        ).strip()


def read_html_title(path):

    parser = TitleParser()

    text = path.read_text(
        encoding="utf-8"
    )

    parser.feed(text)

    if parser.title:
        return parser.title

    return (
        path.stem
        .replace("_", " ")
        .title()
    )


def load_recipe_metadata():
    """
    Read metadata from recipe JSON files where available.

    JSON files are optional from the application's point of view.
    Existing HTML files remain browseable even if matching JSON
    metadata is unavailable.
    """

    metadata = {}

    if not JSON_DIR.exists():
        return metadata

    for path in sorted(
        JSON_DIR.glob("*.json")
    ):

        try:

            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception as exc:

            raise RuntimeError(
                "Could not read recipe JSON:\n"
                f"{path}\n"
                f"{exc}"
            )

        if not isinstance(data, dict):
            continue

        recipe = data.get(
            "recipe"
        )

        if not isinstance(recipe, dict):
            continue

        metadata[path.stem] = {

            "id":
                recipe.get(
                    "id",
                    path.stem
                ),

            "title":
                recipe.get(
                    "title",
                    path.stem
                    .replace("_", " ")
                    .title()
                ),

            "meal_types":
                recipe.get(
                    "meal_types",
                    []
                ),
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
    Copy every existing HTML recipe into docs/recipes.

    recipes.json therefore represents recipes that are currently
    available to open in the app.
    """

    metadata = load_recipe_metadata()

    if not HTML_DIR.exists():

        HTML_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    if APP_RECIPE_DIR.exists():

        shutil.rmtree(
            APP_RECIPE_DIR
        )

    APP_RECIPE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    recipes = []

    html_files = sorted(
        HTML_DIR.glob("*.html")
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

        recipe_metadata = (
            metadata.get(
                html_path.stem
            )
        )

        if recipe_metadata:

            recipe_id = (
                recipe_metadata["id"]
            )

            title = (
                recipe_metadata["title"]
            )

            meal_types = (
                recipe_metadata["meal_types"]
            )

        else:

            recipe_id = (
                html_path.stem
            )

            title = (
                read_html_title(
                    html_path
                )
            )

            meal_types = []

        recipes.append({

            "id":
                recipe_id,

            "filename":
                html_path.name,

            "title":
                title,

            "meal_types":
                meal_types,

        })

    recipes.sort(
        key=lambda recipe: (
            recipe["title"].casefold(),
            recipe["filename"].casefold()
        )
    )

    (
        DOCS_DIR
        /
        "recipes.json"
    ).write_text(

        json.dumps(
            recipes,
            ensure_ascii=False,
            indent=2
        ),

        encoding="utf-8"
    )

    return recipes


def build_schedule(recipes):
    """
    Build the application schedule.

    A schedule entry is valid even when its HTML file does not yet
    exist.

    Each entry receives:

        available: true

    or:

        available: false

    depending purely on whether its matching HTML file currently
    exists in the output directory.
    """

    available_recipes = {

        recipe["filename"]:
            recipe

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

    if not isinstance(
        schedule,
        list
    ):

        raise RuntimeError(
            "meal_schedule.json must contain a JSON array."
        )

    validated = []

    exact_entries_seen = set()

    for index, item in enumerate(
        schedule
    ):

        entry_number = (
            index + 1
        )

        if not isinstance(
            item,
            dict
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "must be an object."
            )

        date = item.get(
            "date"
        )

        meal_type = item.get(
            "meal_type"
        )

        title = item.get(
            "title"
        )

        filename = item.get(
            "file"
        )

        # -----------------------------
        # Validate date
        # -----------------------------

        if not isinstance(
            date,
            str
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "has no valid date."
            )

        if not validate_iso_date(
            date
        ):

            raise RuntimeError(
                f"Invalid date in schedule entry "
                f"{entry_number}: {date}. "
                "Use YYYY-MM-DD."
            )

        # -----------------------------
        # Validate meal type
        # -----------------------------

        if (
            not isinstance(
                meal_type,
                str
            )
            or
            not meal_type.strip()
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "has no valid meal_type."
            )

        # -----------------------------
        # Validate title
        # -----------------------------

        if (
            not isinstance(
                title,
                str
            )
            or
            not title.strip()
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "has no valid title."
            )

        # -----------------------------
        # Validate filename
        # -----------------------------

        if (
            not isinstance(
                filename,
                str
            )
            or
            not filename.strip()
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "has no valid file."
            )

        if not filename.lower().endswith(
            ".html"
        ):

            raise RuntimeError(
                f"Schedule entry {entry_number} "
                "must reference an .html file."
            )

        # -----------------------------
        # Duplicate protection
        # -----------------------------

        exact_key = (
            date,
            meal_type,
            filename
        )

        if exact_key in exact_entries_seen:

            raise RuntimeError(
                "Duplicate schedule entry found:\n"
                f"{date} | "
                f"{meal_type} | "
                f"{filename}"
            )

        exact_entries_seen.add(
            exact_key
        )

        # -----------------------------
        # Determine availability
        # -----------------------------

        available = (
            filename
            in
            available_recipes
        )

        if available:

            recipe = (
                available_recipes[
                    filename
                ]
            )

            recipe_id = (
                recipe["id"]
            )

        else:

            recipe_id = (
                Path(
                    filename
                ).stem
            )

        validated.append({

            "date":
                date,

            "meal_type":
                meal_type,

            "title":
                title,

            "file":
                filename,

            "recipe_id":
                recipe_id,

            "available":
                available,

        })

    meal_order = {

        "Breakfast": 1,

        "Morning snack": 2,

        "Lunch": 3,

        "Afternoon snack": 4,

        "Dinner": 5,

        "Evening snack": 6,

    }

    validated.sort(
        key=lambda item: (

            item["date"],

            meal_order.get(
                item["meal_type"],
                100
            ),

            item["meal_type"].casefold(),

            item["title"].casefold(),
        )
    )

    (
        DOCS_DIR
        /
        "schedule.json"
    ).write_text(

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

    recipes = (
        build_recipe_library()
    )

    schedule = (
        build_schedule(
            recipes
        )
    )

    (
        DOCS_DIR
        /
        ".nojekyll"
    ).write_text(
        "",
        encoding="utf-8"
    )

    available_count = sum(
        1
        for item in schedule
        if item["available"]
    )

    missing_count = (
        len(schedule)
        -
        available_count
    )

    print()
    print(
        "Recipe app library built successfully."
    )
    print()

    print(
        f"HTML recipes available: "
        f"{len(recipes)}"
    )

    print(
        f"Scheduled meals: "
        f"{len(schedule)}"
    )

    print(
        f"Scheduled recipes available: "
        f"{available_count}"
    )

    print(
        f"Scheduled recipes not generated yet: "
        f"{missing_count}"
    )

    print()

    print(
        f"App directory: "
        f"{DOCS_DIR}"
    )

    print()


if __name__ == "__main__":
    main()