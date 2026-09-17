import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run(
    script,
    *args
):

    path = BASE_DIR / script

    if not path.exists():

        raise SystemExit(
            f"Missing required file: {path}"
        )

    command = [
        sys.executable,
        str(path),
        *args,
    ]

    print()
    print(
        "Running:",
        " ".join(command)
    )
    print()

    subprocess.run(
        command,
        check=True
    )


def main():

    run(
        "render_all.py"
    )

    run(
        "build_app.py"
    )

    run(
        "build_shopping_data.py"
    )

    run(
        "build_recipe_index.py"
    )

    print()
    print(
        "Recipe app update complete."
    )
    print()


if __name__ == "__main__":
    main()
