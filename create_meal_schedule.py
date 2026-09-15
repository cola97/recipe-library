import json
import re
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "meal_schedule.json"


PLAN = {
    "2026-09-16": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Toasted Walnuts",
        "Morning snack": "Clementine, Pistachio & Pumpkin Seed Snack Pots",
        "Lunch": "Harissa Tempeh, Roasted Pepper & Bulgur Salad with Lemon Yoghurt and Parsley",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Miso-Ginger Tofu, Broccoli & Brown Basmati Stir-Fry with Sesame and Edamame",
        "Evening snack": "Cocoa, Raspberry & Skyr Pots with Ground Flaxseed",
    },

    "2026-09-17": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Egg Muffins with Seeded Wholemeal Toast",
        "Morning snack": "Plum & Almond Skyr Pots with Cinnamon",
        "Lunch": "Cannellini Bean, Tomato & Wholewheat Pasta Salad with Basil Pesto and Rocket",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Red Lentil, Spinach & Cauliflower Dal with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Kiwi, Greek Yoghurt & Hemp Seed Pots",
    },

    "2026-09-18": {
        "Breakfast": "Vanilla Protein Porridge with Raspberries, Chia and Pistachios",
        "Morning snack": "Satsuma, Walnut & Pumpkin Seed Snack Boxes",
        "Lunch": "Chimichurri Seitan, Roasted Courgette & Wholegrain Couscous Salad with Cherry Tomatoes",
        "Afternoon snack": "Rye Crispbreads with Whipped Cottage Cheese and Roasted Red Pepper",
        "Dinner": "Smoky Black Bean & Mycoprotein Tacos with Charred Sweetcorn, Tomato Salsa, Avocado and Lime Yoghurt",
        "Evening snack": "Dark Cocoa Skyr Pots with Strawberries and Cacao Nibs",
    },

    "2026-09-19": {
        "Breakfast": "Savoury Harissa Tofu Scramble with Edamame, Roasted Tomatoes and Wholemeal Flatbread",
        "Morning snack": "Blackberry, Almond & Cinnamon Yoghurt Pots",
        "Lunch": "Thai Peanut Tempeh Noodle Salad with Cucumber, Carrot, Peppers and Fresh Herbs",
        "Afternoon snack": "Lime-Chilli Roasted Edamame with Satsuma Segments",
        "Dinner": "Chermoula Seitan, Aubergine & Chickpea Couscous with Roasted Peppers, Lemon Yoghurt and Pistachios",
        "Evening snack": "Baked Plum, Quark & Walnut Pots with Cinnamon",
    },

    "2026-09-20": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Shakshuka with Wholegrain Toast",
        "Morning snack": "Raspberry, Chia & Skyr Pots",
        "Lunch": "Roasted Beetroot, Green Lentil & Goat’s Cheese Salad with Walnuts and Dijon Vinaigrette",
        "Afternoon snack": "Oatcakes with Hummus, Cucumber and Pumpkin Seeds",
        "Dinner": "Herb-Roasted Seitan with Crispy Potatoes, Roasted Carrots, Savoy Cabbage and Mushroom-Onion Gravy",
        "Evening snack": "Blackberry & Greek Yoghurt Pots with Toasted Hazelnuts",
    },

    "2026-09-21": {
        "Breakfast": "Skyr, Blackberry & Oat Breakfast Bowls with Ground Flaxseed and Pumpkin Seeds",
        "Morning snack": "Plum & Pistachio Snack Pots",
        "Lunch": "Roast Seitan, Crispy Potato & Savoy Cabbage Salad with Mustard-Herb Dressing",
        "Afternoon snack": "Red Pepper & Cucumber Batons with Lemon-Tahini Hummus",
        "Dinner": "Tomato, Mushroom & Mycoprotein Mince Wholewheat Bolognese with Spinach and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Cinnamon Quark with Raspberries and Walnuts",
    },

    "2026-09-22": {
        "Breakfast": "Mushroom, Spinach & Egg-White Cottage Cheese Scramble with Rye Toast and Tomatoes",
        "Morning snack": "Kiwi, Pumpkin Seed & Skyr Pot",
        "Lunch": "Miso-Sesame Tofu & Edamame Soba Noodle Salad with Broccoli and Carrot",
        "Afternoon snack": "Smoky Roasted Broad Beans with Clementine",
        "Dinner": "Harissa Chickpea, Red Lentil & Roasted Cauliflower Stew with Bulgur and Lemon Yoghurt",
        "Evening snack": "Cocoa Cottage Cheese Pot with Strawberries and Chia",
    },

    "2026-09-23": {
        "Breakfast": "Raspberry, Cocoa & Skyr Overnight Oats with Hemp Seeds and Hazelnuts",
        "Morning snack": "Satsuma & Unsalted Mixed Nut Snack Box",
        "Lunch": "Mediterranean Tempeh, Cannellini Bean & Roasted Courgette Wholegrain Wrap with Basil Yoghurt",
        "Afternoon snack": "Rye Crispbread with Peanut Butter and Plum Slices",
        "Dinner": "Thai Red Curry Tofu with Green Beans, Peppers, Edamame and Jasmine-Brown Rice Blend",
        "Evening snack": "Vanilla Greek Yoghurt with Blackberries and Ground Flaxseed",
    },

    "2026-09-24": {
        "Breakfast": "Herbed Cottage Cheese, Egg & Spinach Breakfast Wrap with Tomato and Rocket",
        "Morning snack": "Blackberry, Pistachio & Skyr Pot",
        "Lunch": "Curried Green Lentil, Cauliflower & Bulgur Salad with Mint Raita and Pumpkin Seeds",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber and Red Pepper",
        "Dinner": "Smoky Tempeh, Black Bean & Sweet Potato Chilli with Lime Yoghurt and Avocado",
        "Evening snack": "Kiwi, Quark & Chia Pot with Toasted Almonds",
    },

    "2026-09-25": {
        "Breakfast": "Cinnamon Protein Porridge with Plums, Walnuts and Skyr",
        "Morning snack": "Clementine, Almond & Pumpkin Seed Snack Box",
        "Lunch": "Pesto Tofu, Tomato & Wholewheat Pasta Salad with Rocket, Green Beans and Edamame",
        "Afternoon snack": "Carrot Batons with Harissa Hummus and Sesame",
        "Dinner": "Gochujang Mycoprotein & Mushroom Rice Bowls with Sesame Broccoli, Cucumber and Vegetarian Kimchi",
        "Evening snack": "Raspberry Cocoa Skyr Pot with Cacao Nibs",
    },

    "2026-09-26": {
        "Breakfast": "Sweetcorn, Black Bean & Cottage Cheese Breakfast Burritos with Scrambled Egg and Tomato Salsa",
        "Morning snack": "Blackberry, Walnut & Greek Yoghurt Pots",
        "Lunch": "Za’atar Tofu, Roasted Aubergine & Chickpea Pitta Pockets with Tomato, Cucumber and Tahini-Lemon Dressing",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Mushroom, Spinach & Green Lentil Wellington-Style Filo Pie with Roasted Squash, Tenderstem Broccoli and Red-Wine Onion Gravy",
        "Evening snack": "Cinnamon Baked Plum Skyr Pots with Pistachios",
    },

    "2026-09-27": {
        "Breakfast": "Roasted Mushroom, Spinach & Cottage Cheese Frittata with Wholemeal Sourdough and Tomatoes",
        "Morning snack": "Raspberry, Chia & Almond Yoghurt Pots",
        "Lunch": "Harissa Butter Bean, Roasted Pepper & Quinoa Salad with Lemon Yoghurt and Parsley",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Rosemary Seitan & Cannellini Bean Casserole with Roasted Butternut Squash, Carrots and Crispy Herb Potatoes",
        "Evening snack": "Blackberry Quark with Toasted Walnuts and Ground Flaxseed",
    },

    "2026-09-28": {
        "Breakfast": "Blackberry, Skyr & Oat Bircher Pots with Chia, Hemp and Pistachios",
        "Morning snack": "Kiwi & Unsalted Mixed Nut Snack Box",
        "Lunch": "Rosemary Seitan, Cannellini Bean & Roasted Squash Barley Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Red Pepper Batons with Smoky Chickpea Hummus",
        "Dinner": "Miso-Glazed Tempeh, Mushroom & Tenderstem Broccoli Soba Stir-Fry with Edamame and Sesame",
        "Evening snack": "Cocoa Greek Yoghurt with Raspberries and Pumpkin Seeds",
    },

    "2026-09-29": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Seeded Toast and Rocket",
        "Morning snack": "Plum, Walnut & Skyr Pot",
        "Lunch": "Chipotle Black Bean & Mycoprotein Wholegrain Burrito Wrap with Sweetcorn, Cabbage Slaw and Lime Yoghurt",
        "Afternoon snack": "Rosemary Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Tomato-Braised Butter Beans, Tofu & Cavolo Nero with Wholegrain Couscous and Basil Gremolata",
        "Evening snack": "Kiwi Quark Pot with Chia and Toasted Hazelnuts",
    },

    "2026-09-30": {
        "Breakfast": "Spiced Pumpkin Protein Porridge with Skyr, Cinnamon, Pumpkin Seeds and Walnuts",
        "Morning snack": "Satsuma, Pistachio & Roasted Edamame Snack Box",
        "Lunch": "Chimichurri Tempeh, Roasted Beetroot & Bulgur Salad with Spinach and Lemon Yoghurt",
        "Afternoon snack": "Wholegrain Crackers with Whipped Cottage Cheese and Tomato Salsa",
        "Dinner": "Jalfrezi Tofu, Chickpea & Roasted Cauliflower Curry with Brown Basmati Rice and Cucumber-Mint Raita",
        "Evening snack": "Blackberry, Cocoa & Skyr Pots with Ground Flaxseed",
    },
}


def make_filename(title):
    """
    Generate the canonical HTML filename from the recipe title.

    Example:

    Blackberry, Skyr & Jumbo Oat Overnight Pots
    with Chia and Toasted Walnuts

    becomes:

    blackberry_skyr_jumbo_oat_overnight_pots_
    chia_toasted_walnuts.html
    """

    text = (
        title
        .replace("’", "")
        .replace("'", "")
        .replace("&", " ")
    )

    text = (
        unicodedata
        .normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )

    words = re.findall(
        r"[a-z0-9]+",
        text
    )

    # These connector words are intentionally omitted.
    words = [
        word
        for word in words
        if word not in {
            "and",
            "with"
        }
    ]

    return "_".join(words) + ".html"


schedule = []

for date, meals in PLAN.items():

    for meal_type, title in meals.items():

        schedule.append({
            "date": date,
            "meal_type": meal_type,
            "title": title,
            "file": make_filename(title),
        })


# Safety checks

if len(schedule) != 90:
    raise RuntimeError(
        f"Expected 90 meals, found {len(schedule)}."
    )


filenames = [
    item["file"]
    for item in schedule
]

if len(filenames) != len(set(filenames)):
    raise RuntimeError(
        "Two planned meals generated the same filename."
    )


OUTPUT_FILE.write_text(
    json.dumps(
        schedule,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print(
    f"Created: {OUTPUT_FILE}"
)

print(
    f"Scheduled meals: {len(schedule)}"
)

print(
    f"Dates: {len(PLAN)}"
)