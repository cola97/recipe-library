import argparse
import copy
import hashlib
import html
import json
from pathlib import Path


# ============================================================
# Formatting helpers
# ============================================================

def display_label(key):
    """
    Convert a JSON field name into a more readable display label.

    This affects presentation only.
    The original JSON key remains preserved in data-json-path.
    """
    if key is None:
        return ""

    return key.replace("_", " ").strip().title()


def path_for_key(parent_path, key):
    if parent_path == "$":
        return f"$.{key}"
    return f"{parent_path}.{key}"


def path_for_index(parent_path, index):
    return f"{parent_path}[{index}]"


def format_scalar(value):
    """
    Render a JSON scalar without altering its semantic value.
    """

    if value is None:
        return '<span class="null-value">null</span>'

    if isinstance(value, bool):
        return (
            '<span class="boolean-value">'
            + ("true" if value else "false")
            + "</span>"
        )

    if isinstance(value, (int, float)):
        return html.escape(
            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False
            )
        )

    if isinstance(value, str):
        return html.escape(value)

    raise TypeError(
        f"Unexpected scalar type: {type(value).__name__}"
    )


# ============================================================
# Completeness checking
# ============================================================

def collect_json_paths(node, path="$"):
    """
    Return every object, array and value path present in the JSON.

    Empty dictionaries and empty arrays are included.
    """

    paths = {path}

    if isinstance(node, dict):
        for key, value in node.items():
            child_path = path_for_key(path, key)
            paths.update(
                collect_json_paths(value, child_path)
            )

    elif isinstance(node, list):
        for index, value in enumerate(node):
            child_path = path_for_index(path, index)
            paths.update(
                collect_json_paths(value, child_path)
            )

    return paths


# ============================================================
# Recursive HTML renderer
# ============================================================

def render_node(
    node,
    path,
    seen_paths,
    key=None,
    depth=0
):
    """
    Recursively render any JSON value.

    No JSON content is intentionally omitted.
    """

    seen_paths.add(path)

    label = display_label(key)

    # --------------------------------------------------------
    # Dictionary / object
    # --------------------------------------------------------

    if isinstance(node, dict):

        if key is None:
            parts = [
                f'<div class="object-content" '
                f'data-json-path="{html.escape(path)}">'
            ]
        else:
            parts = [
                f'<section class="nested-object" '
                f'data-json-path="{html.escape(path)}">'
            ]

            parts.append(
                f"<h3>{html.escape(label)}</h3>"
            )

        if len(node) == 0:
            parts.append(
                '<div class="empty-value">{ }</div>'
            )

        else:
            for child_key, child_value in node.items():

                child_path = path_for_key(
                    path,
                    child_key
                )

                parts.append(
                    render_node(
                        child_value,
                        child_path,
                        seen_paths,
                        key=child_key,
                        depth=depth + 1
                    )
                )

        if key is None:
            parts.append("</div>")
        else:
            parts.append("</section>")

        return "\n".join(parts)

    # --------------------------------------------------------
    # List / array
    # --------------------------------------------------------

    if isinstance(node, list):

        parts = [
            f'<div class="array-block" '
            f'data-json-path="{html.escape(path)}">'
        ]

        if key is not None:
            parts.append(
                f"<h3>{html.escape(label)}</h3>"
            )

        if len(node) == 0:

            parts.append(
                '<div class="empty-value">[ ]</div>'
            )

        else:

            parts.append(
                '<div class="array-items">'
            )

            for index, item in enumerate(node):

                item_path = path_for_index(
                    path,
                    index
                )

                # --------------------------------------------
                # Object inside an array
                # --------------------------------------------

                if isinstance(item, dict):

                    seen_paths.add(item_path)

                    parts.append(
                        f'<article class="array-item" '
                        f'data-json-path="{html.escape(item_path)}">'
                    )

                    parts.append(
                        f'<div class="item-number">'
                        f'Item {index + 1}'
                        f'</div>'
                    )

                    if len(item) == 0:

                        parts.append(
                            '<div class="empty-value">{ }</div>'
                        )

                    else:

                        for child_key, child_value in item.items():

                            child_path = path_for_key(
                                item_path,
                                child_key
                            )

                            parts.append(
                                render_node(
                                    child_value,
                                    child_path,
                                    seen_paths,
                                    key=child_key,
                                    depth=depth + 1
                                )
                            )

                    parts.append(
                        "</article>"
                    )

                # --------------------------------------------
                # Nested array
                # --------------------------------------------

                elif isinstance(item, list):

                    parts.append(
                        render_node(
                            item,
                            item_path,
                            seen_paths,
                            key=None,
                            depth=depth + 1
                        )
                    )

                # --------------------------------------------
                # Scalar array member
                # --------------------------------------------

                else:

                    seen_paths.add(item_path)

                    parts.append(
                        f'<div class="scalar-array-item" '
                        f'data-json-path="{html.escape(item_path)}">'
                        f'{format_scalar(item)}'
                        f'</div>'
                    )

            parts.append(
                "</div>"
            )

        parts.append(
            "</div>"
        )

        return "\n".join(parts)

    # --------------------------------------------------------
    # Scalar
    # --------------------------------------------------------

    if key is None:

        return (
            f'<div class="top-scalar-value" '
            f'data-json-path="{html.escape(path)}">'
            f'{format_scalar(node)}'
            f'</div>'
        )

    return (
        f'<div class="field-row" '
        f'data-json-path="{html.escape(path)}">'
        f'<div class="field-name">'
        f'{html.escape(label)}'
        f'</div>'
        f'<div class="field-value">'
        f'{format_scalar(node)}'
        f'</div>'
        f'</div>'
    )


# ============================================================
# Top-level section renderer
# ============================================================

def render_top_section(
    key,
    value,
    path,
    seen_paths
):
    """
    Render every top-level JSON property as its own coloured section.
    """

    seen_paths.add(path)

    label = display_label(key)

    contents = render_node(
        value,
        path,
        seen_paths,
        key=None,
        depth=0
    )

    return (
        f'<section class="top-section" '
        f'data-json-path="{html.escape(path)}">'
        f'<h2>{html.escape(label)}</h2>'
        f'{contents}'
        f'</section>'
    )


# ============================================================
# Main HTML document
# ============================================================

def build_html(
    data,
    raw_json_text,
    scheduled_date=None
):

    # Keep a completely separate copy for mutation checking.
    original_data = copy.deepcopy(data)

    expected_paths = collect_json_paths(data)

    seen_paths = {"$"}

    recipe_title = (
        data.get("recipe", {}).get("title")
        if isinstance(data, dict)
        else None
    )

    if not isinstance(recipe_title, str):
        recipe_title = "Recipe"

    # --------------------------------------------------------
    # Render every top-level field in original JSON order
    # --------------------------------------------------------

    body_parts = []

    for key, value in data.items():

        path = path_for_key(
            "$",
            key
        )

        body_parts.append(
            render_top_section(
                key,
                value,
                path,
                seen_paths
            )
        )

    # --------------------------------------------------------
    # Completeness audit
    # --------------------------------------------------------

    missing_paths = (
        expected_paths - seen_paths
    )

    if missing_paths:

        missing_text = "\n".join(
            sorted(missing_paths)
        )

        raise RuntimeError(
            "HTML rendering failed completeness audit.\n"
            "The following JSON paths were not rendered:\n"
            f"{missing_text}"
        )

    unexpected_paths = (
        seen_paths - expected_paths
    )

    if unexpected_paths:

        unexpected_text = "\n".join(
            sorted(unexpected_paths)
        )

        raise RuntimeError(
            "HTML rendering produced unexpected JSON paths:\n"
            f"{unexpected_text}"
        )

    # --------------------------------------------------------
    # Mutation check
    # --------------------------------------------------------

    if data != original_data:

        raise RuntimeError(
            "The JSON data changed during rendering."
        )

    # --------------------------------------------------------
    # Source fingerprint
    # --------------------------------------------------------

    source_hash = hashlib.sha256(
        raw_json_text.encode("utf-8")
    ).hexdigest()

    source_json_escaped = html.escape(
        raw_json_text
    )

    body_html = "\n".join(
        body_parts
    )

    # --------------------------------------------------------
    # Schedule metadata
    # --------------------------------------------------------

    if scheduled_date is None:

        date_html = ""

    else:

        date_html = (
            '<div class="schedule-date">'
            '<strong>Scheduled date:</strong> '
            f'{html.escape(scheduled_date)}'
            '</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<title>{html.escape(recipe_title)}</title>

<style>

    :root {{
        --page-width: 1100px;
        --border: #8f8f8f;
        --page-background: #f2f2f2;
    }}

    * {{
        box-sizing: border-box;
    }}

    html {{
        background: var(--page-background);
    }}

    body {{
        margin: 0;

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #000000;

        line-height: 1.55;
    }}

    h1,
    h2,
    h3,
    h4,
    p,
    div,
    span,
    code,
    pre,
    summary,
    strong {{
        color: #000000;
    }}

    .page {{
        width: min(
            calc(100% - 32px),
            var(--page-width)
        );

        margin:
            32px
            auto
            64px
            auto;
    }}

    /* ======================================================
       Header
       ====================================================== */

    .document-header {{
        background: #ffffff;

        border:
            1px
            solid
            var(--border);

        border-radius: 14px;

        padding: 32px;

        margin-bottom: 24px;
    }}

    .document-header h1 {{
        margin: 0;

        font-size:
            clamp(
                2rem,
                4vw,
                3rem
            );

        line-height: 1.1;
    }}

    .schedule-date {{
        margin-top: 18px;

        padding:
            12px
            16px;

        border:
            1px
            solid
            #000000;

        border-radius: 8px;

        background: #fff7c7;

        font-size: 1.1rem;
    }}

    /* ======================================================
       All major JSON sections
       ====================================================== */

    .top-section {{
        border:
            1px
            solid
            var(--border);

        border-radius: 14px;

        padding: 24px;

        margin:
            0
            0
            24px
            0;
    }}

    .top-section > h2 {{
        margin:
            0
            0
            20px
            0;

        padding-bottom: 10px;

        border-bottom:
            2px
            solid
            #000000;

        font-size: 1.6rem;
    }}

    /*
       Every major section receives its own background colour.

       Text remains black throughout.
    */

    .top-section[data-json-path="$.schema_version"] {{
        background: #eeeeee;
    }}

    .top-section[data-json-path="$.recipe"] {{
        background: #ffe8dc;
    }}

    .top-section[data-json-path="$.nutrition_per_serving"] {{
        background: #ddf3e4;
    }}

    .top-section[data-json-path="$.ingredients"] {{
        background: #fff4c9;
    }}

    .top-section[data-json-path="$.equipment"] {{
        background: #dfeeff;
    }}

    .top-section[data-json-path="$.mise_en_place"] {{
        background: #eee2fa;
    }}

    .top-section[data-json-path="$.procedure"] {{
        background: #ffe1e8;
    }}

    .top-section[data-json-path="$.plating"] {{
        background: #daf5f2;
    }}

    .top-section[data-json-path="$.storage"] {{
        background: #ffe9c9;
    }}

    .top-section[data-json-path="$.shopping"] {{
        background: #e4f3d7;
    }}

    .top-section[data-json-path="$.quality_checks"] {{
        background: #eadff5;
    }}

    /* ======================================================
       Nested objects
       ====================================================== */

    .object-content {{
        margin: 0;
    }}

    .nested-object {{
        margin:
            18px
            0;

        padding: 18px;

        border:
            1px
            solid
            #777777;

        border-radius: 10px;

        background:
            rgba(
                255,
                255,
                255,
                0.55
            );
    }}

    .nested-object > h3 {{
        margin:
            0
            0
            14px
            0;
    }}

    /* ======================================================
       Individual fields
       ====================================================== */

    .field-row {{
        display: grid;

        grid-template-columns:
            minmax(
                180px,
                28%
            )
            1fr;

        gap: 20px;

        padding:
            10px
            0;

        border-bottom:
            1px
            solid
            rgba(
                0,
                0,
                0,
                0.18
            );
    }}

    .field-row:last-child {{
        border-bottom: 0;
    }}

    .field-name {{
        font-weight: 700;
    }}

    .field-value {{
        white-space: pre-wrap;

        overflow-wrap: anywhere;
    }}

    .top-scalar-value {{
        font-size: 1.05rem;

        overflow-wrap: anywhere;
    }}

    /* ======================================================
       Arrays
       ====================================================== */

    .array-block {{
        margin:
            10px
            0
            20px
            0;
    }}

    .array-block > h3 {{
        margin-bottom: 12px;
    }}

    .array-items {{
        display: grid;

        gap: 14px;
    }}

    .array-item {{
        padding: 18px;

        border:
            1px
            solid
            #777777;

        border-radius: 10px;

        background:
            rgba(
                255,
                255,
                255,
                0.60
            );
    }}

    .item-number {{
        font-size: 0.82rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.06em;

        margin-bottom: 8px;
    }}

    .scalar-array-item {{
        padding:
            8px
            12px;

        border-left:
            3px
            solid
            #000000;

        background:
            rgba(
                255,
                255,
                255,
                0.55
            );

        white-space: pre-wrap;

        overflow-wrap: anywhere;
    }}

    /* ======================================================
       Special JSON values
       ====================================================== */

    .null-value {{
        font-style: italic;

        color: #000000;
    }}

    .boolean-value {{
        font-family:
            ui-monospace,
            "Cascadia Mono",
            Consolas,
            monospace;

        color: #000000;
    }}

    .empty-value {{
        font-family:
            ui-monospace,
            "Cascadia Mono",
            Consolas,
            monospace;

        color: #000000;

        padding:
            8px
            0;
    }}

    /* ======================================================
       Integrity information
       ====================================================== */

    .integrity {{
        margin-top: 32px;

        background: #eeeeee;

        border:
            1px
            solid
            var(--border);

        border-radius: 10px;

        padding: 18px;

        font-size: 0.9rem;
    }}

    .integrity code {{
        color: #000000;

        overflow-wrap: anywhere;
    }}

    /* ======================================================
       Original source JSON
       ====================================================== */

    details {{
        margin-top: 20px;

        background: #ffffff;

        border:
            1px
            solid
            var(--border);

        border-radius: 10px;

        padding: 16px;
    }}

    summary {{
        cursor: pointer;

        font-weight: 700;

        color: #000000;
    }}

    pre {{
        margin-top: 18px;

        overflow-x: auto;

        padding: 18px;

        background: #eeeeee;

        color: #000000;

        border:
            1px
            solid
            #777777;

        border-radius: 8px;

        white-space: pre-wrap;

        overflow-wrap: anywhere;
    }}

    /* ======================================================
       Mobile layout
       ====================================================== */

    @media (max-width: 700px) {{

        .page {{
            width:
                min(
                    calc(100% - 20px),
                    var(--page-width)
                );

            margin-top: 10px;
        }}

        .document-header,
        .top-section {{
            padding: 18px;
        }}

        .field-row {{
            grid-template-columns: 1fr;

            gap: 3px;
        }}
    }}

    /* ======================================================
       Print layout
       ====================================================== */

    @media print {{

        html,
        body {{
            background: #ffffff;
        }}

        .page {{
            width: 100%;

            margin: 0;
        }}

        .top-section,
        .array-item {{
            break-inside: avoid;
        }}

        /*
           Hide the full raw JSON when printing.
           It remains present in the HTML source.
        */

        details {{
            display: none;
        }}
    }}

</style>

</head>

<body>

<main class="page">

<header class="document-header">

    <h1>{html.escape(recipe_title)}</h1>

    {date_html}

</header>

{body_html}

<section class="integrity">

    <strong>Source integrity</strong>

    <div>
        Source JSON SHA-256:
        <code>{source_hash}</code>
    </div>

    <div>
        JSON paths checked:
        <code>{len(expected_paths)}</code>
    </div>

    <div>
        Missing JSON paths:
        <code>0</code>
    </div>

</section>

<details>

<summary>
Original source JSON
</summary>

<pre>{source_json_escaped}</pre>

</details>

</main>

</body>

</html>
"""


# ============================================================
# Command-line entry point
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Render recipe JSON into lossless, "
            "human-readable HTML."
        )
    )

    parser.add_argument(
        "input_json",
        help=(
            "Path to the source recipe JSON file."
        )
    )

    parser.add_argument(
        "output_html",
        nargs="?",
        default=None,
        help=(
            "Optional explicit HTML output path. "
            "If omitted, output/<JSON filename>.html "
            "is created automatically."
        )
    )

    parser.add_argument(
        "--date",
        dest="scheduled_date",
        default=None,
        help=(
            "Optional scheduled date to display exactly "
            "as entered, for example 16/09/2026."
        )
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help=(
            "Output directory used when output_html "
            "is not explicitly supplied. "
            "Default: output"
        )
    )

    args = parser.parse_args()

    input_path = Path(
        args.input_json
    )

    # --------------------------------------------------------
    # Determine output filename automatically
    # --------------------------------------------------------

    if args.output_html is not None:

        output_path = Path(
            args.output_html
        )

    else:

        output_directory = Path(
            args.output_dir
        )

        output_path = (
            output_directory
            /
            f"{input_path.stem}.html"
        )

    # --------------------------------------------------------
    # Read source JSON
    # --------------------------------------------------------

    raw_json_text = input_path.read_text(
        encoding="utf-8"
    )

    try:

        data = json.loads(
            raw_json_text
        )

    except json.JSONDecodeError as exc:

        raise SystemExit(
            "Invalid JSON.\n"
            f"Line: {exc.lineno}\n"
            f"Column: {exc.colno}\n"
            f"Error: {exc.msg}"
        )

    if not isinstance(data, dict):

        raise SystemExit(
            "The root JSON value must be an object."
        )

    # --------------------------------------------------------
    # Render HTML
    # --------------------------------------------------------

    rendered_html = build_html(
        data,
        raw_json_text,
        scheduled_date=args.scheduled_date
    )

    # --------------------------------------------------------
    # Create output directory if necessary
    # --------------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        rendered_html,
        encoding="utf-8"
    )

    print(
        f"Created: {output_path.resolve()}"
    )


if __name__ == "__main__":
    main()