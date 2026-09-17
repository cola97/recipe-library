let shoppingSchedule = [];
let shoppingRecipes = {};
let lastShoppingText = "";


const shoppingFrom =
    document.getElementById(
        "shoppingFrom"
    );

const shoppingTo =
    document.getElementById(
        "shoppingTo"
    );

const loadShoppingMeals =
    document.getElementById(
        "loadShoppingMeals"
    );

const shoppingMealSelection =
    document.getElementById(
        "shoppingMealSelection"
    );

const shoppingGenerateBar =
    document.getElementById(
        "shoppingGenerateBar"
    );

const shoppingSelectedCount =
    document.getElementById(
        "shoppingSelectedCount"
    );

const generateShoppingList =
    document.getElementById(
        "generateShoppingList"
    );

const shoppingResultSection =
    document.getElementById(
        "shoppingResultSection"
    );

const shoppingResults =
    document.getElementById(
        "shoppingResults"
    );

const copyShoppingListTop =
    document.getElementById(
        "copyShoppingListTop"
    );

const copyShoppingListBottom =
    document.getElementById(
        "copyShoppingListBottom"
    );


const mealOrder = [
    "Breakfast",
    "Morning snack",
    "Lunch",
    "Afternoon snack",
    "Dinner",
    "Evening snack"
];


const shoppingSectionOrder = [
    "Fruit & vegetables",
    "Fresh herbs & aromatics",
    "Chilled, dairy & eggs",
    "Plant proteins & legumes",
    "Bread & bakery",
    "Grains, pasta & cereals",
    "Condiments & cooking",
    "Spices & seasonings",
    "Nuts & seeds",
    "Oils",
    "Baking",
    "Other"
];


function shoppingDateDisplay(
    isoDate
) {

    const [
        year,
        month,
        day
    ] =
        isoDate.split("-");


    const date =
        new Date(
            Number(year),
            Number(month) - 1,
            Number(day)
        );


    return (
        date.toLocaleDateString(
            "en-GB",
            {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            }
        )
    );
}


function localTodayISO() {

    const now =
        new Date();

    const year =
        now.getFullYear();

    const month =
        String(
            now.getMonth() + 1
        ).padStart(
            2,
            "0"
        );

    const day =
        String(
            now.getDate()
        ).padStart(
            2,
            "0"
        );

    return (
        `${year}-${month}-${day}`
    );
}


function fractionText(
    value
) {

    const rounded =
        Math.round(
            value * 8
        ) / 8;

    const whole =
        Math.floor(
            rounded
        );

    const remainder =
        Math.round(
            (
                rounded
                -
                whole
            )
            *
            8
        );

    const fractions = {
        0: "",
        1: "⅛",
        2: "¼",
        3: "⅜",
        4: "½",
        5: "⅝",
        6: "¾",
        7: "⅞"
    };


    if (
        whole === 0
        &&
        remainder === 0
    ) {
        return "0";
    }


    if (
        whole > 0
        &&
        remainder > 0
    ) {

        return (
            `${whole}`
            +
            fractions[
                remainder
            ]
        );
    }


    if (
        whole > 0
    ) {

        return String(
            whole
        );
    }


    return fractions[
        remainder
    ];
}


function normaliseQuantity(
    quantity,
    unit
) {

    const amount =
        Number(
            quantity
        );


    if (
        !Number.isFinite(
            amount
        )
    ) {

        return {
            group:
                unit || "other",
            value:
                quantity
        };
    }


    if (
        unit === "kg"
    ) {

        return {
            group:
                "mass",
            value:
                amount * 1000
        };
    }


    if (
        unit === "g"
    ) {

        return {
            group:
                "mass",
            value:
                amount
        };
    }


    if (
        unit === "L"
    ) {

        return {
            group:
                "volume",
            value:
                amount * 1000
        };
    }


    if (
        unit === "ml"
    ) {

        return {
            group:
                "volume",
            value:
                amount
        };
    }


    if (
        unit === "tbsp"
    ) {

        return {
            group:
                "spoon",
            value:
                amount * 3
        };
    }


    if (
        unit === "tsp"
    ) {

        return {
            group:
                "spoon",
            value:
                amount
        };
    }


    if (
        unit === "integer"
    ) {

        return {
            group:
                "count",
            value:
                amount
        };
    }


    return {
        group:
            unit || "other",
        value:
            amount
    };
}


function formatNormalisedQuantity(
    group,
    value
) {

    if (
        group === "mass"
    ) {

        if (
            value >= 1000
            &&
            value % 1000 === 0
        ) {

            return (
                `${value / 1000} kg`
            );
        }


        return (
            `${Math.round(value * 10) / 10} g`
        );
    }


    if (
        group === "volume"
    ) {

        if (
            value >= 1000
            &&
            value % 1000 === 0
        ) {

            return (
                `${value / 1000} L`
            );
        }


        return (
            `${Math.round(value * 10) / 10} ml`
        );
    }


    if (
        group === "spoon"
    ) {

        if (
            value >= 3
        ) {

            return (
                `${fractionText(value / 3)} tbsp`
            );
        }


        return (
            `${fractionText(value)} tsp`
        );
    }


    if (
        group === "count"
    ) {

        return (
            fractionText(
                value
            )
        );
    }


    return (
        `${Math.round(value * 100) / 100}`
        +
        (
            group
                ? ` ${group}`
                : ""
        )
    );
}


function broadShoppingSection(
    category
) {

    const value =
        (
            category
            ||
            ""
        )
            .toLocaleLowerCase();


    if (
        [
            "fruit",
            "vegetables",
            "leafy vegetables"
        ].includes(
            value
        )
    ) {
        return "Fruit & vegetables";
    }


    if (
        [
            "fresh herbs",
            "aromatics"
        ].includes(
            value
        )
    ) {
        return "Fresh herbs & aromatics";
    }


    if (
        [
            "dairy",
            "eggs"
        ].includes(
            value
        )
    ) {
        return "Chilled, dairy & eggs";
    }


    if (
        [
            "plant protein",
            "legumes"
        ].includes(
            value
        )
    ) {
        return "Plant proteins & legumes";
    }


    if (
        value === "bread"
    ) {
        return "Bread & bakery";
    }


    if (
        [
            "grains",
            "cereals",
            "pasta and grains"
        ].includes(
            value
        )
    ) {
        return "Grains, pasta & cereals";
    }


    if (
        [
            "condiments",
            "flavourings",
            "sweeteners",
            "thickeners"
        ].includes(
            value
        )
    ) {
        return "Condiments & cooking";
    }


    if (
        [
            "spices",
            "seasoning"
        ].includes(
            value
        )
    ) {
        return "Spices & seasonings";
    }


    if (
        [
            "nuts",
            "seeds"
        ].includes(
            value
        )
    ) {
        return "Nuts & seeds";
    }


    if (
        value === "oils"
    ) {
        return "Oils";
    }


    if (
        value === "baking ingredients"
    ) {
        return "Baking";
    }


    return "Other";
}


function isShoppingIngredient(
    item
) {

    const id =
        (
            item.ingredient_id
            ||
            ""
        )
            .toLocaleLowerCase();

    const name =
        (
            item.display_name
            ||
            ""
        )
            .toLocaleLowerCase();


    if (
        id === "water"
        ||
        name === "water"
        ||
        name === "cold water"
    ) {
        return false;
    }


    return true;
}


function updateSelectedCount() {

    const available =
        Array.from(
            document.querySelectorAll(
                ".shopping-meal-checkbox:not(:disabled)"
            )
        );

    const checked =
        available.filter(
            checkbox =>
                checkbox.checked
        );


    shoppingSelectedCount.textContent =
        (
            `${checked.length} of `
            +
            `${available.length} meals selected`
        );
}


function showDatePicker(
    input
) {

    input.focus();


    if (
        typeof input.showPicker
        ===
        "function"
    ) {

        try {
            input.showPicker();
        } catch (
            error
        ) {
            // Normal date-input behaviour remains available.
        }
    }
}


async function loadShoppingData() {

    try {

        const [
            scheduleResponse,
            recipeResponse
        ] =
            await Promise.all([

                fetch(
                    "./schedule.json",
                    {
                        cache:
                            "no-store"
                    }
                ),

                fetch(
                    "./shopping_data.json",
                    {
                        cache:
                            "no-store"
                    }
                )

            ]);


        shoppingSchedule =
            await scheduleResponse.json();

        shoppingRecipes =
            await recipeResponse.json();


        const today =
            localTodayISO();

        const scheduledDates =
            [
                ...new Set(
                    shoppingSchedule.map(
                        item =>
                            item.date
                    )
                )
            ]
                .sort();


        const initialDate =
            shoppingSchedule.some(
                item =>
                    item.date === today
            )
                ? today
                : (
                    scheduledDates[0]
                    ||
                    today
                );


        shoppingFrom.value =
            initialDate;

        shoppingTo.value =
            initialDate;

    } catch (
        error
    ) {

        console.error(
            error
        );

        shoppingMealSelection.textContent =
            "Shopping data could not be loaded.";
    }
}


function renderShoppingMealChoices() {

    const from =
        shoppingFrom.value;

    const to =
        shoppingTo.value;


    shoppingMealSelection.innerHTML =
        "";

    shoppingResults.innerHTML =
        "";

    shoppingResultSection.hidden =
        true;

    shoppingGenerateBar.hidden =
        true;

    lastShoppingText =
        "";


    if (
        !from
        ||
        !to
        ||
        from > to
    ) {

        shoppingMealSelection.textContent =
            "Choose a valid date range.";

        return;
    }


    const matches =
        shoppingSchedule

            .filter(
                item =>
                    item.date >= from
                    &&
                    item.date <= to
            )

            .sort(
                (a, b) => {

                    const dateCompare =
                        a.date.localeCompare(
                            b.date
                        );

                    if (
                        dateCompare
                    ) {
                        return dateCompare;
                    }


                    return (
                        mealOrder.indexOf(
                            a.meal_type
                        )
                        -
                        mealOrder.indexOf(
                            b.meal_type
                        )
                    );
                }
            );


    if (!matches.length) {

        shoppingMealSelection.textContent =
            "No scheduled meals in this range.";

        return;
    }


    const byDate = {};


    for (
        const item
        of matches
    ) {

        if (
            !byDate[
                item.date
            ]
        ) {

            byDate[
                item.date
            ] = [];
        }


        byDate[
            item.date
        ].push(
            item
        );
    }


    for (
        const date
        of Object.keys(
            byDate
        ).sort()
    ) {

        const dayCard =
            document.createElement(
                "section"
            );

        dayCard.className =
            "shopping-day";


        const header =
            document.createElement(
                "div"
            );

        header.className =
            "shopping-day-header";


        const heading =
            document.createElement(
                "h3"
            );

        heading.textContent =
            shoppingDateDisplay(
                date
            );


        const actions =
            document.createElement(
                "div"
            );

        actions.className =
            "shopping-day-actions";


        const allButton =
            document.createElement(
                "button"
            );

        allButton.type =
            "button";

        allButton.textContent =
            "All";


        const noneButton =
            document.createElement(
                "button"
            );

        noneButton.type =
            "button";

        noneButton.textContent =
            "None";


        actions.appendChild(
            allButton
        );

        actions.appendChild(
            noneButton
        );


        header.appendChild(
            heading
        );

        header.appendChild(
            actions
        );


        dayCard.appendChild(
            header
        );


        const list =
            document.createElement(
                "div"
            );

        list.className =
            "shopping-meal-list";


        for (
            const item
            of byDate[
                date
            ]
        ) {

            const label =
                document.createElement(
                    "label"
                );

            label.className =
                "shopping-meal-row";


            const checkbox =
                document.createElement(
                    "input"
                );

            checkbox.type =
                "checkbox";

            checkbox.className =
                "shopping-meal-checkbox";

            checkbox.dataset.file =
                item.file;

            checkbox.dataset.date =
                item.date;

            checkbox.dataset.meal =
                item.meal_type;


            const recipeExists =
                Boolean(
                    shoppingRecipes[
                        item.file
                    ]
                );


            checkbox.checked =
                recipeExists;

            checkbox.disabled =
                !recipeExists;


            const text =
                document.createElement(
                    "span"
                );


            const mealType =
                document.createElement(
                    "span"
                );

            mealType.className =
                "shopping-meal-type";

            mealType.textContent =
                item.meal_type;


            const title =
                document.createElement(
                    "span"
                );

            title.className =
                "shopping-meal-title";

            title.textContent =
                item.title;


            text.appendChild(
                mealType
            );

            text.appendChild(
                title
            );


            if (
                !recipeExists
            ) {

                const unavailable =
                    document.createElement(
                        "span"
                    );

                unavailable.className =
                    "shopping-unavailable";

                unavailable.textContent =
                    "Recipe not generated";

                text.appendChild(
                    unavailable
                );
            }


            label.appendChild(
                checkbox
            );

            label.appendChild(
                text
            );

            list.appendChild(
                label
            );


            checkbox.addEventListener(
                "change",
                updateSelectedCount
            );
        }


        dayCard.appendChild(
            list
        );


        allButton.addEventListener(
            "click",
            () => {

                for (
                    const checkbox
                    of dayCard.querySelectorAll(
                        ".shopping-meal-checkbox:not(:disabled)"
                    )
                ) {

                    checkbox.checked =
                        true;
                }


                updateSelectedCount();
            }
        );


        noneButton.addEventListener(
            "click",
            () => {

                for (
                    const checkbox
                    of dayCard.querySelectorAll(
                        ".shopping-meal-checkbox:not(:disabled)"
                    )
                ) {

                    checkbox.checked =
                        false;
                }


                updateSelectedCount();
            }
        );


        shoppingMealSelection.appendChild(
            dayCard
        );
    }


    shoppingGenerateBar.hidden =
        false;

    updateSelectedCount();
}


function generateList() {

    const checked =
        Array.from(
            document.querySelectorAll(
                ".shopping-meal-checkbox:checked"
            )
        );


    const ingredients = {};


    for (
        const checkbox
        of checked
    ) {

        const recipe =
            shoppingRecipes[
                checkbox.dataset.file
            ];


        if (!recipe) {
            continue;
        }


        for (
            const item
            of recipe.ingredients
        ) {

            if (
                !isShoppingIngredient(
                    item
                )
            ) {
                continue;
            }


            const id =
                (
                    item.ingredient_id
                    ||
                    item.display_name
                );


            if (
                !ingredients[
                    id
                ]
            ) {

                ingredients[
                    id
                ] = {
                    displayName:
                        item.display_name,

                    category:
                        item.category,

                    groups:
                        {}
                };
            }


            const normal =
                normaliseQuantity(
                    item.quantity_used,
                    item.unit_used
                );


            if (
                ingredients[
                    id
                ]
                    .groups[
                        normal.group
                    ]
                ===
                undefined
            ) {

                ingredients[
                    id
                ]
                    .groups[
                        normal.group
                    ] =
                        0;
            }


            ingredients[
                id
            ]
                .groups[
                    normal.group
                ] +=
                    Number(
                        normal.value
                    );
        }
    }


    const allIngredients =
        Object.values(
            ingredients
        );


    if (
        !allIngredients.length
    ) {

        shoppingResults.textContent =
            "No meals selected.";

        shoppingResultSection.hidden =
            false;

        lastShoppingText =
            "";

        return;
    }


    const grouped = {};


    for (
        const item
        of allIngredients
    ) {

        const section =
            broadShoppingSection(
                item.category
            );


        if (
            !grouped[
                section
            ]
        ) {

            grouped[
                section
            ] = [];
        }


        grouped[
            section
        ].push(
            item
        );
    }


    shoppingResults.innerHTML =
        "";


    const textLines =
        [];


    for (
        const section
        of shoppingSectionOrder
    ) {

        const items =
            grouped[
                section
            ];


        if (
            !items
            ||
            !items.length
        ) {
            continue;
        }


        items.sort(
            (a, b) =>
                a.displayName.localeCompare(
                    b.displayName
                )
        );


        const card =
            document.createElement(
                "section"
            );

        card.className =
            "shopping-category-card";


        const heading =
            document.createElement(
                "h3"
            );

        heading.className =
            "shopping-category-heading";

        heading.textContent =
            section;

        card.appendChild(
            heading
        );


        const list =
            document.createElement(
                "div"
            );

        list.className =
            "shopping-category-items";


        textLines.push(
            section.toUpperCase()
        );


        for (
            const item
            of items
        ) {

            const quantities =
                Object.entries(
                    item.groups
                )
                    .map(
                        ([group, value]) =>
                            formatNormalisedQuantity(
                                group,
                                value
                            )
                    )
                    .join(
                        " + "
                    );


            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "shopping-result-row";


            const name =
                document.createElement(
                    "div"
                );

            name.className =
                "shopping-result-name";

            name.textContent =
                item.displayName;


            const quantity =
                document.createElement(
                    "div"
                );

            quantity.className =
                "shopping-result-quantity";

            quantity.textContent =
                quantities;


            row.appendChild(
                name
            );

            row.appendChild(
                quantity
            );


            list.appendChild(
                row
            );


            textLines.push(
                (
                    `${item.displayName}`
                    +
                    " — "
                    +
                    quantities
                )
            );
        }


        textLines.push(
            ""
        );


        card.appendChild(
            list
        );

        shoppingResults.appendChild(
            card
        );
    }


    lastShoppingText =
        textLines
            .join(
                "\n"
            )
            .trim();


    shoppingResultSection.hidden =
        false;


    shoppingResultSection.scrollIntoView({
        behavior:
            "smooth",

        block:
            "start"
    });
}


async function copyShoppingList(
    button
) {

    if (
        !lastShoppingText
    ) {
        return;
    }


    await navigator.clipboard.writeText(
        lastShoppingText
    );


    const original =
        button.textContent;

    button.textContent =
        "Copied";


    setTimeout(
        () => {

            button.textContent =
                original;

        },
        1200
    );
}


for (
    const shell
    of document.querySelectorAll(
        ".date-input-shell"
    )
) {

    const input =
        document.getElementById(
            shell.dataset.dateTarget
        );


    shell.addEventListener(
        "click",
        event => {

            if (
                event.target
                !==
                input
            ) {

                showDatePicker(
                    input
                );
            }
        }
    );


    input.addEventListener(
        "click",
        () => {

            showDatePicker(
                input
            );
        }
    );
}


loadShoppingMeals.addEventListener(
    "click",
    renderShoppingMealChoices
);


generateShoppingList.addEventListener(
    "click",
    generateList
);


copyShoppingListTop.addEventListener(
    "click",
    () => {

        copyShoppingList(
            copyShoppingListTop
        );
    }
);


copyShoppingListBottom.addEventListener(
    "click",
    () => {

        copyShoppingList(
            copyShoppingListBottom
        );
    }
);


loadShoppingData();
