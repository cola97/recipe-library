import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "recipes_json"
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_FILE = DOCS_DIR / "shopping_data.json"


def build_shopping_data():

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    result = {}

    if not JSON_DIR.exists():
        JSON_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    for path in sorted(
        JSON_DIR.glob("*.json")
    ):

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        recipe = data.get(
            "recipe",
            {}
        )

        ingredients = []

        for item in data.get(
            "ingredients",
            []
        ):

            ingredients.append({
                "ingredient_id":
                    item.get(
                        "ingredient_id",
                        ""
                    ),

                "display_name":
                    item.get(
                        "display_name",
                        ""
                    ),

                "category":
                    item.get(
                        "category",
                        ""
                    ),

                "quantity_used":
                    item.get(
                        "quantity_used"
                    ),

                "unit_used":
                    item.get(
                        "unit_used",
                        ""
                    ),
            })

        html_filename = (
            f"{path.stem}.html"
        )

        result[html_filename] = {
            "recipe_id":
                recipe.get(
                    "id",
                    path.stem
                ),

            "title":
                recipe.get(
                    "title",
                    path.stem
                ),

            "servings":
                recipe.get(
                    "servings",
                    2
                ),

            "ingredients":
                ingredients,
        }

    OUTPUT_FILE.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Shopping data: "
        f"{len(result)} recipes"
    )


if __name__ == "__main__":
    build_shopping_data()