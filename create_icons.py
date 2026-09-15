import struct
import zlib
from pathlib import Path


BASE = Path(__file__).resolve().parent
ICON_DIR = BASE / "docs" / "icons"

ICON_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def chunk(chunk_type, data):

    payload = (
        chunk_type
        +
        data
    )

    return (
        struct.pack(
            ">I",
            len(data)
        )
        +
        payload
        +
        struct.pack(
            ">I",
            zlib.crc32(payload) & 0xffffffff
        )
    )


def create_icon(size, path):

    rows = []

    centre_x = size / 2
    centre_y = size / 2

    plate_outer = size * 0.30
    plate_inner = size * 0.24

    for y in range(size):

        row = bytearray()

        row.append(0)

        for x in range(size):

            # Warm cream background
            r, g, b = 245, 241, 225

            dx = x - centre_x
            dy = y - centre_y

            distance_squared = (
                dx * dx
                +
                dy * dy
            )

            # Black circular plate outline
            if (
                plate_inner ** 2
                <= distance_squared
                <= plate_outer ** 2
            ):
                r, g, b = 0, 0, 0

            # Central dot
            if (
                distance_squared
                <= (size * 0.035) ** 2
            ):
                r, g, b = 0, 0, 0

            row.extend(
                [r, g, b]
            )

        rows.append(bytes(row))

    raw = b"".join(rows)

    png = (
        b"\x89PNG\r\n\x1a\n"
        +
        chunk(
            b"IHDR",
            struct.pack(
                ">IIBBBBB",
                size,
                size,
                8,
                2,
                0,
                0,
                0
            )
        )
        +
        chunk(
            b"IDAT",
            zlib.compress(
                raw,
                9
            )
        )
        +
        chunk(
            b"IEND",
            b""
        )
    )

    path.write_bytes(png)


create_icon(
    192,
    ICON_DIR / "icon-192.png"
)

create_icon(
    512,
    ICON_DIR / "icon-512.png"
)

print(
    f"Icons created in {ICON_DIR}"
)