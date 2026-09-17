import argparse
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

JSON_DIR = (
    BASE_DIR
    /
    "recipes_json"
)

OUTPUT_DIR = (
    BASE_DIR
    /
    "output"
)

RENDERER = (
    BASE_DIR
    /
    "render_recipe.py"
)


def needs_render(
    json_file,
    html_file,
    force=False
):

    if force:
        return True

    if not html_file.exists():
        return True

    output_time = (
        html_file.stat().st_mtime
    )

    json_time = (
        json_file.stat().st_mtime
    )

    renderer_time = (
        RENDERER.stat().st_mtime
    )

    return (
        output_time
        <
        max(
            json_time,
            renderer_time
        )
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Render all recipe JSON files."
        )
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Render every recipe even if "
            "the HTML already appears current."
        )
    )

    args = parser.parse_args()

    if not RENDERER.exists():

        raise SystemExit(
            f"Renderer not found: {RENDERER}"
        )

    JSON_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    json_files = sorted(
        JSON_DIR.glob(
            "*.json"
        )
    )

    if not json_files:

        print(
            "No recipe JSON files found."
        )

        return

    rendered = []
    skipped = []
    failed = []

    for json_file in json_files:

        html_file = (
            OUTPUT_DIR
            /
            f"{json_file.stem}.html"
        )

        if not needs_render(
            json_file,
            html_file,
            force=args.force
        ):

            print(
                f"Up to date: "
                f"{json_file.name}"
            )

            skipped.append(
                json_file.name
            )

            continue

        print(
            f"Rendering: "
            f"{json_file.name}"
        )

        result = subprocess.run(
            [
                sys.executable,
                str(RENDERER),
                str(json_file),
                str(html_file),
            ]
        )

        if result.returncode == 0:

            rendered.append(
                json_file.name
            )

        else:

            failed.append(
                json_file.name
            )

    print()
    print(
        "Render summary"
    )
    print(
        "--------------"
    )

    print(
        f"Rendered: "
        f"{len(rendered)}"
    )

    print(
        f"Already current: "
        f"{len(skipped)}"
    )

    print(
        f"Failed: "
        f"{len(failed)}"
    )

    if failed:

        print()
        print(
            "Failed files:"
        )

        for filename in failed:

            print(
                f"  {filename}"
            )

        raise SystemExit(1)


if __name__ == "__main__":
    main()