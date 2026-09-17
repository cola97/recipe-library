import argparse
import html
import json
from fractions import Fraction
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# Basic helpers
# ============================================================

def esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def meaningful(value):
    return value not in (
        None,
        "",
        [],
        {},
    )


def format_number(value):
    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))

        return (
            f"{value:.4f}"
            .rstrip("0")
            .rstrip(".")
        )

    return str(value)


# ============================================================
# Fraction formatting
# ============================================================

UNICODE_FRACTIONS = {
    (1, 2): "½",
    (1, 3): "⅓",
    (2, 3): "⅔",
    (1, 4): "¼",
    (3, 4): "¾",
    (1, 5): "⅕",
    (2, 5): "⅖",
    (3, 5): "⅗",
    (4, 5): "⅘",
    (1, 6): "⅙",
    (5, 6): "⅚",
    (1, 8): "⅛",
    (3, 8): "⅜",
    (5, 8): "⅝",
    (7, 8): "⅞",
}


def format_fraction(value):
    """
    Convert numeric spoon quantities into readable fractions.

    Examples:
        0.5    -> ½
        0.25   -> ¼
        1.5    -> 1½
        0.0625 -> 1/16

    Old recipes containing very small spoon quantities are
    displayed exactly rather than rounded.
    """

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)

    fraction = Fraction(
        str(value)
    ).limit_denominator(32)

    if abs(
        float(fraction) - numeric
    ) > 0.000001:
        return format_number(value)

    sign = "-" if fraction < 0 else ""

    fraction = abs(fraction)

    whole = (
        fraction.numerator
        //
        fraction.denominator
    )

    remainder = (
        fraction.numerator
        %
        fraction.denominator
    )

    if remainder == 0:
        return f"{sign}{whole}"

    glyph = UNICODE_FRACTIONS.get(
        (
            remainder,
            fraction.denominator,
        )
    )

    if glyph:

        if whole:
            return (
                f"{sign}"
                f"{whole}"
                f"{glyph}"
            )

        return (
            f"{sign}"
            f"{glyph}"
        )

    fraction_text = (
        f"{remainder}"
        f"/"
        f"{fraction.denominator}"
    )

    if whole:

        return (
            f"{sign}"
            f"{whole} "
            f"{fraction_text}"
        )

    return (
        f"{sign}"
        f"{fraction_text}"
    )


def format_quantity(
    quantity,
    unit
):
    """
    Format ingredient quantities for the human cooking view.

    No conversion between units is performed.
    """

    if unit in (
        "tsp",
        "tbsp",
    ):
        number = format_fraction(
            quantity
        )

    else:
        number = format_number(
            quantity
        )

    if unit == "integer":
        return number

    return (
        f"{number} {unit}"
    )


# ============================================================
# Time formatting
# ============================================================

def format_duration(
    minimum,
    maximum
):

    if minimum is None and maximum is None:
        return None

    if (
        minimum is not None
        and
        maximum is not None
    ):

        if minimum == maximum:
            return (
                f"{format_number(minimum)} min"
            )

        return (
            f"{format_number(minimum)}"
            f"–"
            f"{format_number(maximum)} min"
        )

    if minimum is not None:
        return (
            f"{format_number(minimum)} min minimum"
        )

    return (
        f"up to {format_number(maximum)} min"
    )


# ============================================================
# HTML fragments
# ============================================================

def badge(text):
    return (
        '<span class="badge">'
        f'{esc(text)}'
        '</span>'
    )


def render_ingredients(data):

    ingredients = data.get(
        "ingredients",
        []
    )

    if not ingredients:
        return ""

    cards = []

    for item in ingredients:

        name = item.get(
            "display_name",
            ""
        )

        quantity = format_quantity(
            item.get(
                "quantity_used",
                ""
            ),
            item.get(
                "unit_used",
                ""
            )
        )

        purchase = item.get(
            "purchase_quantity"
        )

        preparation = item.get(
            "preparation"
        )

        parts = [
            '<article class="ingredient-card">',
            '<div class="ingredient-heading">',
            f'<strong>{esc(name)}</strong>',
            f'<span class="ingredient-quantity">{esc(quantity)}</span>',
            '</div>',
        ]

        if meaningful(purchase):
            parts.append(
                '<div class="subline">'
                '<strong>Buy:</strong> '
                f'{esc(purchase)}'
                '</div>'
            )

        if meaningful(preparation):
            parts.append(
                '<div class="subline">'
                '<strong>Prep:</strong> '
                f'{esc(preparation)}'
                '</div>'
            )

        parts.append(
            '</article>'
        )

        cards.append(
            "\n".join(parts)
        )

    return f"""
<details class="section non-method" open>
    <summary>Ingredients</summary>
    <div class="section-content ingredient-grid">
        {''.join(cards)}
    </div>
</details>
"""


def render_equipment(data):

    equipment = data.get(
        "equipment",
        []
    )

    if not equipment:
        return ""

    rows = []

    for item in equipment:

        name = item.get(
            "display_name"
        )

        if not meaningful(name):
            continue

        rows.append(
            '<li>'
            f'{esc(name)}'
            '</li>'
        )

    if not rows:
        return ""

    return f"""
<details class="section non-method">
    <summary>Equipment</summary>
    <div class="section-content">
        <ul class="compact-list">
            {''.join(rows)}
        </ul>
    </div>
</details>
"""


def render_mise_en_place(data):

    prep = data.get(
        "mise_en_place",
        []
    )

    if not prep:
        return ""

    cards = []

    for index, item in enumerate(
        prep,
        start=1
    ):

        instruction = item.get(
            "instruction"
        )

        endpoint = item.get(
            "endpoint"
        )

        if not meaningful(
            instruction
        ):
            continue

        parts = [
            '<article class="prep-card">',
            f'<h3>Prep {index}</h3>',
            f'<p>{esc(instruction)}</p>',
        ]

        if meaningful(endpoint):

            parts.append(
                '<div class="endpoint">'
                '<strong>Ready when:</strong> '
                f'{esc(endpoint)}'
                '</div>'
            )

        parts.append(
            '</article>'
        )

        cards.append(
            "\n".join(parts)
        )

    if not cards:
        return ""

    return f"""
<details class="section non-method" open>
    <summary>Mise en place</summary>
    <div class="section-content card-stack">
        {''.join(cards)}
    </div>
</details>
"""


def render_corrective_actions(
    actions
):

    if not actions:
        return ""

    rows = []

    for item in actions:

        condition = item.get(
            "condition"
        )

        action = item.get(
            "action"
        )

        if (
            not meaningful(condition)
            and
            not meaningful(action)
        ):
            continue

        text = ""

        if meaningful(condition):

            text += (
                '<strong>If:</strong> '
                f'{esc(condition)}'
            )

        if (
            meaningful(condition)
            and
            meaningful(action)
        ):
            text += "<br>"

        if meaningful(action):

            text += (
                '<strong>Do:</strong> '
                f'{esc(action)}'
            )

        rows.append(
            f'<li>{text}</li>'
        )

    if not rows:
        return ""

    return f"""
<details class="corrective">
    <summary>Corrective actions</summary>
    <ul>
        {''.join(rows)}
    </ul>
</details>
"""


def render_procedure(data):

    procedure = data.get(
        "procedure",
        []
    )

    if not procedure:
        return ""

    cards = []

    for index, step in enumerate(
        procedure,
        start=1
    ):

        title = (
            step.get("title")
            or
            f"Step {index}"
        )

        section = step.get(
            "section"
        )

        instruction = step.get(
            "instruction"
        )

        endpoint = step.get(
            "endpoint"
        )

        meta = []

        if meaningful(
            step.get(
                "heat_source"
            )
        ):
            meta.append(
                "Heat source: "
                +
                str(
                    step["heat_source"]
                )
            )

        if meaningful(
            step.get(
                "heat_level"
            )
        ):
            meta.append(
                "Setting: "
                +
                str(
                    step["heat_level"]
                )
            )

        if step.get(
            "temperature_c"
        ) is not None:
            meta.append(
                "Temperature: "
                +
                format_number(
                    step[
                        "temperature_c"
                    ]
                )
                +
                "°C"
            )

        duration = format_duration(
            step.get(
                "duration_min_minutes"
            ),
            step.get(
                "duration_max_minutes"
            )
        )

        if duration:
            meta.append(
                "Time: "
                +
                duration
            )

        corrective = (
            render_corrective_actions(
                step.get(
                    "corrective_actions",
                    []
                )
            )
        )

        parts = [
            (
                '<article '
                'class="method-step" '
                f'data-step-index="{index - 1}">'
            ),
            '<div class="step-heading">',
            f'<div class="step-number">Step {index}</div>',
            f'<h3>{esc(title)}</h3>',
            '</div>',
        ]

        if meaningful(section):
            parts.append(
                '<div class="step-section">'
                f'{esc(section)}'
                '</div>'
            )

        if meta:

            parts.append(
                '<div class="step-meta">'
                +
                "".join(
                    badge(item)
                    for item in meta
                )
                +
                '</div>'
            )

        if meaningful(instruction):

            parts.append(
                '<p class="instruction">'
                f'{esc(instruction)}'
                '</p>'
            )

        if meaningful(endpoint):

            parts.append(
                '<div class="endpoint">'
                '<strong>Ready when:</strong> '
                f'{esc(endpoint)}'
                '</div>'
            )

        if corrective:
            parts.append(
                corrective
            )

        parts.append(
            '</article>'
        )

        cards.append(
            "\n".join(parts)
        )

    return f"""
<section class="section method-section">
    <h2>Method</h2>

    <div id="methodSteps" class="card-stack">
        {''.join(cards)}
    </div>

    <div id="cookControls" class="cook-controls">
        <button
            id="previousStep"
            type="button"
        >
            Previous
        </button>

        <div id="stepCounter"></div>

        <button
            id="nextStep"
            type="button"
        >
            Next
        </button>
    </div>
</section>
"""


def render_plating(data):

    plating = data.get(
        "plating",
        []
    )

    instructions = [
        item.get(
            "instruction"
        )
        for item in plating
        if meaningful(
            item.get(
                "instruction"
            )
        )
    ]

    if not instructions:
        return ""

    paragraphs = "".join(
        f"<p>{esc(text)}</p>"
        for text in instructions
    )

    return f"""
<details class="section non-method">
    <summary>Serving</summary>
    <div class="section-content">
        {paragraphs}
    </div>
</details>
"""


def render_storage(data):

    storage = data.get(
        "storage",
        {}
    )

    if not storage:
        return ""

    rows = []

    refrigerator = storage.get(
        "refrigerator_days"
    )

    freezer = storage.get(
        "freezer_months"
    )

    instructions = storage.get(
        "storage_instructions"
    )

    reheating = storage.get(
        "reheating_methods",
        []
    )

    if refrigerator is not None:
        rows.append(
            '<p>'
            '<strong>Refrigerator:</strong> '
            f'{esc(format_number(refrigerator))} days'
            '</p>'
        )

    if freezer is not None:
        rows.append(
            '<p>'
            '<strong>Freezer:</strong> '
            f'{esc(format_number(freezer))} months'
            '</p>'
        )

    if meaningful(instructions):
        rows.append(
            f'<p>{esc(instructions)}</p>'
        )

    if reheating:

        reheating_rows = "".join(
            f'<li>{esc(method)}</li>'
            for method in reheating
            if meaningful(method)
        )

        if reheating_rows:

            rows.append(
                '<h3>Reheating</h3>'
                '<ul>'
                f'{reheating_rows}'
                '</ul>'
            )

    if not rows:
        return ""

    return f"""
<details class="section non-method">
    <summary>Storage & reheating</summary>
    <div class="section-content">
        {''.join(rows)}
    </div>
</details>
"""


def render_shopping(data):

    shopping = data.get(
        "shopping",
        {}
    )

    if not shopping:
        return ""

    groups = [
        (
            "Sainsbury's",
            shopping.get(
                "sainsburys",
                []
            )
        ),
        (
            "Marks & Spencer",
            shopping.get(
                "marks_and_spencer",
                []
            )
        ),
        (
            "Either retailer",
            shopping.get(
                "either_retailer",
                []
            )
        ),
    ]

    blocks = []

    for title, items in groups:

        useful_items = [
            item
            for item in items
            if meaningful(item)
        ]

        if not useful_items:
            continue

        rows = "".join(
            f"<li>{esc(item)}</li>"
            for item in useful_items
        )

        blocks.append(
            f"""
            <h3>{esc(title)}</h3>
            <ul>{rows}</ul>
            """
        )

    if not blocks:
        return ""

    return f"""
<details class="section non-method">
    <summary>Shopping</summary>
    <div class="section-content">
        {''.join(blocks)}
    </div>
</details>
"""


# ============================================================
# Document creation
# ============================================================

def build_html(
    data,
    scheduled_date=None
):

    recipe = data.get(
        "recipe",
        {}
    )

    nutrition = data.get(
        "nutrition_per_serving",
        {}
    )

    title = recipe.get(
        "title",
        "Recipe"
    )

    description = recipe.get(
        "description",
        ""
    )

    quick_facts = []

    if recipe.get(
        "servings"
    ) is not None:
        quick_facts.append(
            (
                "Serves",
                format_number(
                    recipe[
                        "servings"
                    ]
                )
            )
        )

    if meaningful(
        recipe.get(
            "difficulty"
        )
    ):
        quick_facts.append(
            (
                "Difficulty",
                recipe[
                    "difficulty"
                ]
            )
        )

    if recipe.get(
        "active_time_minutes"
    ) is not None:
        quick_facts.append(
            (
                "Active",
                (
                    f'{format_number(recipe["active_time_minutes"])} min'
                )
            )
        )

    if recipe.get(
        "total_time_minutes"
    ) is not None:
        quick_facts.append(
            (
                "Total",
                (
                    f'{format_number(recipe["total_time_minutes"])} min'
                )
            )
        )

    if nutrition.get(
        "energy_kcal"
    ) is not None:
        quick_facts.append(
            (
                "Energy",
                (
                    f'{format_number(nutrition["energy_kcal"])} kcal'
                )
            )
        )

    if nutrition.get(
        "protein_g"
    ) is not None:
        quick_facts.append(
            (
                "Protein",
                (
                    f'{format_number(nutrition["protein_g"])} g'
                )
            )
        )

    quick_fact_html = "".join(
        (
            '<div class="fact">'
            f'<span>{esc(label)}</span>'
            f'<strong>{esc(value)}</strong>'
            '</div>'
        )
        for label, value in quick_facts
    )

    tags = []

    for value in recipe.get(
        "meal_types",
        []
    ):
        tags.append(
            badge(value)
        )

    for value in recipe.get(
        "dietary_tags",
        []
    ):
        tags.append(
            badge(value)
        )

    allergens = recipe.get(
        "allergens",
        []
    )

    allergen_html = ""

    if allergens:

        allergen_html = (
            '<div class="allergens">'
            '<strong>Allergens:</strong> '
            +
            ", ".join(
                esc(value)
                for value in allergens
            )
            +
            '</div>'
        )

    date_html = ""

    if meaningful(
        scheduled_date
    ):

        date_html = (
            '<div class="scheduled-date">'
            f'{esc(scheduled_date)}'
            '</div>'
        )

    sections = "\n".join([
        render_ingredients(data),
        render_equipment(data),
        render_mise_en_place(data),
        render_procedure(data),
        render_plating(data),
        render_storage(data),
        render_shopping(data),
    ])

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1, viewport-fit=cover"
>

<title>{esc(title)}</title>

<style>

    :root {{
        --background: #f4f2ec;
        --panel: #ffffff;
        --text: #000000;
        --muted: #555555;
        --border: #b9b5ad;
        --accent: #e5f1dd;
        --endpoint: #fff4c6;
        --step: #f7f7f4;
    }}

    * {{
        box-sizing: border-box;

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }}

    html,
    body {{
        margin: 0;
        padding: 0;

        background: var(--background);
        color: var(--text);
    }}

    body {{
        min-height: 100vh;
        min-height: 100dvh;
    }}

    button,
    input,
    select,
    summary {{
        font: inherit;
    }}

    .page {{
        width: min(
            calc(100% - 24px),
            1050px
        );

        margin: 0 auto;

        padding:
            max(12px, env(safe-area-inset-top))
            0
            max(40px, env(safe-area-inset-bottom))
            0;
    }}

    .recipe-header {{
        position: static;

        background: transparent;

        padding:
            12px
            0
            10px
            0;

        border-bottom:
            1px
            solid
            var(--border);
    }}

    .title-row {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
    }}

    h1 {{
        margin: 0;

        font-size:
            clamp(
                1.65rem,
                5vw,
                2.8rem
            );

        line-height: 1.12;
    }}

    .description {{
        margin:
            12px
            0
            0
            0;

        line-height: 1.5;
    }}

    .scheduled-date {{
        margin-top: 8px;
        font-weight: 700;
    }}

    .tag-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;

        margin-top: 10px;
    }}

    .badge {{
        display: inline-block;

        padding:
            4px
            8px;

        border:
            1px
            solid
            var(--border);

        border-radius: 999px;

        background: #ffffff;

        color: #000000;

        font-size: 0.82rem;
    }}

    .allergens {{
        margin-top: 10px;

        padding:
            8px
            10px;

        border-radius: 8px;

        background: #ffe4df;
    }}

    .facts {{
        display: grid;

        grid-template-columns:
            repeat(
                auto-fit,
                minmax(90px, 1fr)
            );

        gap: 8px;

        margin:
            14px
            0;
    }}

    .fact {{
        display: grid;
        gap: 2px;

        padding: 9px;

        border:
            1px
            solid
            var(--border);

        border-radius: 9px;

        background: #ffffff;
    }}

    .fact span {{
        font-size: 0.78rem;
        color: var(--muted);
    }}

    .section {{
        display: block;

        margin-top: 14px;

        border:
            1px
            solid
            var(--border);

        border-radius: 12px;

        background: var(--panel);

        overflow: hidden;
    }}

    details.section > summary {{
        cursor: pointer;

        padding:
            15px
            16px;

        font-size: 1.12rem;

        font-weight: 800;

        background: var(--accent);
    }}

    .section-content {{
        padding: 14px;
    }}

    .method-section {{
        padding:
            14px;
    }}

    .method-section > h2 {{
        margin:
            0
            0
            12px
            0;
    }}

    .ingredient-grid {{
        display: grid;
        gap: 10px;
    }}

    .ingredient-card,
    .prep-card,
    .method-step {{
        padding: 14px;

        border:
            1px
            solid
            var(--border);

        border-radius: 10px;

        background: var(--step);
    }}

    .ingredient-heading {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 14px;
    }}

    .ingredient-quantity {{
        flex: 0 0 auto;

        font-weight: 800;

        white-space: nowrap;
    }}

    .subline {{
        margin-top: 7px;
        line-height: 1.4;
    }}

    .compact-list {{
        margin:
            0;
        padding-left:
            22px;
    }}

    .card-stack {{
        display: grid;
        gap: 12px;
    }}

    .prep-card h3,
    .method-step h3 {{
        margin:
            0;
    }}

    .prep-card p,
    .method-step p {{
        margin:
            10px
            0;
    }}

    .step-heading {{
        display: flex;
        align-items: baseline;
        gap: 10px;
    }}

    .step-number {{
        flex: 0 0 auto;

        font-size: 0.8rem;
        font-weight: 800;

        text-transform: uppercase;
    }}

    .step-section {{
        margin-top: 6px;

        font-size: 0.85rem;
        font-weight: 700;

        color: var(--muted);
    }}

    .step-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;

        margin-top: 10px;
    }}

    .instruction {{
        font-size: 1rem;
        line-height: 1.55;
    }}

    .endpoint {{
        margin-top: 10px;

        padding:
            10px
            12px;

        border-left:
            4px
            solid
            #000000;

        background: var(--endpoint);

        line-height: 1.45;
    }}

    .corrective {{
        margin-top: 10px;
    }}

    .corrective summary {{
        cursor: pointer;
        font-weight: 750;
    }}

    .corrective ul {{
        margin-bottom: 0;
    }}

    .cook-button {{
        flex: 0 0 auto;

        min-height: 42px;

        padding:
            8px
            12px;

        border:
            1px
            solid
            #000000;

        border-radius: 9px;

        background: #000000;
        color: #ffffff;

        font-weight: 750;
    }}

    .cook-controls {{
        display: none;

        position: sticky;

        bottom:
            max(
                8px,
                env(safe-area-inset-bottom)
            );

        z-index: 30;

        align-items: center;

        justify-content: space-between;

        gap: 10px;

        margin-top: 14px;

        padding: 10px;

        border:
            1px
            solid
            #000000;

        border-radius: 12px;

        background: #ffffff;
    }}

    .cook-controls button {{
        min-height: 44px;

        padding:
            8px
            14px;

        border:
            1px
            solid
            #000000;

        border-radius: 8px;

        background: #000000;
        color: #ffffff;

        font-weight: 750;
    }}

    /* ==========================================================
       Compact cook-mode header
       ========================================================== */

    body.cook-mode .recipe-header {{
        position: sticky;
        top: 0;
        z-index: 30;

        margin: 0;

        padding:
            6px
            0;

        background:
            rgba(
                244,
                242,
                236,
                0.98
            );

        border-bottom:
            1px
            solid
            var(--border);

        backdrop-filter:
            blur(8px);
    }}

    body.cook-mode .recipe-header .description,
    body.cook-mode .recipe-header .scheduled-date,
    body.cook-mode .recipe-header .tag-row,
    body.cook-mode .recipe-header .allergens,
    body.cook-mode .facts {{
        display: none;
    }}

    body.cook-mode .title-row {{
        display: grid;

        grid-template-columns:
            minmax(0, 1fr)
            auto;

        align-items: center;

        gap: 8px;
    }}

    body.cook-mode .recipe-header h1 {{
        margin: 0;

        font-size: 1rem;

        line-height: 1.2;

        white-space: nowrap;

        overflow: hidden;

        text-overflow: ellipsis;
    }}

    body.cook-mode .cook-button {{
        width: auto;

        min-height: 36px;

        padding:
            6px
            10px;

        font-size: 0.85rem;

        white-space: nowrap;
    }}

    body.cook-mode .method-section > h2 {{
        display: none;
    }}

    body.cook-mode .non-method {{
        display: none;
    }}

    body.cook-mode .method-step {{
        display: none;
    }}

    body.cook-mode .method-step.active {{
        display: block;
    }}

    body.cook-mode .cook-controls {{
        display: flex;
    }}

    body.cook-mode .method-section {{
        min-height:
            calc(100dvh - 60px);

        margin-top: 6px;
    }}

    @media (max-width: 600px) {{

        .page {{
            width:
                calc(100% - 12px);
        }}

        .recipe-header {{
            padding-top: 8px;
        }}

        .title-row {{
            display: grid;
            grid-template-columns: 1fr;
        }}

        .cook-button {{
            width: 100%;
        }}

        body.cook-mode .title-row {{
            grid-template-columns:
                minmax(0, 1fr)
                auto;
        }}

        body.cook-mode .cook-button {{
            width: auto;
        }}

        .ingredient-heading {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 3px;
        }}

        .ingredient-quantity {{
            white-space: normal;
        }}

        .method-section,
        .section-content {{
            padding: 10px;
        }}

        .ingredient-card,
        .prep-card,
        .method-step {{
            padding: 12px;
        }}

h1 {
    font-size: 1.35rem;

    line-height: 1.18;
}

.cook-button {
    width: auto;

    min-height: 36px;

    padding:
        6px
        12px;
}
    }}

    @media print {{

        .recipe-header {{
            position: static;
        }}

        .cook-button,
        .cook-controls {{
            display: none !important;
        }}

        body.cook-mode .non-method,
        body.cook-mode .method-step {{
            display: block;
        }}

        .section {{
            break-inside: avoid;
        }}
    }}
.recipe-info {
    margin-top: 10px;

    border:
        1px
        solid
        var(--border);

    border-radius: 9px;

    background: #ffffff;

    overflow: hidden;
}

.recipe-info > summary {
    cursor: pointer;

    padding:
        9px
        11px;

    font-weight: 750;
}

.recipe-info-content {
    padding:
        0
        11px
        11px
        11px;
}

</style>

</head>

<body>

<main class="page">

<header class="recipe-header">

    <div class="title-row">

        <h1>{esc(title)}</h1>

        <button
            id="cookModeButton"
            class="cook-button"
            type="button"
        >
            Cook mode
        </button>

    </div>

    {date_html}

    <details class="recipe-info">

        <summary>
            Recipe info
        </summary>

        <div class="recipe-info-content">

            <p class="description">
                {esc(description)}
            </p>

            <div class="tag-row">
                {''.join(tags)}
            </div>

            {allergen_html}

        </div>

    </details>

</header>

<div class="facts">
    {quick_fact_html}
</div>

{sections}

</main>


<script>

(function () {{

    const button =
        document.getElementById(
            "cookModeButton"
        );

    const steps =
        Array.from(
            document.querySelectorAll(
                ".method-step"
            )
        );

    const controls =
        document.getElementById(
            "cookControls"
        );

    const previous =
        document.getElementById(
            "previousStep"
        );

    const next =
        document.getElementById(
            "nextStep"
        );

    const counter =
        document.getElementById(
            "stepCounter"
        );

    let currentStep = 0;


    function showStep(index) {{

        if (!steps.length) {{
            return;
        }}

        currentStep =
            Math.max(
                0,
                Math.min(
                    index,
                    steps.length - 1
                )
            );

        steps.forEach(
            (step, stepIndex) => {{

                step.classList.toggle(
                    "active",
                    stepIndex === currentStep
                );

            }}
        );

        if (counter) {{

            counter.textContent =
                (
                    "Step "
                    +
                    (currentStep + 1)
                    +
                    " of "
                    +
                    steps.length
                );
        }}

        if (previous) {{
            previous.disabled =
                currentStep === 0;
        }}

        if (next) {{
            next.disabled =
                currentStep ===
                steps.length - 1;
        }}

        const active =
            steps[currentStep];

        if (active) {{

            active.scrollIntoView({{
                behavior: "smooth",
                block: "start"
            }});
        }}
    }}


    if (button) {{

        button.addEventListener(
            "click",
            () => {{

                const active =
                    document.body.classList.toggle(
                        "cook-mode"
                    );

                button.textContent =
                    active
                        ? "Exit cook mode"
                        : "Cook mode";

                if (active) {{
                    showStep(
                        currentStep
                    );
                }}
            }}
        );
    }}


    if (previous) {{

        previous.addEventListener(
            "click",
            () => {{
                showStep(
                    currentStep - 1
                );
            }}
        );
    }}


    if (next) {{

        next.addEventListener(
            "click",
            () => {{
                showStep(
                    currentStep + 1
                );
            }}
        );
    }}


    if (!steps.length && controls) {{
        controls.style.display = "none";
    }}

}})();

</script>

</body>

</html>
"""


# ============================================================
# Command-line entry point
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Render structured recipe JSON "
            "into compact human cooking HTML."
        )
    )

    parser.add_argument(
        "input_json",
        help=(
            "Path to the recipe JSON file."
        )
    )

    parser.add_argument(
        "output_html",
        nargs="?",
        default=None,
        help=(
            "Optional explicit output HTML path."
        )
    )

    parser.add_argument(
        "--date",
        dest="scheduled_date",
        default=None,
        help=(
            "Optional display date. "
            "Normally scheduling is handled by the app."
        )
    )

    args = parser.parse_args()

    input_path = Path(
        args.input_json
    )

    if not input_path.exists():

        raise SystemExit(
            f"Input file not found: {input_path}"
        )

    raw_text = input_path.read_text(
        encoding="utf-8"
    )

    try:

        data = json.loads(
            raw_text
        )

    except json.JSONDecodeError as exc:

        raise SystemExit(
            "Invalid JSON.\n"
            f"Line: {exc.lineno}\n"
            f"Column: {exc.colno}\n"
            f"Error: {exc.msg}"
        )

    if not isinstance(
        data,
        dict
    ):

        raise SystemExit(
            "Recipe JSON root must be an object."
        )

    if args.output_html:

        output_path = Path(
            args.output_html
        )

    else:

        output_path = (
            DEFAULT_OUTPUT_DIR
            /
            f"{input_path.stem}.html"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        build_html(
            data,
            scheduled_date=args.scheduled_date
        ),
        encoding="utf-8"
    )

    print(
        f"Created: {output_path.resolve()}"
    )


if __name__ == "__main__":
    main()