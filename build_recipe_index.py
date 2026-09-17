import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "recipes_json"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
DOCS_RECIPE_DIR = DOCS_DIR / "recipes"
OUTPUT_FILE = DOCS_DIR / "recipes.json"


def text_for_ingredient(item):
    return " ".join(
        [
            str(
                item.get(
                    "ingredient_id",
                    ""
                )
            ),
            str(
                item.get(
                    "display_name",
                    ""
                )
            ),
        ]
    ).lower()


def derive_protein_sources(
    ingredients
):
    sources = set()

    for item in ingredients:

        category = str(
            item.get(
                "category",
                ""
            )
        ).lower()

        text = text_for_ingredient(
            item
        )

        if category == "plant protein":

            if "tofu" in text:
                sources.add("Tofu")

            elif "tempeh" in text:
                sources.add("Tempeh")

            elif "seitan" in text:
                sources.add("Seitan")

            elif (
                "mycoprotein" in text
                or
                "quorn" in text
            ):
                sources.add("Mycoprotein")

            else:
                sources.add("Other plant protein")

        if category == "legumes":

            if "edamame" in text:
                sources.add("Edamame")

            elif "lentil" in text:
                sources.add("Lentils")

            elif "chickpea" in text:
                sources.add("Chickpeas")

            elif "bean" in text:
                sources.add("Beans")

            else:
                sources.add("Legumes")

        if category == "eggs":
            sources.add("Eggs")

        if category == "dairy":

            if "cottage" in text:
                sources.add("Cottage cheese")

            elif (
                "skyr" in text
                or
                "greek yoghurt" in text
                or
                "greek yogurt" in text
            ):
                sources.add(
                    "Skyr / Greek yoghurt"
                )

            elif "quark" in text:
                sources.add("Quark")

    return sorted(
        sources
    )


def html_exists(
    filename
):
    return (
        (
            OUTPUT_DIR
            /
            filename
        ).exists()
        or
        (
            DOCS_RECIPE_DIR
            /
            filename
        ).exists()
    )


def build_recipe_index():

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    recipes = []

    for path in sorted(
        JSON_DIR.glob(
            "*.json"
        )
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

        nutrition = data.get(
            "nutrition_per_serving",
            {}
        )

        ingredients = data.get(
            "ingredients",
            []
        )

        filename = (
            f"{path.stem}.html"
        )

        if not html_exists(
            filename
        ):
            continue

        recipes.append(
            {
                "id":
                    recipe.get(
                        "id",
                        path.stem
                    ),

                "filename":
                    filename,

                "title":
                    recipe.get(
                        "title",
                        path.stem
                    ),

                "description":
                    recipe.get(
                        "description",
                        ""
                    ),

                "servings":
                    recipe.get(
                        "servings"
                    ),

                "difficulty":
                    recipe.get(
                        "difficulty",
                        ""
                    ),

                "active_time_minutes":
                    recipe.get(
                        "active_time_minutes"
                    ),

                "total_time_minutes":
                    recipe.get(
                        "total_time_minutes"
                    ),

                "cuisine":
                    recipe.get(
                        "cuisine",
                        []
                    ),

                "meal_types":
                    recipe.get(
                        "meal_types",
                        []
                    ),

                "dietary_tags":
                    recipe.get(
                        "dietary_tags",
                        []
                    ),

                "allergens":
                    recipe.get(
                        "allergens",
                        []
                    ),

                "energy_kcal":
                    nutrition.get(
                        "energy_kcal"
                    ),

                "protein_g":
                    nutrition.get(
                        "protein_g"
                    ),

                "protein_sources":
                    derive_protein_sources(
                        ingredients
                    ),
            }
        )

    recipes.sort(
        key=lambda item:
            item[
                "title"
            ].casefold()
    )

    OUTPUT_FILE.write_text(
        json.dumps(
            recipes,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Recipe index: "
        f"{len(recipes)} recipes"
    )


if __name__ == "__main__":
    build_recipe_index()
