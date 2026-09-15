let recipes = [];
let schedule = [];
let filteredRecipes = [];


const dateSelect =
    document.getElementById(
        "dateSelect"
    );

const mealSelect =
    document.getElementById(
        "mealSelect"
    );

const scheduledRecipes =
    document.getElementById(
        "scheduledRecipes"
    );

const recipeSearch =
    document.getElementById(
        "recipeSearch"
    );

const allRecipes =
    document.getElementById(
        "allRecipes"
    );

const openLibraryRecipe =
    document.getElementById(
        "openLibraryRecipe"
    );

const recipeFrame =
    document.getElementById(
        "recipeFrame"
    );

const viewerPlaceholder =
    document.getElementById(
        "viewerPlaceholder"
    );

const currentContext =
    document.getElementById(
        "currentContext"
    );


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


function displayDate(
    isoDate
) {

    if (!isoDate) {
        return "";
    }

    const [
        year,
        month,
        day
    ] = isoDate.split("-");

    return (
        `${day}/${month}/${year}`
    );
}


function getRecipe(
    filename
) {

    return recipes.find(
        recipe =>
            recipe.filename === filename
    );
}


function clearViewer(
    message
) {

    recipeFrame.hidden =
        true;

    recipeFrame.removeAttribute(
        "src"
    );

    viewerPlaceholder.hidden =
        false;

    viewerPlaceholder.textContent =
        message;
}


function openRecipe(
    filename,
    contextText = ""
) {

    const recipe =
        getRecipe(
            filename
        );

    /*
       Only HTML recipes that actually exist in
       recipes.json may be opened.
    */

    if (!recipe) {

        clearViewer(
            "Recipe not generated yet."
        );

        return;
    }

    recipeFrame.src =
        `./recipes/${encodeURIComponent(filename)}`;

    recipeFrame.hidden =
        false;

    viewerPlaceholder.hidden =
        true;

    if (contextText) {

        currentContext.textContent =
            contextText;

    } else {

        currentContext.textContent =
            recipe.title;
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function getMealsForDate(
    date
) {

    const mealOrder = [
        "Breakfast",
        "Morning snack",
        "Lunch",
        "Afternoon snack",
        "Dinner",
        "Evening snack"
    ];

    const present =
        new Set(

            schedule

                .filter(
                    item =>
                        item.date === date
                )

                .map(
                    item =>
                        item.meal_type
                )
        );

    /*
       Standard meal types are shown in their normal
       order. Any future/custom meal types are appended
       alphabetically afterwards.
    */

    const standard =
        mealOrder.filter(
            meal =>
                present.has(meal)
        );

    const custom =
        [...present]

            .filter(
                meal =>
                    !mealOrder.includes(
                        meal
                    )
            )

            .sort(
                (a, b) =>
                    a.localeCompare(b)
            );

    return [
        ...standard,
        ...custom
    ];
}


function updateMealSelector() {

    const date =
        dateSelect.value;

    const existingMeal =
        mealSelect.value;

    const meals =
        getMealsForDate(
            date
        );

    mealSelect.innerHTML =
        "";

    if (
        meals.length === 0
    ) {

        const option =
            document.createElement(
                "option"
            );

        option.value =
            "";

        option.textContent =
            "No scheduled meals";

        mealSelect.appendChild(
            option
        );

        updateScheduledRecipes();

        return;
    }

    for (
        const meal
        of meals
    ) {

        const option =
            document.createElement(
                "option"
            );

        option.value =
            meal;

        option.textContent =
            meal;

        mealSelect.appendChild(
            option
        );
    }

    if (
        meals.includes(
            existingMeal
        )
    ) {

        mealSelect.value =
            existingMeal;

    } else if (
        meals.includes(
            "Breakfast"
        )
    ) {

        mealSelect.value =
            "Breakfast";

    } else {

        mealSelect.value =
            meals[0];
    }

    updateScheduledRecipes();
}


function createStatusBadge(
    available
) {

    const badge =
        document.createElement(
            "span"
        );

    badge.className =
        available
            ? "status-badge status-available"
            : "status-badge status-missing";

    badge.textContent =
        available
            ? "Available"
            : "Not generated yet";

    return badge;
}


function updateScheduledRecipes() {

    const date =
        dateSelect.value;

    const meal =
        mealSelect.value;

    scheduledRecipes.innerHTML =
        "";

    if (
        !date ||
        !meal
    ) {

        const message =
            document.createElement(
                "div"
            );

        message.className =
            "empty-schedule-message";

        message.textContent =
            "No scheduled recipe.";

        scheduledRecipes.appendChild(
            message
        );

        clearViewer(
            "Choose a scheduled meal or select a recipe from the library."
        );

        return;
    }

    const matches =
        schedule.filter(
            item =>
                item.date === date &&
                item.meal_type === meal
        );

    currentContext.textContent =
        `${displayDate(date)} — ${meal}`;

    if (
        matches.length === 0
    ) {

        const message =
            document.createElement(
                "div"
            );

        message.className =
            "empty-schedule-message";

        message.textContent =
            "No recipe is scheduled for this meal.";

        scheduledRecipes.appendChild(
            message
        );

        clearViewer(
            "No recipe is scheduled for this meal."
        );

        return;
    }

    for (
        const item
        of matches
    ) {

        const card =
            document.createElement(
                "article"
            );

        card.className =
            item.available
                ? "scheduled-card scheduled-available"
                : "scheduled-card scheduled-missing";

        const header =
            document.createElement(
                "div"
            );

        header.className =
            "scheduled-card-header";

        const title =
            document.createElement(
                "div"
            );

        title.className =
            "scheduled-title";

        title.textContent =
            item.title;

        header.appendChild(
            title
        );

        header.appendChild(
            createStatusBadge(
                item.available
            )
        );

        card.appendChild(
            header
        );

        const filename =
            document.createElement(
                "div"
            );

        filename.className =
            "scheduled-filename";

        filename.textContent =
            item.file;

        card.appendChild(
            filename
        );

        if (
            item.available
        ) {

            const button =
                document.createElement(
                    "button"
                );

            button.type =
                "button";

            button.className =
                "scheduled-open-button";

            button.textContent =
                "Open recipe";

            button.addEventListener(
                "click",
                () => {

                    openRecipe(
                        item.file,
                        (
                            `${displayDate(item.date)}`
                            +
                            ` — ${item.meal_type}`
                            +
                            ` — ${item.title}`
                        )
                    );
                }
            );

            card.appendChild(
                button
            );

        } else {

            const unavailableMessage =
                document.createElement(
                    "div"
                );

            unavailableMessage.className =
                "not-generated-message";

            unavailableMessage.textContent =
                (
                    "This meal is in the plan, "
                    +
                    "but its HTML recipe has not been generated yet."
                );

            card.appendChild(
                unavailableMessage
            );
        }

        scheduledRecipes.appendChild(
            card
        );
    }

    /*
       Automatically open the recipe only when
       the selected date + meal resolves to exactly
       one available recipe.
    */

    if (
        matches.length === 1 &&
        matches[0].available
    ) {

        const item =
            matches[0];

        openRecipe(
            item.file,
            (
                `${displayDate(item.date)}`
                +
                ` — ${item.meal_type}`
                +
                ` — ${item.title}`
            )
        );

    } else if (
        matches.length === 1 &&
        !matches[0].available
    ) {

        clearViewer(
            "Recipe not generated yet."
        );
    }
}


function populateRecipeLibrary(
    searchText = ""
) {

    const query =
        searchText
            .trim()
            .toLocaleLowerCase();

    filteredRecipes =
        recipes.filter(
            recipe => {

                const searchable = [

                    recipe.title,

                    recipe.filename,

                    ...(
                        recipe.meal_types
                        ||
                        []
                    )

                ]
                    .join(" ")
                    .toLocaleLowerCase();

                return (
                    searchable.includes(
                        query
                    )
                );
            }
        );

    allRecipes.innerHTML =
        "";

    for (
        const recipe
        of filteredRecipes
    ) {

        const option =
            document.createElement(
                "option"
            );

        option.value =
            recipe.filename;

        const typeText =
            recipe.meal_types?.length

                ? (
                    ` — ${
                        recipe.meal_types.join(
                            ", "
                        )
                    }`
                )

                : "";

        option.textContent =
            (
                recipe.title
                +
                typeText
            );

        allRecipes.appendChild(
            option
        );
    }
}


async function loadData() {

    try {

        const [
            recipeResponse,
            scheduleResponse
        ] =
            await Promise.all([

                fetch(
                    "./recipes.json",
                    {
                        cache:
                            "no-store"
                    }
                ),

                fetch(
                    "./schedule.json",
                    {
                        cache:
                            "no-store"
                    }
                )

            ]);

        if (
            !recipeResponse.ok
        ) {

            throw new Error(
                "Could not load recipes.json"
            );
        }

        if (
            !scheduleResponse.ok
        ) {

            throw new Error(
                "Could not load schedule.json"
            );
        }

        recipes =
            await recipeResponse.json();

        schedule =
            await scheduleResponse.json();

        populateRecipeLibrary();

        const today =
            localTodayISO();

        const scheduledDates = [

            ...new Set(
                schedule.map(
                    item =>
                        item.date
                )
            )

        ].sort();

        if (
            schedule.some(
                item =>
                    item.date === today
            )
        ) {

            dateSelect.value =
                today;

        } else if (
            scheduledDates.length
        ) {

            dateSelect.value =
                scheduledDates[0];

        } else {

            dateSelect.value =
                today;
        }

        updateMealSelector();

    } catch (
        error
    ) {

        console.error(
            error
        );

        currentContext.textContent =
            "The recipe library could not be loaded.";

        scheduledRecipes.textContent =
            error.message;

        clearViewer(
            "The recipe library could not be loaded."
        );
    }
}


dateSelect.addEventListener(
    "change",
    updateMealSelector
);


mealSelect.addEventListener(
    "change",
    updateScheduledRecipes
);


recipeSearch.addEventListener(
    "input",
    () => {

        populateRecipeLibrary(
            recipeSearch.value
        );
    }
);


openLibraryRecipe.addEventListener(
    "click",
    () => {

        const filename =
            allRecipes.value;

        if (!filename) {
            return;
        }

        openRecipe(
            filename
        );
    }
);


allRecipes.addEventListener(
    "dblclick",
    () => {

        const filename =
            allRecipes.value;

        if (!filename) {
            return;
        }

        openRecipe(
            filename
        );
    }
);


loadData();