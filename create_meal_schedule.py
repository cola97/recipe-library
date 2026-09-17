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
    },
    "2026-10-01": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Ground Flaxseed",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Miso Tempeh, Edamame & Brown Rice Salad with Broccoli and Sesame-Ginger Dressing",
        "Afternoon snack": "Carrot & Cucumber Batons with Lemon Hummus",
        "Dinner": "Tomato-Braised Butter Beans, Tofu & Cavolo Nero with Wholegrain Couscous and Basil Gremolata",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-10-02": {
        "Breakfast": "Cinnamon Protein Porridge with Plums, Skyr and Walnuts",
        "Morning snack": "Kiwi & Pumpkin Seed Snack Pots",
        "Lunch": "Basil-Pesto Mycoprotein, Tomato & Wholewheat Pasta Salad with Rocket and Green Beans",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Chipotle Black Bean & Mycoprotein Tacos with Charred Sweetcorn, Cabbage Slaw and Lime Yoghurt",
        "Evening snack": "Blackberry Skyr Pots with Cacao Nibs"
    },
    "2026-10-03": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Shakshuka with Seeded Wholemeal Toast",
        "Morning snack": "Raspberry, Almond & Greek Yoghurt Pots",
        "Lunch": "Za’atar Tofu, Roasted Aubergine & Bulgur Salad with Cucumber and Tahini-Lemon Dressing",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Chermoula Seitan, Roasted Squash & Chickpea Couscous with Charred Peppers and Lemon Yoghurt",
        "Evening snack": "Baked Plum & Quark Pots with Cinnamon"
    },
    "2026-10-04": {
        "Breakfast": "Roasted Mushroom, Spinach & Cottage Cheese Frittata with Wholemeal Sourdough",
        "Morning snack": "Blackberry, Chia & Skyr Pots",
        "Lunch": "Harissa Butter Bean, Beetroot & Rocket Wholegrain Wraps with Mint Yoghurt",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Rosemary Seitan Roast with Crispy Potatoes, Roasted Carrots, Savoy Cabbage and Mushroom-Onion Gravy",
        "Evening snack": "Orange, Cinnamon & Greek Yoghurt Pots with Walnuts"
    },
    "2026-10-05": {
        "Breakfast": "Raspberry-Cocoa Overnight Oats with Skyr and Hemp Seeds",
        "Morning snack": "Clementine & Unsalted Mixed Nut Snack Boxes",
        "Lunch": "Cannellini Bean, Cottage Cheese & Roasted Squash Barley Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Red Pepper Batons with Smoky Chickpea Hummus",
        "Dinner": "Mushroom, Spinach & Mycoprotein Wholewheat Bolognese with Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Kiwi Quark Pots with Ground Flaxseed"
    },
    "2026-10-06": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Seeded Wholemeal Toast",
        "Morning snack": "Plum & Pistachio Skyr Pots",
        "Lunch": "Gochujang Tofu & Edamame Soba Noodle Salad with Broccoli and Carrot",
        "Afternoon snack": "Rosemary Roasted Chickpeas with Cucumber Sticks",
        "Dinner": "Red Lentil, Cauliflower & Spinach Dal with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Blackberries"
    },
    "2026-10-07": {
        "Breakfast": "Blackberry Skyr Breakfast Bowls with Jumbo Oats, Chia and Pumpkin Seeds",
        "Morning snack": "Kiwi & Walnut Snack Boxes",
        "Lunch": "Mediterranean Tempeh, Cannellini Bean & Roasted Courgette Wholegrain Wraps with Basil Yoghurt",
        "Afternoon snack": "Carrot Batons with Lemon-Tahini Hummus",
        "Dinner": "Miso-Ginger Mycoprotein, Mushroom & Broccoli Stir-Fry with Brown Rice",
        "Evening snack": "Raspberry Cottage Cheese Pots with Cinnamon"
    },
    "2026-10-08": {
        "Breakfast": "Vanilla Protein Porridge with Raspberries, Flaxseed and Almonds",
        "Morning snack": "Satsuma & Pumpkin Seed Snack Boxes",
        "Lunch": "Curried Green Lentil, Cauliflower & Bulgur Salad with Mint Raita",
        "Afternoon snack": "Wholegrain Crackers with Whipped Cottage Cheese and Cucumber",
        "Dinner": "Smoky Tempeh, Black Bean & Sweet Potato Chilli with Lime Yoghurt",
        "Evening snack": "Kiwi Skyr Pots with Chia"
    },
    "2026-10-09": {
        "Breakfast": "Herbed Cottage Cheese, Egg & Spinach Breakfast Wraps with Tomato",
        "Morning snack": "Blackberry & Pistachio Yoghurt Pots",
        "Lunch": "Harissa Tofu, Roasted Pepper & Quinoa Salad with Parsley and Lemon Yoghurt",
        "Afternoon snack": "Paprika Roasted Broad Beans with Clementine",
        "Dinner": "Gochujang Mycoprotein & Mushroom Rice Bowls with Sesame Broccoli, Cucumber and Vegetarian Kimchi",
        "Evening snack": "Cocoa Quark Pots with Raspberries and Hazelnuts"
    },
    "2026-10-10": {
        "Breakfast": "Sweetcorn, Black Bean & Cottage Cheese Breakfast Burritos with Scrambled Egg and Tomato Salsa",
        "Morning snack": "Kiwi, Walnut & Greek Yoghurt Pots",
        "Lunch": "Chimichurri Tempeh, Roasted Beetroot & Bulgur Salad with Spinach",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Mushroom, Spinach & Green Lentil Filo Pie with Roasted Butternut Squash and Red-Wine Onion Gravy",
        "Evening snack": "Cinnamon Baked Plum Skyr Pots with Pistachios"
    },
    "2026-10-11": {
        "Breakfast": "Savoury Tofu Scramble with Mushrooms, Spinach, Tomatoes and Wholemeal Toast",
        "Morning snack": "Raspberry, Chia & Almond Yoghurt Pots",
        "Lunch": "Roasted Cauliflower, Chickpea & Cottage Cheese Grain Salad with Harissa-Lemon Dressing",
        "Afternoon snack": "Oatcakes with Hummus and Red Pepper",
        "Dinner": "Rosemary Seitan & Cannellini Bean Casserole with Carrots, Leeks and Crispy Herb Potatoes",
        "Evening snack": "Blackberry Quark Pots with Toasted Walnuts"
    },
    "2026-10-12": {
        "Breakfast": "Blackberry, Skyr & Oat Overnight Pots with Ground Flaxseed",
        "Morning snack": "Clementine & Almond Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Carrot & Cottage Cheese Wholewheat Pasta Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Cucumber & Pepper Batons with Lemon Hummus",
        "Dinner": "Thai Red Curry Tofu with Green Beans, Peppers, Edamame and Brown Basmati Rice",
        "Evening snack": "Cocoa Skyr Pots with Raspberries"
    },
    "2026-10-13": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Kiwi & Pistachio Snack Pots",
        "Lunch": "Miso Tempeh, Edamame & Soba Noodle Salad with Cabbage and Carrot",
        "Afternoon snack": "Smoky Roasted Chickpeas with Cucumber",
        "Dinner": "Tomato, Aubergine & Mycoprotein Wholewheat Pasta with Basil and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Orange & Cinnamon Greek Yoghurt Pots"
    },
    "2026-10-14": {
        "Breakfast": "Raspberry Protein Porridge with Skyr, Chia and Pumpkin Seeds",
        "Morning snack": "Satsuma & Walnut Snack Boxes",
        "Lunch": "Chipotle Black Bean & Mycoprotein Wholegrain Burrito Wraps with Sweetcorn and Cabbage",
        "Afternoon snack": "Carrot Batons with Edamame Hummus",
        "Dinner": "Harissa Red Lentil, Chickpea & Roasted Squash Stew with Bulgur and Mint Yoghurt",
        "Evening snack": "Kiwi Quark Pots with Ground Flaxseed"
    },
    "2026-10-15": {
        "Breakfast": "Herbed Cottage Cheese & Egg Breakfast Wraps with Spinach and Tomato",
        "Morning snack": "Blackberry & Pumpkin Seed Skyr Pots",
        "Lunch": "Pesto Tofu, Green Bean & Wholewheat Pasta Salad with Rocket and Tomatoes",
        "Afternoon snack": "Paprika Roasted Broad Beans with Clementine",
        "Dinner": "Miso-Glazed Tempeh, Mushroom & Broccoli Stir-Fry with Brown Rice and Edamame",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Raspberries"
    },
    "2026-10-16": {
        "Breakfast": "Cinnamon Overnight Oats with Skyr, Plum and Walnuts",
        "Morning snack": "Kiwi & Almond Snack Boxes",
        "Lunch": "Za’atar Mycoprotein, Roasted Pepper & Bulgur Salad with Cucumber and Lemon Yoghurt",
        "Afternoon snack": "Wholegrain Crackers with Whipped Cottage Cheese and Tomato Salsa",
        "Dinner": "Smoky Black Bean & Tofu Enchiladas with Roasted Peppers, Tomato Salsa and Lime Yoghurt",
        "Evening snack": "Blackberry Quark Pots with Cacao Nibs"
    },
    "2026-10-17": {
        "Breakfast": "Mushroom, Spinach & Cottage Cheese Omelette with Seeded Toast and Roasted Tomatoes",
        "Morning snack": "Raspberry & Pistachio Skyr Pots",
        "Lunch": "Miso-Sesame Tofu, Edamame & Brown Rice Salad with Cucumber and Cabbage",
        "Afternoon snack": "Chilli-Lime Roasted Chickpeas with Satsuma",
        "Dinner": "Ras el Hanout Tempeh, Roasted Squash & Cauliflower Tagine with Chickpeas and Wholegrain Couscous",
        "Evening snack": "Baked Plum Greek Yoghurt Pots with Cinnamon"
    },
    "2026-10-18": {
        "Breakfast": "Blackberry, Skyr & Protein Pancakes with Toasted Hazelnuts",
        "Morning snack": "Kiwi, Chia & Yoghurt Pots",
        "Lunch": "Green Lentil, Beetroot & Feta Wholegrain Pitta Pockets with Rocket and Dijon Yoghurt",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Herb-Roasted Mycoprotein Loaf with Crispy Potatoes, Savoy Cabbage, Carrots and Mushroom Gravy",
        "Evening snack": "Cocoa Quark Pots with Orange Zest"
    },
    "2026-10-19": {
        "Breakfast": "Raspberry-Cocoa Skyr Overnight Oats with Flaxseed",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Butter Bean, Roasted Squash & Cottage Cheese Barley Salad with Lemon-Herb Dressing",
        "Afternoon snack": "Red Pepper Batons with Smoky Hummus",
        "Dinner": "Gochujang Tofu, Mushroom & Green Bean Stir-Fry with Brown Rice and Edamame",
        "Evening snack": "Blackberry Greek Yoghurt Pots with Pumpkin Seeds"
    },
    "2026-10-20": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Wholemeal Toast",
        "Morning snack": "Kiwi & Walnut Skyr Pots",
        "Lunch": "Curried Green Lentil & Cauliflower Bulgur Pots with Mint Raita",
        "Afternoon snack": "Rosemary Roasted Chickpeas with Cucumber",
        "Dinner": "Tomato-Braised Tempeh, Cannellini Beans & Cavolo Nero with Wholegrain Couscous",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-10-21": {
        "Breakfast": "Cinnamon Protein Porridge with Blackberries, Skyr and Chia",
        "Morning snack": "Satsuma & Almond Snack Boxes",
        "Lunch": "Harissa Mycoprotein, Roasted Carrot & Quinoa Salad with Spinach and Lemon Yoghurt",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Thai Green Curry Tofu with Broccoli, Peppers, Green Beans and Jasmine-Brown Rice",
        "Evening snack": "Kiwi Cottage Cheese Pots with Ground Flaxseed"
    },
    "2026-10-22": {
        "Breakfast": "Mushroom, Spinach & Cottage Cheese Breakfast Wraps with Scrambled Egg",
        "Morning snack": "Blackberry & Pumpkin Seed Yoghurt Pots",
        "Lunch": "Miso Tempeh, Edamame & Wholewheat Noodle Salad with Cabbage and Carrot",
        "Afternoon snack": "Paprika Roasted Broad Beans with Clementine",
        "Dinner": "Mycoprotein, Red Lentil & Mushroom Cottage Pie with Carrot-Swede Mash and Peas",
        "Evening snack": "Raspberry Skyr Pots with Cacao Nibs"
    },
    "2026-10-23": {
        "Breakfast": "Vanilla Overnight Oats with Skyr, Kiwi and Pistachios",
        "Morning snack": "Satsuma & Walnut Snack Boxes",
        "Lunch": "Basil-Pesto Tofu, Tomato & Green Bean Wholewheat Pasta Salad with Rocket",
        "Afternoon snack": "Cucumber Sticks with Harissa Hummus",
        "Dinner": "Chipotle Tempeh & Black Bean Burgers with Cabbage Slaw, Tomato and Air-Fried Sweet Potato Wedges",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Blackberries"
    },
    "2026-10-24": {
        "Breakfast": "Shakshuka with Eggs, Cottage Cheese, Spinach and Wholemeal Toast",
        "Morning snack": "Raspberry, Chia & Almond Skyr Pots",
        "Lunch": "Chermoula Tofu, Roasted Cauliflower & Chickpea Couscous Salad with Parsley",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Clementine",
        "Dinner": "Mushroom, Spinach & Seitan Stroganoff with Barley and Roasted Green Beans",
        "Evening snack": "Baked Plum Quark Pots with Cinnamon and Walnuts"
    },
    "2026-10-25": {
        "Breakfast": "Roasted Mushroom, Leek & Cottage Cheese Frittata with Seeded Sourdough",
        "Morning snack": "Kiwi & Pistachio Greek Yoghurt Pots",
        "Lunch": "Harissa Butter Bean, Roasted Beetroot & Bulgur Salad with Mint Yoghurt",
        "Afternoon snack": "Oatcakes with Hummus and Cucumber",
        "Dinner": "Mustard-Herb Seitan with Roasted Squash, Crispy Potatoes, Brussels Sprouts and Onion Gravy",
        "Evening snack": "Blackberry Skyr Pots with Ground Flaxseed"
    },
    "2026-10-26": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia",
        "Morning snack": "Clementine & Mixed Nut Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Squash & Cottage Cheese Wholegrain Wraps with Rocket and Dijon Dressing",
        "Afternoon snack": "Red Pepper & Cucumber Batons with Edamame Hummus",
        "Dinner": "Miso-Ginger Mycoprotein, Broccoli & Mushroom Soba Stir-Fry with Edamame",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-10-27": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Kiwi & Pumpkin Seed Skyr Pots",
        "Lunch": "Chipotle Black Bean, Sweetcorn & Mycoprotein Brown Rice Salad with Lime Yoghurt",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Jalfrezi Tofu, Chickpea & Cauliflower Curry with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Orange & Cinnamon Greek Yoghurt Pots"
    },
    "2026-10-28": {
        "Breakfast": "Raspberry Protein Porridge with Skyr, Hemp Seeds and Hazelnuts",
        "Morning snack": "Satsuma & Almond Snack Boxes",
        "Lunch": "Mediterranean Tempeh, Roasted Pepper & Bulgur Salad with Spinach and Basil Yoghurt",
        "Afternoon snack": "Carrot Batons with Lemon Hummus",
        "Dinner": "Lentil, Mushroom & Mycoprotein Wholewheat Pasta with Rosemary Tomato Sauce and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Kiwi Quark Pots with Chia"
    },
    "2026-10-29": {
        "Breakfast": "Herbed Cottage Cheese, Mushroom & Egg Breakfast Wraps with Spinach",
        "Morning snack": "Blackberry & Pistachio Skyr Pots",
        "Lunch": "Miso Tofu, Edamame & Soba Noodle Salad with Broccoli and Carrot",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Clementine",
        "Dinner": "Smoky Tempeh, Butter Bean & Sweet Potato Chilli with Lime Yoghurt",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Raspberries"
    },
    "2026-10-30": {
        "Breakfast": "Cinnamon Overnight Oats with Skyr, Blackberries and Walnuts",
        "Morning snack": "Kiwi & Pumpkin Seed Snack Boxes",
        "Lunch": "Za’atar Mycoprotein, Roasted Cauliflower & Wholegrain Couscous Salad with Cucumber and Lemon Yoghurt",
        "Afternoon snack": "Wholegrain Crackers with Whipped Cottage Cheese and Tomato Salsa",
        "Dinner": "Harissa Tofu & Roasted Aubergine Flatbreads with Cabbage Slaw, Tomato and Tahini-Lemon Yoghurt",
        "Evening snack": "Raspberry Quark Pots with Cacao Nibs"
    },
    "2026-10-31": {
        "Breakfast": "Spiced Pumpkin Protein Pancakes with Skyr, Cinnamon and Toasted Pecans",
        "Morning snack": "Blackberry & Chia Greek Yoghurt Pots",
        "Lunch": "Warm Green Lentil, Roasted Squash & Tempeh Salad with Spinach and Dijon-Herb Dressing",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Smoky Mycoprotein, Black Bean & Mushroom Chilli-Stuffed Roasted Squash with Lime Yoghurt",
        "Evening snack": "Dark Cocoa Skyr Pots with Orange Zest and Pumpkin Seeds"
    },
    "2026-11-01": {
        "Breakfast": "Mushroom, Leek & Cottage Cheese Frittata with Seeded Wholemeal Toast",
        "Morning snack": "Clementine, Pistachio & Pumpkin Seed Pots",
        "Lunch": "Harissa Butter Bean, Roasted Beetroot & Bulgur Salad with Lemon Yoghurt",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Mustard-Herb Seitan Roast with Crispy Potatoes, Carrots, Brussels Sprouts and Mushroom-Onion Gravy",
        "Evening snack": "Cinnamon Quark Pots with Orange and Walnuts"
    },
    "2026-11-02": {
        "Breakfast": "Raspberry-Cocoa Skyr Overnight Oats with Ground Flaxseed",
        "Morning snack": "Kiwi & Almond Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Carrot & Cottage Cheese Barley Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Red Pepper Batons with Lemon Hummus",
        "Dinner": "Miso-Ginger Tempeh, Broccoli & Mushroom Soba Stir-Fry with Edamame",
        "Evening snack": "Blackberry Greek Yoghurt Pots with Chia"
    },
    "2026-11-03": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Satsuma & Walnut Snack Boxes",
        "Lunch": "Chipotle Black Bean & Mycoprotein Wholegrain Wraps with Cabbage, Sweetcorn and Lime Yoghurt",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Red Lentil, Cauliflower & Spinach Dal with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-11-04": {
        "Breakfast": "Vanilla Protein Porridge with Frozen Berries and Pumpkin Seeds",
        "Morning snack": "Clementine & Pistachio Snack Pots",
        "Lunch": "Miso Tofu, Edamame & Brown Rice Salad with Broccoli and Sesame-Ginger Dressing",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Tomato, Mushroom & Mycoprotein Wholewheat Bolognese with Spinach and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Kiwi Skyr Pots with Ground Flaxseed"
    },
    "2026-11-05": {
        "Breakfast": "Herbed Cottage Cheese, Egg & Spinach Breakfast Wraps with Tomato",
        "Morning snack": "Orange & Almond Snack Boxes",
        "Lunch": "Curried Green Lentil, Roasted Cauliflower & Bulgur Salad with Mint Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Cucumber",
        "Dinner": "Smoky Tempeh, Black Bean & Sweet Potato Chilli with Lime Yoghurt",
        "Evening snack": "Cinnamon Greek Yoghurt Pots with Blackberries"
    },
    "2026-11-06": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia",
        "Morning snack": "Kiwi & Pumpkin Seed Snack Pots",
        "Lunch": "Basil-Pesto Mycoprotein, Green Bean & Wholewheat Pasta Salad with Rocket",
        "Afternoon snack": "Red Pepper & Carrot Batons with Harissa Hummus",
        "Dinner": "Gochujang Tofu & Edamame Rice Bowls with Sesame Broccoli, Mushrooms and Vegetarian Kimchi",
        "Evening snack": "Cocoa Cottage Cheese Pots with Raspberries"
    },
    "2026-11-07": {
        "Breakfast": "Sweetcorn, Black Bean & Cottage Cheese Breakfast Burritos with Scrambled Egg and Tomato Salsa",
        "Morning snack": "Clementine, Walnut & Greek Yoghurt Pots",
        "Lunch": "Za’atar Tempeh, Roasted Squash & Chickpea Couscous Salad with Lemon Yoghurt",
        "Afternoon snack": "Chilli-Lime Roasted Edamame",
        "Dinner": "Mushroom, Spinach & Green Lentil Filo Pie with Roasted Carrots and Red-Wine Onion Gravy",
        "Evening snack": "Warm Spiced Blackberry Skyr Pots with Hazelnuts"
    },
    "2026-11-08": {
        "Breakfast": "Tofu Scramble with Chestnut Mushrooms, Spinach, Tomatoes and Wholemeal Toast",
        "Morning snack": "Kiwi, Chia & Skyr Pots",
        "Lunch": "Beetroot, Puy Lentil & Feta Wholemeal Pitta Pockets with Rocket and Dijon Yoghurt",
        "Afternoon snack": "Oatcakes with Smoky Chickpea Hummus",
        "Dinner": "Rosemary Seitan & Cannellini Bean Casserole with Leeks, Carrots and Crispy Herb Potatoes",
        "Evening snack": "Orange, Cocoa & Quark Pots"
    },
    "2026-11-09": {
        "Breakfast": "Cinnamon Protein Porridge with Frozen Raspberries and Skyr",
        "Morning snack": "Satsuma & Pistachio Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Squash & Cottage Cheese Wholegrain Wraps with Spinach and Mustard Dressing",
        "Afternoon snack": "Cucumber Sticks with Lemon-Tahini Hummus",
        "Dinner": "Thai Red Curry Mycoprotein with Green Beans, Peppers and Brown Basmati Rice",
        "Evening snack": "Blackberry Greek Yoghurt Pots with Ground Flaxseed"
    },
    "2026-11-10": {
        "Breakfast": "Mushroom, Spinach & Cottage Cheese Egg Muffins with Seeded Toast",
        "Morning snack": "Kiwi & Unsalted Mixed Nut Snack Boxes",
        "Lunch": "Harissa Tofu, Roasted Carrot & Quinoa Salad with Parsley and Lemon Yoghurt",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Tomato-Braised Tempeh, Butter Beans & Cavolo Nero with Wholegrain Couscous",
        "Evening snack": "Cocoa Skyr Pots with Orange Zest"
    },
    "2026-11-11": {
        "Breakfast": "Frozen Berry, Skyr & Oat Breakfast Pots with Hemp Seeds",
        "Morning snack": "Clementine & Pumpkin Seed Snack Boxes",
        "Lunch": "Miso Tempeh, Edamame & Soba Noodle Salad with Cabbage and Carrot",
        "Afternoon snack": "Red Pepper Batons with Edamame Hummus",
        "Dinner": "Lentil, Mushroom & Mycoprotein Cottage Pie with Carrot-Swede Mash and Peas",
        "Evening snack": "Kiwi Quark Pots with Cinnamon"
    },
    "2026-11-12": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Breakfast Wraps with Scrambled Egg",
        "Morning snack": "Orange & Walnut Snack Boxes",
        "Lunch": "Mediterranean Mycoprotein, Cannellini Bean & Bulgur Salad with Roasted Peppers and Basil Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Cucumber",
        "Dinner": "Miso-Glazed Tofu, Broccoli & Mushroom Stir-Fry with Brown Rice and Edamame",
        "Evening snack": "Raspberry Greek Yoghurt Pots with Chia"
    },
    "2026-11-13": {
        "Breakfast": "Cocoa Protein Porridge with Blackberries and Almonds",
        "Morning snack": "Kiwi & Pistachio Snack Pots",
        "Lunch": "Pesto Tofu, Green Bean & Wholewheat Pasta Salad with Spinach",
        "Afternoon snack": "Carrot Batons with Smoky Hummus",
        "Dinner": "Chipotle Tempeh & Black Bean Burgers with Red Cabbage Slaw and Air-Fried Sweet Potato Wedges",
        "Evening snack": "Clementine Skyr Pots with Cacao Nibs"
    },
    "2026-11-14": {
        "Breakfast": "Shakshuka with Eggs, Cottage Cheese, Spinach and Wholemeal Toast",
        "Morning snack": "Frozen Berry, Walnut & Skyr Pots",
        "Lunch": "Chimichurri Tofu, Roasted Beetroot & Barley Salad with Watercress",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Ras el Hanout Seitan, Chickpea & Roasted Squash Tagine with Wholewheat Couscous",
        "Evening snack": "Cinnamon Quark Pots with Kiwi and Pistachios"
    },
    "2026-11-15": {
        "Breakfast": "Mushroom, Leek & Cottage Cheese Omelette with Rye Toast and Wilted Spinach",
        "Morning snack": "Clementine, Chia & Greek Yoghurt Pots",
        "Lunch": "Harissa Butter Bean, Roasted Cauliflower & Bulgur Salad with Mint Yoghurt",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Herb-Roasted Mycoprotein Loaf with Crispy Potatoes, Savoy Cabbage, Carrots and Mushroom Gravy",
        "Evening snack": "Cocoa Blackberry Skyr Pots with Ground Flaxseed"
    },
    "2026-11-16": {
        "Breakfast": "Raspberry-Cinnamon Skyr Overnight Oats with Pumpkin Seeds",
        "Morning snack": "Kiwi & Almond Snack Boxes",
        "Lunch": "Green Lentil, Roasted Carrot & Cottage Cheese Barley Salad with Dijon Dressing",
        "Afternoon snack": "Red Pepper Batons with Lemon Hummus",
        "Dinner": "Gochujang Tempeh, Mushroom & Broccoli Noodle Stir-Fry with Edamame",
        "Evening snack": "Orange Quark Pots with Cinnamon"
    },
    "2026-11-17": {
        "Breakfast": "Spinach & Cottage Cheese Egg Muffins with Wholemeal Toast and Tomatoes",
        "Morning snack": "Satsuma & Walnut Snack Boxes",
        "Lunch": "Chipotle Black Bean & Mycoprotein Brown Rice Salad with Sweetcorn and Lime Yoghurt",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Jalfrezi Tofu, Chickpea & Cauliflower Curry with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Blackberry Greek Yoghurt Pots with Chia"
    },
    "2026-11-18": {
        "Breakfast": "Blackberry Protein Porridge with Skyr and Ground Flaxseed",
        "Morning snack": "Kiwi & Pistachio Snack Pots",
        "Lunch": "Za’atar Tempeh, Roasted Squash & Wholewheat Couscous Salad with Spinach",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Mycoprotein, Mushroom & Spinach Wholewheat Pasta with Rosemary Tomato Sauce",
        "Evening snack": "Cocoa Cottage Cheese Pots with Frozen Raspberries"
    },
    "2026-11-19": {
        "Breakfast": "Herbed Cottage Cheese & Egg Breakfast Wraps with Mushrooms and Spinach",
        "Morning snack": "Clementine & Pumpkin Seed Snack Boxes",
        "Lunch": "Curried Red Lentil, Cauliflower & Bulgur Pots with Lemon Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Red Pepper",
        "Dinner": "Mustard-Herb Tempeh, Brussels Sprouts & Carrot Traybake with Crispy New Potatoes",
        "Evening snack": "Kiwi Skyr Pots with Cacao Nibs"
    },
    "2026-11-20": {
        "Breakfast": "Frozen Berry, Skyr & Jumbo Oat Overnight Pots with Hemp Seeds",
        "Morning snack": "Orange & Almond Snack Boxes",
        "Lunch": "Miso Tofu, Edamame & Soba Noodle Salad with Broccoli and Red Cabbage",
        "Afternoon snack": "Cucumber Sticks with Harissa Hummus",
        "Dinner": "Smoky Mycoprotein & Black Bean Enchiladas with Roasted Peppers and Lime Yoghurt",
        "Evening snack": "Cocoa Quark Pots with Blackberries"
    },
    "2026-11-21": {
        "Breakfast": "Savoury Tempeh, Mushroom & Spinach Breakfast Hash with Cottage Cheese and Potatoes",
        "Morning snack": "Kiwi, Walnut & Greek Yoghurt Pots",
        "Lunch": "Chermoula Tofu, Roasted Carrot & Chickpea Quinoa Salad with Parsley",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Clementine",
        "Dinner": "Spinach, Mushroom & Green Lentil Lasagne with Rosemary Tomato Sauce and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Raspberry Skyr Pots with Toasted Hazelnuts"
    },
    "2026-11-22": {
        "Breakfast": "Cottage Cheese, Spinach & Mushroom Frittata with Seeded Wholemeal Toast",
        "Morning snack": "Satsuma, Chia & Skyr Pots",
        "Lunch": "Beetroot, Butter Bean & Feta Wholegrain Wraps with Rocket and Mustard Yoghurt",
        "Afternoon snack": "Oatcakes with Smoky Chickpea Hummus",
        "Dinner": "Mustard Seitan, Leek & Cannellini Bean Pot Pie with Roasted Carrots and Savoy Cabbage",
        "Evening snack": "Orange-Cocoa Quark Pots with Walnuts"
    },
    "2026-11-23": {
        "Breakfast": "Cinnamon Skyr Overnight Oats with Frozen Blackberries and Flaxseed",
        "Morning snack": "Kiwi & Pistachio Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Squash & Cottage Cheese Wholewheat Pasta Salad with Spinach",
        "Afternoon snack": "Carrot & Cucumber Batons with Lemon Hummus",
        "Dinner": "Thai Green Curry Tempeh with Broccoli, Green Beans and Brown Basmati Rice",
        "Evening snack": "Raspberry Greek Yoghurt Pots with Pumpkin Seeds"
    },
    "2026-11-24": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Clementine & Almond Snack Boxes",
        "Lunch": "Harissa Mycoprotein, Roasted Cauliflower & Bulgur Salad with Lemon Yoghurt",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Tomato-Braised Tofu, Butter Beans & Cavolo Nero with Wholegrain Couscous",
        "Evening snack": "Kiwi Quark Pots with Chia"
    },
    "2026-11-25": {
        "Breakfast": "Cocoa Protein Porridge with Frozen Raspberries and Skyr",
        "Morning snack": "Orange & Walnut Snack Boxes",
        "Lunch": "Miso Tempeh, Edamame & Brown Rice Salad with Cabbage and Carrot",
        "Afternoon snack": "Red Pepper Batons with Edamame Hummus",
        "Dinner": "Smoky Red Lentil, Mycoprotein & Mushroom Chilli with Sweet Potato and Lime Yoghurt",
        "Evening snack": "Blackberry Cottage Cheese Pots with Cinnamon"
    },
    "2026-11-26": {
        "Breakfast": "Herbed Cottage Cheese, Mushroom & Egg Breakfast Wraps with Spinach",
        "Morning snack": "Kiwi & Pumpkin Seed Snack Pots",
        "Lunch": "Pesto Tofu, Green Bean & Wholewheat Pasta Salad with Rocket",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Clementine",
        "Dinner": "Miso-Ginger Mycoprotein, Broccoli & Mushroom Stir-Fry with Soba Noodles",
        "Evening snack": "Cocoa Skyr Pots with Ground Flaxseed"
    },
    "2026-11-27": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia",
        "Morning snack": "Satsuma & Pistachio Snack Boxes",
        "Lunch": "Chipotle Black Bean, Sweetcorn & Tempeh Wholegrain Wraps with Red Cabbage and Lime Yoghurt",
        "Afternoon snack": "Carrot Batons with Smoky Hummus",
        "Dinner": "Harissa Tofu & Roasted Squash Flatbreads with Cabbage Slaw and Tahini-Lemon Yoghurt",
        "Evening snack": "Kiwi Quark Pots with Cacao Nibs"
    },
    "2026-11-28": {
        "Breakfast": "Spiced Pumpkin Protein Pancakes with Skyr and Toasted Walnuts",
        "Morning snack": "Orange, Almond & Greek Yoghurt Pots",
        "Lunch": "Warm Puy Lentil, Roasted Beetroot & Tempeh Salad with Spinach and Dijon-Herb Dressing",
        "Afternoon snack": "Chilli-Lime Roasted Edamame",
        "Dinner": "Mushroom, Leek & Seitan Stroganoff with Pearl Barley and Roasted Green Beans",
        "Evening snack": "Cocoa Raspberry Skyr Pots with Pistachios"
    },
    "2026-11-29": {
        "Breakfast": "Tofu Scramble with Chestnut Mushrooms, Spinach and Seeded Wholemeal Toast",
        "Morning snack": "Kiwi, Chia & Quark Pots",
        "Lunch": "Harissa Chickpea, Roasted Carrot & Cottage Cheese Bulgur Salad with Parsley",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Rosemary Mycoprotein & Cannellini Bean Casserole with Butternut Squash, Brussels Sprouts and Crispy Potatoes",
        "Evening snack": "Clementine Greek Yoghurt Pots with Walnuts"
    },
    "2026-11-30": {
        "Breakfast": "Frozen Berry, Skyr & Oat Breakfast Pots with Ground Flaxseed",
        "Morning snack": "Satsuma & Almond Snack Boxes",
        "Lunch": "Curried Green Lentil, Roasted Cauliflower & Cottage Cheese Barley Salad with Mint Yoghurt",
        "Afternoon snack": "Red Pepper & Cucumber Batons with Lemon Hummus",
        "Dinner": "Gochujang Tofu, Edamame & Mushroom Brown Rice Stir-Fry with Broccoli",
        "Evening snack": "Cocoa Quark Pots with Orange Zest"
    },
    "2026-12-01": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Ground Flaxseed",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Miso Tofu, Edamame & Brown Rice Salad with Broccoli and Sesame-Ginger Dressing",
        "Afternoon snack": "Carrot & Cucumber Batons with Lemon Hummus",
        "Dinner": "Mushroom, Spinach & Mycoprotein Wholewheat Bolognese with Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Cocoa Quark Pots with Frozen Raspberries"
    },
    "2026-12-02": {
        "Breakfast": "Cinnamon Protein Porridge with Skyr, Blackberries and Pumpkin Seeds",
        "Morning snack": "Kiwi & Walnut Snack Boxes",
        "Lunch": "Green Lentil, Roasted Carrot & Cottage Cheese Barley Salad with Dijon-Herb Dressing",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Miso-Ginger Tempeh, Broccoli & Mushroom Soba Stir-Fry with Edamame",
        "Evening snack": "Orange & Cinnamon Greek Yoghurt Pots"
    },
    "2026-12-03": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Egg Muffins with Seeded Wholemeal Toast",
        "Morning snack": "Satsuma & Almond Snack Boxes",
        "Lunch": "Harissa Mycoprotein, Roasted Cauliflower & Bulgur Salad with Lemon Yoghurt",
        "Afternoon snack": "Red Pepper Batons with Edamame Hummus",
        "Dinner": "Gochujang Tofu, Edamame & Green Bean Brown Rice Stir-Fry with Sesame",
        "Evening snack": "Blackberry Skyr Pots with Chia"
    },
    "2026-12-04": {
        "Breakfast": "Raspberry-Cocoa Skyr Overnight Oats with Hemp Seeds",
        "Morning snack": "Clementine & Pumpkin Seed Snack Pots",
        "Lunch": "Chickpea, Cottage Cheese & Roasted Squash Wholegrain Wraps with Rocket and Mint Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Cucumber",
        "Dinner": "Smoky Black Bean & Mycoprotein Tacos with Red Cabbage Slaw, Charred Sweetcorn and Lime Yoghurt",
        "Evening snack": "Cocoa Quark Pots with Orange Zest"
    },
    "2026-12-05": {
        "Breakfast": "Shakshuka with Eggs, Cottage Cheese, Spinach and Wholemeal Toast",
        "Morning snack": "Kiwi, Chia & Greek Yoghurt Pots",
        "Lunch": "Za’atar Tempeh, Roasted Beetroot & Wholewheat Couscous Salad with Lemon Yoghurt",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Clementine",
        "Dinner": "Rosemary Seitan, Cannellini Bean & Mushroom Casserole with Crispy Potatoes and Savoy Cabbage",
        "Evening snack": "Warm Spiced Blackberry Skyr Pots with Toasted Hazelnuts"
    },
    "2026-12-06": {
        "Breakfast": "Tofu Scramble with Chestnut Mushrooms, Spinach and Seeded Wholemeal Toast",
        "Morning snack": "Orange, Walnut & Skyr Pots",
        "Lunch": "Puy Lentil, Roasted Carrot & Feta Wholemeal Pitta Pockets with Watercress and Mustard Yoghurt",
        "Afternoon snack": "Oatcakes with Smoky Chickpea Hummus",
        "Dinner": "Herb-Roasted Mycoprotein Loaf with Crispy Potatoes, Brussels Sprouts, Carrots and Mushroom-Onion Gravy",
        "Evening snack": "Raspberry Quark Pots with Ground Flaxseed"
    },
    "2026-12-07": {
        "Breakfast": "Frozen Berry, Skyr & Oat Breakfast Pots with Chia",
        "Morning snack": "Kiwi & Pistachio Snack Boxes",
        "Lunch": "Miso Tofu, Edamame & Soba Noodle Salad with Cabbage and Carrot",
        "Afternoon snack": "Red Pepper & Cucumber Batons with Lemon Hummus",
        "Dinner": "Red Lentil, Cauliflower & Spinach Dal with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Cocoa Greek Yoghurt Pots with Blackberries"
    },
    "2026-12-08": {
        "Breakfast": "Herbed Cottage Cheese & Egg Breakfast Wraps with Spinach and Tomato",
        "Morning snack": "Clementine & Almond Snack Boxes",
        "Lunch": "Mediterranean Mycoprotein, Cannellini Bean & Bulgur Salad with Roasted Peppers and Basil Yoghurt",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Mustard-Herb Tempeh, Brussels Sprouts & Carrot Traybake with Crispy New Potatoes",
        "Evening snack": "Kiwi Skyr Pots with Ground Flaxseed"
    },
    "2026-12-09": {
        "Breakfast": "Vanilla Protein Porridge with Frozen Raspberries and Walnuts",
        "Morning snack": "Satsuma & Pumpkin Seed Snack Pots",
        "Lunch": "Curried Green Lentil, Roasted Cauliflower & Cottage Cheese Barley Salad with Mint Yoghurt",
        "Afternoon snack": "Carrot Batons with Edamame Hummus",
        "Dinner": "Thai Green Curry Tofu with Broccoli, Green Beans, Edamame and Brown Basmati Rice",
        "Evening snack": "Cocoa Quark Pots with Orange Zest"
    },
    "2026-12-10": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Ground Flaxseed",
        "Morning snack": "Kiwi & Walnut Snack Boxes",
        "Lunch": "Basil-Pesto Tempeh, Green Bean & Wholewheat Pasta Salad with Spinach",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Red Pepper",
        "Dinner": "Tomato-Braised Butter Beans, Mycoprotein & Cavolo Nero with Wholegrain Couscous",
        "Evening snack": "Raspberry Greek Yoghurt Pots with Chia"
    },
    "2026-12-11": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Chipotle Black Bean & Mycoprotein Brown Rice Salad with Sweetcorn, Cabbage and Lime Yoghurt",
        "Afternoon snack": "Cucumber Sticks with Harissa Hummus",
        "Dinner": "Za’atar Tofu & Roasted Squash Flatbreads with Red Cabbage, Tomato and Tahini-Lemon Yoghurt",
        "Evening snack": "Cocoa Skyr Pots with Cacao Nibs"
    },
    "2026-12-12": {
        "Breakfast": "Sweetcorn, Black Bean & Cottage Cheese Breakfast Burritos with Scrambled Egg and Tomato Salsa",
        "Morning snack": "Kiwi, Almond & Greek Yoghurt Pots",
        "Lunch": "Chimichurri Tempeh, Roasted Beetroot & Quinoa Salad with Watercress",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Satsuma",
        "Dinner": "Mushroom, Spinach & Green Lentil Lasagne with Rosemary Tomato Sauce and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Blackberry Quark Pots with Toasted Walnuts"
    },
    "2026-12-13": {
        "Breakfast": "Mushroom, Leek & Cottage Cheese Frittata with Seeded Wholemeal Toast",
        "Morning snack": "Clementine, Chia & Skyr Pots",
        "Lunch": "Harissa Butter Bean, Roasted Cauliflower & Bulgur Salad with Lemon Yoghurt",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Mustard-Herb Seitan Roast with Crispy Potatoes, Carrots, Savoy Cabbage and Mushroom Gravy",
        "Evening snack": "Orange-Cocoa Greek Yoghurt Pots with Hazelnuts"
    },
    "2026-12-14": {
        "Breakfast": "Raspberry-Cinnamon Skyr Overnight Oats with Pumpkin Seeds",
        "Morning snack": "Kiwi & Mixed Nut Snack Boxes",
        "Lunch": "Cannellini Bean, Roasted Squash & Cottage Cheese Wholewheat Pasta Salad with Spinach",
        "Afternoon snack": "Carrot & Cucumber Batons with Lemon Hummus",
        "Dinner": "Miso-Glazed Tempeh, Mushroom & Broccoli Stir-Fry with Brown Rice and Edamame",
        "Evening snack": "Blackberry Quark Pots with Ground Flaxseed"
    },
    "2026-12-15": {
        "Breakfast": "Cocoa Protein Porridge with Skyr, Frozen Blackberries and Almonds",
        "Morning snack": "Clementine & Pumpkin Seed Snack Pots",
        "Lunch": "Harissa Tofu, Roasted Carrot & Quinoa Salad with Parsley and Lemon Yoghurt",
        "Afternoon snack": "Smoked Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Mycoprotein, Red Lentil & Mushroom Cottage Pie with Carrot-Swede Mash and Peas",
        "Evening snack": "Kiwi Greek Yoghurt Pots with Chia"
    },
    "2026-12-16": {
        "Breakfast": "Spinach, Mushroom & Cottage Cheese Breakfast Wraps with Scrambled Egg",
        "Morning snack": "Satsuma & Walnut Snack Boxes",
        "Lunch": "Miso Tempeh, Edamame & Soba Noodle Salad with Red Cabbage and Carrot",
        "Afternoon snack": "Red Pepper Batons with Edamame Hummus",
        "Dinner": "Tomato, Aubergine & Mycoprotein Wholewheat Pasta with Basil and Vegetarian Parmesan-Style Cheese",
        "Evening snack": "Cocoa Skyr Pots with Raspberries"
    },
    "2026-12-17": {
        "Breakfast": "Frozen Berry, Skyr & Jumbo Oat Overnight Pots with Hemp Seeds",
        "Morning snack": "Kiwi & Pistachio Snack Boxes",
        "Lunch": "Curried Red Lentil, Roasted Cauliflower & Cottage Cheese Bulgur Pots with Mint Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Cucumber",
        "Dinner": "Gochujang Tofu, Edamame, Mushroom & Broccoli Brown Rice Stir-Fry",
        "Evening snack": "Orange & Cinnamon Quark Pots"
    },
    "2026-12-18": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Seeded Toast",
        "Morning snack": "Clementine & Almond Snack Boxes",
        "Lunch": "Pesto Mycoprotein, Green Bean & Wholewheat Pasta Salad with Rocket",
        "Afternoon snack": "Carrot Batons with Smoky Chickpea Hummus",
        "Dinner": "Chipotle Tempeh & Black Bean Burgers with Red Cabbage Slaw and Air-Fried Sweet Potato Wedges",
        "Evening snack": "Blackberry Greek Yoghurt Pots with Cacao Nibs"
    },
    "2026-12-19": {
        "Breakfast": "Spiced Pumpkin Protein Pancakes with Skyr and Toasted Walnuts",
        "Morning snack": "Kiwi, Chia & Greek Yoghurt Pots",
        "Lunch": "Chermoula Tofu, Roasted Squash & Chickpea Couscous Salad with Parsley",
        "Afternoon snack": "Chilli-Lime Roasted Edamame with Clementine",
        "Dinner": "Mushroom, Leek & Seitan Stroganoff with Pearl Barley and Roasted Green Beans",
        "Evening snack": "Cocoa Raspberry Skyr Pots with Pistachios"
    },
    "2026-12-20": {
        "Breakfast": "Roasted Mushroom, Spinach & Cottage Cheese Omelette with Rye Toast",
        "Morning snack": "Satsuma, Walnut & Skyr Pots",
        "Lunch": "Beetroot, Green Lentil & Feta Wholegrain Wraps with Watercress and Dijon Yoghurt",
        "Afternoon snack": "Oatcakes with Lemon Hummus and Cucumber",
        "Dinner": "Rosemary Mycoprotein & Cannellini Bean Casserole with Butternut Squash, Brussels Sprouts and Crispy Potatoes",
        "Evening snack": "Orange-Cocoa Quark Pots with Ground Flaxseed"
    },
    "2026-12-21": {
        "Breakfast": "Blackberry Skyr Overnight Oats with Chia and Pumpkin Seeds",
        "Morning snack": "Kiwi & Almond Snack Boxes",
        "Lunch": "Miso Tofu, Edamame & Brown Rice Salad with Broccoli and Sesame-Ginger Dressing",
        "Afternoon snack": "Red Pepper Batons with Edamame Hummus",
        "Dinner": "Smoky Tempeh, Black Bean & Sweet Potato Chilli with Lime Yoghurt",
        "Evening snack": "Raspberry Greek Yoghurt Pots with Cinnamon"
    },
    "2026-12-22": {
        "Breakfast": "Cinnamon Protein Porridge with Skyr, Frozen Raspberries and Walnuts",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Za’atar Mycoprotein, Roasted Cauliflower & Bulgur Salad with Lemon Yoghurt",
        "Afternoon snack": "Paprika Roasted Chickpeas with Cucumber",
        "Dinner": "Thai Red Curry Tofu with Green Beans, Broccoli, Edamame and Brown Basmati Rice",
        "Evening snack": "Cocoa Quark Pots with Orange Zest"
    },
    "2026-12-23": {
        "Breakfast": "Herbed Cottage Cheese, Spinach & Egg Breakfast Wraps with Tomato",
        "Morning snack": "Kiwi & Pumpkin Seed Snack Pots",
        "Lunch": "Cannellini Bean, Roasted Carrot & Cottage Cheese Barley Salad with Mustard-Herb Dressing",
        "Afternoon snack": "Carrot & Cucumber Batons with Lemon Hummus",
        "Dinner": "Miso-Ginger Mycoprotein, Mushroom & Broccoli Soba Stir-Fry",
        "Evening snack": "Blackberry Skyr Pots with Chia"
    },
    "2026-12-24": {
        "Breakfast": "Orange-Cinnamon Skyr Overnight Oats with Cocoa and Hazelnuts",
        "Morning snack": "Clementine & Pistachio Snack Boxes",
        "Lunch": "Cranberry-Free Festive Tempeh, Roasted Squash & Bulgur Salad with Spinach and Mustard Yoghurt",
        "Afternoon snack": "Rosemary Roasted Broad Beans with Red Pepper",
        "Dinner": "Mushroom, Spinach & Green Lentil Filo Pie with Roasted Brussels Sprouts and Red-Wine Onion Gravy",
        "Evening snack": "Dark Cocoa Quark Pots with Orange Zest and Toasted Walnuts"
    },
    "2026-12-25": {
        "Breakfast": "Festive Mushroom, Spinach & Cottage Cheese Eggs with Seeded Sourdough",
        "Morning snack": "Clementine, Pistachio & Dark Cocoa Skyr Pots",
        "Lunch": "Roasted Beetroot, Puy Lentil & Feta Wholegrain Pitta Pockets with Rocket and Mustard Yoghurt",
        "Afternoon snack": "Cinnamon-Spiced Roasted Chickpeas with Satsuma",
        "Dinner": "Herb-Roasted Seitan with Crispy Potatoes, Brussels Sprouts, Maple-Mustard Carrots, Savoy Cabbage and Mushroom Gravy",
        "Evening snack": "Chocolate-Orange Skyr Pots with Hazelnuts"
    },
    "2026-12-26": {
        "Breakfast": "Savoury Potato, Tempeh & Spinach Breakfast Hash with Cottage Cheese",
        "Morning snack": "Kiwi, Walnut & Greek Yoghurt Pots",
        "Lunch": "Mustard-Herb Seitan, Roasted Vegetable & Barley Salad with Watercress",
        "Afternoon snack": "Oatcakes with Edamame Hummus and Cucumber",
        "Dinner": "Smoky Mycoprotein, Black Bean & Roasted Pepper Enchiladas with Lime Yoghurt",
        "Evening snack": "Cocoa Raspberry Quark Pots with Chia"
    },
    "2026-12-27": {
        "Breakfast": "Tofu Scramble with Mushrooms, Brussels Sprouts and Wholemeal Toast",
        "Morning snack": "Clementine & Almond Skyr Pots",
        "Lunch": "Harissa Butter Bean, Roasted Carrot & Couscous Salad with Mint Yoghurt",
        "Afternoon snack": "Chilli-Lime Roasted Edamame",
        "Dinner": "Leek, Mushroom & Cannellini Bean Cottage Pie with Mycoprotein and Carrot-Swede Mash",
        "Evening snack": "Kiwi Greek Yoghurt Pots with Ground Flaxseed"
    },
    "2026-12-28": {
        "Breakfast": "Frozen Berry, Skyr & Oat Breakfast Pots with Hemp Seeds",
        "Morning snack": "Satsuma & Pistachio Snack Boxes",
        "Lunch": "Miso Tempeh, Edamame & Soba Noodle Salad with Cabbage and Carrot",
        "Afternoon snack": "Red Pepper Batons with Lemon Hummus",
        "Dinner": "Tomato-Braised Tofu, Butter Beans & Cavolo Nero with Wholegrain Couscous",
        "Evening snack": "Cocoa Quark Pots with Raspberries"
    },
    "2026-12-29": {
        "Breakfast": "Spinach, Tomato & Cottage Cheese Egg Muffins with Rye Toast",
        "Morning snack": "Kiwi & Walnut Snack Boxes",
        "Lunch": "Chipotle Black Bean & Mycoprotein Brown Rice Salad with Sweetcorn and Lime Yoghurt",
        "Afternoon snack": "Rosemary Roasted Chickpeas with Cucumber",
        "Dinner": "Jalfrezi Tempeh, Chickpea & Cauliflower Curry with Brown Basmati Rice and Cucumber Raita",
        "Evening snack": "Orange Skyr Pots with Chia"
    },
    "2026-12-30": {
        "Breakfast": "Raspberry-Cocoa Protein Porridge with Skyr and Pumpkin Seeds",
        "Morning snack": "Clementine & Almond Snack Boxes",
        "Lunch": "Basil-Pesto Tofu, Green Bean & Wholewheat Pasta Salad with Spinach",
        "Afternoon snack": "Carrot & Cucumber Batons with Edamame Hummus",
        "Dinner": "Lentil, Mushroom & Mycoprotein Wholewheat Pasta with Rosemary Tomato Sauce",
        "Evening snack": "Blackberry Quark Pots with Ground Flaxseed"
    },
    "2026-12-31": {
        "Breakfast": "Blackberry, Skyr & Jumbo Oat Overnight Pots with Chia and Pistachios",
        "Morning snack": "Kiwi & Walnut Snack Pots",
        "Lunch": "Chimichurri Tempeh, Roasted Beetroot & Bulgur Salad with Watercress",
        "Afternoon snack": "Smoked Paprika Roasted Broad Beans with Clementine",
        "Dinner": "Gochujang Tofu & Edamame Rice Bowls with Sesame Broccoli, Mushrooms and Vegetarian Kimchi",
        "Evening snack": "Dark Cocoa, Orange & Skyr Pots with Cacao Nibs"
    }
}


def canonical_filename(title):
    text = unicodedata.normalize(
        "NFKD",
        title
    )

    text = (
        text
        .replace(
            "’",
            "'"
        )
        .replace(
            "&",
            " "
        )
        .lower()
    )

    text = re.sub(
        r"['’]",
        "",
        text
    )

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    words = [
        word
        for word in text.split()
        if word not in {
            "and",
            "with"
        }
    ]

    return (
        "_".join(
            words
        )
        +
        ".html"
    )


def main():
    schedule = []

    for date_value in sorted(
        PLAN
    ):
        for meal_type in MEAL_ORDER:
            title = (
                PLAN[
                    date_value
                ][
                    meal_type
                ]
            )

            schedule.append(
                {
                    "date":
                        date_value,

                    "meal_type":
                        meal_type,

                    "title":
                        title,

                    "file":
                        canonical_filename(
                            title
                        ),
                }
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
        f"Created: {OUTPUT_FILE.resolve()}"
    )

    print(
        f"Scheduled meals: {len(schedule)}"
    )


if __name__ == "__main__":
    main()
