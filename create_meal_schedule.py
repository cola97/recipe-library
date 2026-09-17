import json
import re
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "meal_schedule.json"

MEAL_ORDER = ['Breakfast', 'Morning snack', 'Lunch', 'Afternoon snack', 'Dinner', 'Evening snack']

PLAN = {
    "2026-09-16": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Toasted Walnuts",
        "Morning snack": "Clementine, Pistachio & Pumpkin Seed Snack Pots",
        "Lunch": "Harissa Tempeh, Roasted Pepper & Bulgur Salad with Lemon Yoghurt and Parsley",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Miso-Ginger Tofu, Broccoli & Brown Basmati Stir-Fry with Sesame and Edamame",
        "Evening snack": "Cocoa, Raspberry & Skyr Pots with Ground Flaxseed"
    },
    "2026-09-17": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Egg Muffins with Seeded Wholemeal Toast",
        "Morning snack": "Plum & Almond Skyr Pots with Cinnamon",
        "Lunch": "Cannellini Bean, Tomato & Wholewheat Pasta Salad with Basil Pesto and Rocket",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Red Lentil, Spinach & Cauliflower Dal with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Kiwi, Greek Yoghurt & Hemp Seed Pots"
    },
    "2026-09-18": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Toasted Walnuts",
        "Morning snack": "Clementine, Pistachio & Pumpkin Seed Snack Boxes",
        "Lunch": "Harissa Tempeh, Roasted Pepper & Bulgur Salad with Lemon Yoghurt and Parsley",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Smoky Black Bean & Mycoprotein Fajitas with Charred Peppers, Sweetcorn, Tomato Salsa and Lime Yoghurt",
        "Evening snack": "Cocoa, Raspberry & Skyr Pots with Ground Flaxseed"
    },
    "2026-09-19": {
        "Breakfast": "Raspberry-Lemon Protein Pancakes with Skyr and Pistachios",
        "Morning snack": "Plum, Almond & Cinnamon Yoghurt Pots",
        "Lunch": "Miso-Sesame Tofu & Edamame Soba Noodle Salad with Broccoli and Carrot",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Satsuma Segments",
        "Dinner": "Gochujang Tempeh, Aubergine & Mushroom Rice Bowls with Sesame Cabbage and Cucumber",
        "Evening snack": "Baked Plum & Quark Pots with Cinnamon and Walnuts"
    },
    "2026-09-20": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Shakshuka with Wholemeal Toast",
        "Morning snack": "Blackberry, Chia & Skyr Pots",
        "Lunch": "Beetroot, Green Lentil & Feta Wholegrain Wraps with Rocket and Dijon-Herb Yoghurt",
        "Afternoon snack": "Oatcakes with Hummus and Cucumber",
        "Dinner": "Herb-Roasted Seitan with Crispy Potatoes, Carrots, Savoy Cabbage and Mushroom-Onion Gravy",
        "Evening snack": "Orange & Cinnamon Skyr Pots with Toasted Walnuts"
    },
    "2026-09-21": {
        "Breakfast": "Skyr, Blackberry & Oat Breakfast Pots with Ground Flaxseed and Pumpkin Seeds",
        "Morning snack": "Kiwi & Unsalted Mixed Seed Snack Pots",
        "Lunch": "Cannellini Bean, Cottage Cheese & Roasted Courgette Wholewheat Pasta Salad with Basil and Lemon",
        "Afternoon snack": "Red Pepper & Cucumber Batons with Lemon Hummus",
        "Dinner": "Tomato, Mushroom & Mycoprotein Wholewheat Bolognese with Spinach and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-09-22": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Seeded Wholemeal Toast",
        "Morning snack": "Plum & Pistachio Snack Boxes",
        "Lunch": "Miso Tofu, Edamame & Brown Rice Salad with Broccoli and Sesame-Ginger Dressing",
        "Afternoon snack": "Smoky Roasted Broad Beans with Clementine",
        "Dinner": "Harissa Red Lentil, Chickpea & Cauliflower Stew with Bulgur and Lemon Yoghurt",
        "Evening snack": "Kiwi, Greek Yoghurt & Chia Pots"
    },
    "2026-09-23": {
        "Breakfast": "Raspberry-Cocoa Overnight Oats with Skyr, Hemp Seeds and Hazelnuts",
        "Morning snack": "Clementine & Walnut Snack Boxes",
        "Lunch": "Thai Peanut Tempeh Noodle Salad with Cucumber, Carrot and Peppers",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Lemon-Herb Mycoprotein, New Potato & Broccoli Traybake with Roasted Tomatoes",
        "Evening snack": "Vanilla Skyr Pots with Blackberries and Ground Flaxseed"
    },
    "2026-09-24": {
        "Breakfast": "Herbed Cottage Cheese & Egg Breakfast Wraps with Spinach and Tomato",
        "Morning snack": "Blackberry, Pistachio & Skyr Pots",
        "Lunch": "Curried Green Lentil, Cauliflower & Bulgur Salad with Mint Raita and Pumpkin Seeds",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Gochujang Tofu & Edamame Stir-Fry with Mushrooms, Broccoli and Brown Rice",
        "Evening snack": "Plum, Quark & Chia Pots"
    },
    "2026-09-25": {
        "Breakfast": "Cinnamon Protein Porridge with Plums, Walnuts and Skyr",
        "Morning snack": "Satsuma, Almond & Pumpkin Seed Snack Boxes",
        "Lunch": "Basil-Pesto Mycoprotein, Tomato & Wholewheat Pasta Salad with Rocket and Green Beans",
        "Afternoon snack": "Carrot Batons with Harissa Hummus",
        "Dinner": "Za’atar Tempeh & Roasted Aubergine Flatbreads with Tomato-Cucumber Salad and Tahini-Lemon Yoghurt",
        "Evening snack": "Raspberry-Cocoa Skyr Pots with Cacao Nibs"
    },
    "2026-09-26": {
        "Breakfast": "Sweetcorn, Black Bean & Cottage Cheese Breakfast Burritos with Scrambled Egg and Tomato Salsa",
        "Morning snack": "Blackberry, Walnut & Greek Yoghurt Pots",
        "Lunch": "Chimichurri Tofu, Roasted Beetroot & Quinoa Salad with Spinach and Pumpkin Seeds",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Jalfrezi Mycoprotein, Chickpea & Roasted Cauliflower Biryani with Cucumber-Mint Raita",
        "Evening snack": "Baked Plum Skyr Pots with Pistachios"
    },
    "2026-09-27": {
        "Breakfast": "Roasted Mushroom, Spinach & Cottage Cheese Frittata with Wholemeal Sourdough and Tomatoes",
        "Morning snack": "Raspberry, Chia & Almond Yoghurt Pots",
        "Lunch": "Harissa Butter Bean, Roasted Pepper & Bulgur Salad with Lemon Skyr and Parsley",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Rosemary Seitan & Cannellini Bean Casserole with Roasted Butternut Squash, Carrots and Crispy Herb Potatoes",
        "Evening snack": "Blackberry Quark Pots with Walnuts and Ground Flaxseed"
    },
    "2026-09-28": {
        "Breakfast": "Blackberry Skyr Overnight Oats with Chia, Hemp Seeds and Pistachios",
        "Morning snack": "Kiwi & Unsalted Mixed Nut Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Squash & Cottage Cheese Barley Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Red Pepper Batons with Smoky Chickpea Hummus",
        "Dinner": "Miso-Glazed Tempeh, Mushroom & Broccoli Soba Stir-Fry with Edamame",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Raspberries and Pumpkin Seeds"
    },
    "2026-09-29": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Breakfast Wraps with Rocket",
        "Morning snack": "Plum, Walnut & Skyr Pots",
        "Lunch": "Chipotle Black Bean & Mycoprotein Wholegrain Burrito Wraps with Sweetcorn, Cabbage Slaw and Lime Yoghurt",
        "Afternoon snack": "Rosemary Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Tomato-Braised Tofu, Butter Beans & Cavolo Nero with Wholegrain Couscous and Basil Gremolata",
        "Evening snack": "Kiwi Quark Pots with Chia and Toasted Hazelnuts"
    },
    "2026-09-30": {
        "Breakfast": "Spiced Pumpkin Protein Porridge with Skyr, Cinnamon, Pumpkin Seeds and Walnuts",
        "Morning snack": "Satsuma, Pistachio & Roasted Edamame Snack Boxes",
        "Lunch": "Chimichurri Tempeh, Roasted Beetroot & Bulgur Salad with Spinach and Lemon Yoghurt",
        "Afternoon snack": "Wholegrain Crackers with Whipped Cottage Cheese and Tomato Salsa",
        "Dinner": "Mushroom, Spinach & Mycoprotein Wholewheat Pasta with Rosemary Tomato Sauce and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Blackberry, Cocoa & Skyr Pots with Ground Flaxseed"
    }
}


def canonical_filename(title):
    text = unicodedata.normalize("NFKD", title)
    text = text.replace("’", "'").replace("&", " ")
    text = text.lower()
    text = re.sub(r"['’]", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    words = [
        word
        for word in text.split()
        if word not in {"and", "with"}
    ]
    return "_".join(words) + ".html"


def main():
    schedule = []

    for date in sorted(PLAN):
        for meal_type in MEAL_ORDER:
            title = PLAN[date][meal_type]

            schedule.append({
                "date": date,
                "meal_type": meal_type,
                "title": title,
                "file": canonical_filename(title),
            })

    OUTPUT_FILE.write_text(
        json.dumps(
            schedule,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Created: {OUTPUT_FILE.resolve()}"
    )

    print(
        f"Scheduled meals: {len(schedule)}"
    )


if __name__ == "__main__":
    main()
