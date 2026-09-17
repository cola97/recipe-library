import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run(script, *args):

    command = [
        sys.executable,
        str(
            BASE_DIR
            /
            script
        ),
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

    print()
    print(
        "Recipe app update complete."
    )
    print()


if __name__ == "__main__":
    main()