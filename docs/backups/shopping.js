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

const generateShoppingList =
    document.getElementById(
        "generateShoppingList"
    );

const copyShoppingList =
    document.getElementById(
        "copyShoppingList"
    );

const shoppingResults =
    document.getElementById(
        "shoppingResults"
    );


function shoppingDateDisplay(
    isoDate
) {

    const [
        year,
        month,
        day
    ] = isoDate.split("-");

    return (
        `${day}/${month}/${year}`
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
            `${whole}${fractions[remainder]}`
        );
    }

    if (whole > 0) {
        return String(whole);
    }

    return fractions[remainder];
}


function normaliseQuantity(
    quantity,
    unit
) {

    const amount =
        Number(quantity);

    if (
        !Number.isFinite(amount)
    ) {

        return {
            group: unit,
            value: quantity,
            originalUnit: unit
        };
    }

    if (
        unit === "kg"
    ) {
        return {
            group: "mass",
            value: amount * 1000,
            originalUnit: unit
        };
    }

    if (
        unit === "g"
    ) {
        return {
            group: "mass",
            value: amount,
            originalUnit: unit
        };
    }

    if (
        unit === "L"
    ) {
        return {
            group: "volume",
            value: amount * 1000,
            originalUnit: unit
        };
    }

    if (
        unit === "ml"
    ) {
        return {
            group: "volume",
            value: amount,
            originalUnit: unit
        };
    }

    if (
        unit === "tbsp"
    ) {
        return {
            group: "spoon",
            value: amount * 3,
            originalUnit: unit
        };
    }

    if (
        unit === "tsp"
    ) {
        return {
            group: "spoon",
            value: amount,
            originalUnit: unit
        };
    }

    if (
        unit === "integer"
    ) {
        return {
            group: "count",
            value: amount,
            originalUnit: unit
        };
    }

    return {
        group: unit,
        value: amount,
        originalUnit: unit
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

            const tbsp =
                value / 3;

            return (
                `${fractionText(tbsp)} tbsp`
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
            fractionText(value)
        );
    }

    return (
        `${Math.round(value * 100) / 100} ${group}`
    );
}


async function loadShoppingData() {

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
        new Date();

    const year =
        today.getFullYear();

    const month =
        String(
            today.getMonth() + 1
        ).padStart(
            2,
            "0"
        );

    const day =
        String(
            today.getDate()
        ).padStart(
            2,
            "0"
        );

    const todayISO =
        `${year}-${month}-${day}`;

    shoppingFrom.value =
        todayISO;

    shoppingTo.value =
        todayISO;
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

    copyShoppingList.hidden =
        true;

    if (
        !from
        ||
        !to
        ||
        from > to
    ) {

        shoppingMealSelection.textContent =
            "Choose a valid date range.";

        generateShoppingList.hidden =
            true;

        return;
    }


    const matches =
        shoppingSchedule.filter(
            item =>
                item.date >= from
                &&
                item.date <= to
        );


    if (!matches.length) {

        shoppingMealSelection.textContent =
            "No scheduled meals in this range.";

        generateShoppingList.hidden =
            true;

        return;
    }


    const byDate = {};

    for (
        const item
        of matches
    ) {

        if (!byDate[item.date]) {
            byDate[item.date] = [];
        }

        byDate[item.date].push(
            item
        );
    }


    for (
        const date
        of Object.keys(byDate).sort()
    ) {

        const dayCard =
            document.createElement(
                "section"
            );

        dayCard.className =
            "shopping-day";


        const heading =
            document.createElement(
                "h3"
            );

        heading.textContent =
            shoppingDateDisplay(
                date
            );

        dayCard.appendChild(
            heading
        );


        for (
            const item
            of byDate[date]
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

            text.textContent =
                (
                    `${item.meal_type}: `
                    +
                    item.title
                    +
                    (
                        recipeExists
                            ? ""
                            : " — recipe not generated"
                    )
                );


            label.appendChild(
                checkbox
            );

            label.appendChild(
                text
            );

            dayCard.appendChild(
                label
            );
        }


        shoppingMealSelection.appendChild(
            dayCard
        );
    }


    generateShoppingList.hidden =
        false;
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

            const id =
                item.ingredient_id
                ||
                item.display_name;


            if (!ingredients[id]) {

                ingredients[id] = {
                    displayName:
                        item.display_name,
                    category:
                        item.category,
                    groups: {}
                };
            }


            const normal =
                normaliseQuantity(
                    item.quantity_used,
                    item.unit_used
                );


            if (
                !ingredients[id]
                    .groups[
                        normal.group
                    ]
            ) {

                ingredients[id]
                    .groups[
                        normal.group
                    ] = 0;
            }


            ingredients[id]
                .groups[
                    normal.group
                ] +=
                    Number(
                        normal.value
                    );
        }
    }


    const sorted =
        Object.values(
            ingredients
        ).sort(
            (a, b) => {

                const categoryCompare =
                    (
                        a.category
                        ||
                        ""
                    )
                    .localeCompare(
                        b.category
                        ||
                        ""
                    );

                if (categoryCompare) {
                    return categoryCompare;
                }

                return (
                    a.displayName
                    .localeCompare(
                        b.displayName
                    )
                );
            }
        );


    shoppingResults.innerHTML =
        "";


    const textLines = [];

    let currentCategory =
        null;


    for (
        const item
        of sorted
    ) {

        const category =
            item.category
            ||
            "Other";


        if (
            category !== currentCategory
        ) {

            currentCategory =
                category;


            const heading =
                document.createElement(
                    "h3"
                );

            heading.textContent =
                category;

            shoppingResults.appendChild(
                heading
            );


            textLines.push(
                ""
            );

            textLines.push(
                category.toUpperCase()
            );
        }


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

        row.innerHTML =
            (
                `<strong>${item.displayName}</strong>`
                +
                `<span>${quantities}</span>`
            );


        shoppingResults.appendChild(
            row
        );


        textLines.push(
            (
                `${item.displayName}`
                +
                ` — `
                +
                quantities
            )
        );
    }


    if (!sorted.length) {

        shoppingResults.textContent =
            "No meals selected.";

        copyShoppingList.hidden =
            true;

        lastShoppingText =
            "";

        return;
    }


    lastShoppingText =
        textLines
            .join("\n")
            .trim();


    copyShoppingList.hidden =
        false;
}


loadShoppingMeals.addEventListener(
    "click",
    renderShoppingMealChoices
);


generateShoppingList.addEventListener(
    "click",
    generateList
);


copyShoppingList.addEventListener(
    "click",
    async () => {

        if (!lastShoppingText) {
            return;
        }

        await navigator.clipboard.writeText(
            lastShoppingText
        );

        copyShoppingList.textContent =
            "Copied";

        setTimeout(
            () => {

                copyShoppingList.textContent =
                    "Copy shopping list";

            },
            1200
        );
    }
);


loadShoppingData();