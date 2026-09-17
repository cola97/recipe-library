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
