let recipes = [];
let schedule = [];
let currentScreen = "meals";
let screenBeforeRecipe = "meals";


const appShell =
    document.getElementById(
        "appShell"
    );

const navButtons =
    Array.from(
        document.querySelectorAll(
            ".nav-button"
        )
    );

const screenPanels =
    Array.from(
        document.querySelectorAll(
            "[data-screen-panel]"
        )
    );


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

const ratingFilter =
    document.getElementById(
        "ratingFilter"
    );

const mealTypeFilter =
    document.getElementById(
        "mealTypeFilter"
    );

const proteinSourceFilter =
    document.getElementById(
        "proteinSourceFilter"
    );

const activeTimeFilter =
    document.getElementById(
        "activeTimeFilter"
    );

const totalTimeFilter =
    document.getElementById(
        "totalTimeFilter"
    );

const minimumProteinFilter =
    document.getElementById(
        "minimumProteinFilter"
    );

const cuisineFilter =
    document.getElementById(
        "cuisineFilter"
    );

const difficultyFilter =
    document.getElementById(
        "difficultyFilter"
    );

const recipeSort =
    document.getElementById(
        "recipeSort"
    );

const clearRecipeFilters =
    document.getElementById(
        "clearRecipeFilters"
    );

const recipeResultCount =
    document.getElementById(
        "recipeResultCount"
    );

const recipeCards =
    document.getElementById(
        "recipeCards"
    );


const viewerPanel =
    document.getElementById(
        "viewerPanel"
    );

const recipeFrame =
    document.getElementById(
        "recipeFrame"
    );

const backToPlanner =
    document.getElementById(
        "backToPlanner"
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


function setScreen(
    screenName
) {

    currentScreen =
        screenName;

    for (
        const button
        of navButtons
    ) {

        button.classList.toggle(
            "active",
            button.dataset.screen === screenName
        );
    }


    for (
        const panel
        of screenPanels
    ) {

        const active =
            panel.dataset.screenPanel
            ===
            screenName;

        panel.hidden =
            !active;

        panel.classList.toggle(
            "active",
            active
        );
    }


    if (
        screenName === "recipes"
    ) {

        renderRecipeCards();
    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function getRecipe(
    filename
) {

    return recipes.find(
        recipe =>
            recipe.filename === filename
    );
}


function openRecipe(
    filename
) {

    const recipe =
        getRecipe(
            filename
        );

    if (!recipe) {
        return;
    }

    screenBeforeRecipe =
        currentScreen;

    appShell.hidden =
        true;

    viewerPanel.hidden =
        false;

    document.body.classList.add(
        "recipe-open"
    );

    recipeFrame.src =
        (
            "./recipes/"
            +
            encodeURIComponent(
                filename
            )
        );

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function closeRecipe() {

    recipeFrame.removeAttribute(
        "src"
    );

    viewerPanel.hidden =
        true;

    appShell.hidden =
        false;

    document.body.classList.remove(
        "recipe-open"
    );

    setScreen(
        screenBeforeRecipe
    );
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

    const standard =
        mealOrder.filter(
            meal =>
                present.has(
                    meal
                )
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
                    a.localeCompare(
                        b
                    )
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


    if (!meals.length) {

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
        (
            available
                ? "status-badge status-available"
                : "status-badge status-missing"
        );

    badge.textContent =
        (
            available
                ? "Available"
                : "Not generated yet"
        );

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
        !date
        ||
        !meal
    ) {

        scheduledRecipes.textContent =
            "No scheduled recipe.";

        return;
    }


    const matches =
        schedule.filter(
            item =>
                item.date === date
                &&
                item.meal_type === meal
        );


    if (!matches.length) {

        scheduledRecipes.textContent =
            "No recipe is scheduled for this meal.";

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
            (
                item.available
                    ? "scheduled-card scheduled-available"
                    : "scheduled-card scheduled-missing"
            );


        const top =
            document.createElement(
                "div"
            );

        top.className =
            "scheduled-card-header";


        const title =
            document.createElement(
                "div"
            );

        title.className =
            "scheduled-title";

        title.textContent =
            item.title;


        top.appendChild(
            title
        );

        top.appendChild(
            createStatusBadge(
                item.available
            )
        );

        card.appendChild(
            top
        );


        const context =
            document.createElement(
                "div"
            );

        context.className =
            "scheduled-context";

        context.textContent =
            (
                `${displayDate(item.date)}`
                +
                ` · ${item.meal_type}`
            );

        card.appendChild(
            context
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
                        item.file
                    );
                }
            );

            card.appendChild(
                button
            );

        } else {

            const message =
                document.createElement(
                    "div"
                );

            message.className =
                "not-generated-message";

            message.textContent =
                (
                    "This meal is in the plan, "
                    +
                    "but its recipe has not been generated yet."
                );

            card.appendChild(
                message
            );
        }


        scheduledRecipes.appendChild(
            card
        );
    }
}


function recipeRating(
    recipe
) {

    return (
        localStorage.getItem(
            (
                "recipe-rating:"
                +
                recipe.id
            )
        )
        ||
        "neutral"
    );
}


function ratingLabel(
    rating
) {

    if (
        rating === "favourite"
    ) {
        return "♥ Favourite";
    }

    if (
        rating === "dislike"
    ) {
        return "👎 Disliked";
    }

    return "";
}


function addOptions(
    select,
    values
) {

    const existing =
        new Set(
            Array.from(
                select.options
            )
            .map(
                option =>
                    option.value
            )
        );


    for (
        const value
        of values
    ) {

        if (
            !value
            ||
            existing.has(
                value
            )
        ) {
            continue;
        }

        const option =
            document.createElement(
                "option"
            );

        option.value =
            value;

        option.textContent =
            value;

        select.appendChild(
            option
        );
    }
}


function populateRecipeFilterOptions() {

    const mealTypes =
        new Set();

    const proteinSources =
        new Set();

    const cuisines =
        new Set();

    const difficulties =
        new Set();


    for (
        const recipe
        of recipes
    ) {

        for (
            const value
            of recipe.meal_types || []
        ) {
            mealTypes.add(
                value
            );
        }

        for (
            const value
            of recipe.protein_sources || []
        ) {
            proteinSources.add(
                value
            );
        }

        for (
            const value
            of recipe.cuisine || []
        ) {
            cuisines.add(
                value
            );
        }

        if (
            recipe.difficulty
        ) {
            difficulties.add(
                recipe.difficulty
            );
        }
    }


    addOptions(
        mealTypeFilter,
        [...mealTypes].sort()
    );

    addOptions(
        proteinSourceFilter,
        [...proteinSources].sort()
    );

    addOptions(
        cuisineFilter,
        [...cuisines].sort()
    );

    addOptions(
        difficultyFilter,
        [...difficulties].sort()
    );
}


function numericOrInfinity(
    value
) {

    const number =
        Number(value);

    return (
        Number.isFinite(
            number
        )
            ? number
            : Infinity
    );
}


function numericOrZero(
    value
) {

    const number =
        Number(value);

    return (
        Number.isFinite(
            number
        )
            ? number
            : 0
    );
}


function filteredAndSortedRecipes() {

    const search =
        recipeSearch.value
            .trim()
            .toLocaleLowerCase();

    const selectedRating =
        ratingFilter.value;

    const selectedMeal =
        mealTypeFilter.value;

    const selectedProteinSource =
        proteinSourceFilter.value;

    const maxActive =
        activeTimeFilter.value
            ? Number(
                activeTimeFilter.value
            )
            : null;

    const maxTotal =
        totalTimeFilter.value
            ? Number(
                totalTimeFilter.value
            )
            : null;

    const minimumProtein =
        minimumProteinFilter.value
            ? Number(
                minimumProteinFilter.value
            )
            : null;

    const selectedCuisine =
        cuisineFilter.value;

    const selectedDifficulty =
        difficultyFilter.value;


    const filtered =
        recipes.filter(
            recipe => {

                const rating =
                    recipeRating(
                        recipe
                    );


                if (
                    selectedRating
                    &&
                    rating !== selectedRating
                ) {
                    return false;
                }


                if (
                    selectedMeal
                    &&
                    !(
                        recipe.meal_types
                        ||
                        []
                    ).includes(
                        selectedMeal
                    )
                ) {
                    return false;
                }


                if (
                    selectedProteinSource
                    &&
                    !(
                        recipe.protein_sources
                        ||
                        []
                    ).includes(
                        selectedProteinSource
                    )
                ) {
                    return false;
                }


                if (
                    maxActive !== null
                    &&
                    numericOrInfinity(
                        recipe.active_time_minutes
                    )
                    >
                    maxActive
                ) {
                    return false;
                }


                if (
                    maxTotal !== null
                    &&
                    numericOrInfinity(
                        recipe.total_time_minutes
                    )
                    >
                    maxTotal
                ) {
                    return false;
                }


                if (
                    minimumProtein !== null
                    &&
                    numericOrZero(
                        recipe.protein_g
                    )
                    <
                    minimumProtein
                ) {
                    return false;
                }


                if (
                    selectedCuisine
                    &&
                    !(
                        recipe.cuisine
                        ||
                        []
                    ).includes(
                        selectedCuisine
                    )
                ) {
                    return false;
                }


                if (
                    selectedDifficulty
                    &&
                    recipe.difficulty
                    !==
                    selectedDifficulty
                ) {
                    return false;
                }


                if (search) {

                    const searchable =
                        [
                            recipe.title,
                            recipe.description,
                            recipe.filename,
                            ...(
                                recipe.meal_types
                                ||
                                []
                            ),
                            ...(
                                recipe.protein_sources
                                ||
                                []
                            ),
                            ...(
                                recipe.cuisine
                                ||
                                []
                            ),
                            ...(
                                recipe.dietary_tags
                                ||
                                []
                            )
                        ]
                            .filter(Boolean)
                            .join(" ")
                            .toLocaleLowerCase();


                    if (
                        !searchable.includes(
                            search
                        )
                    ) {
                        return false;
                    }
                }


                return true;
            }
        );


    const sortMode =
        recipeSort.value;


    filtered.sort(
        (a, b) => {

            if (
                sortMode === "active_asc"
            ) {

                return (
                    numericOrInfinity(
                        a.active_time_minutes
                    )
                    -
                    numericOrInfinity(
                        b.active_time_minutes
                    )
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            if (
                sortMode === "total_asc"
            ) {

                return (
                    numericOrInfinity(
                        a.total_time_minutes
                    )
                    -
                    numericOrInfinity(
                        b.total_time_minutes
                    )
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            if (
                sortMode === "protein_desc"
            ) {

                return (
                    numericOrZero(
                        b.protein_g
                    )
                    -
                    numericOrZero(
                        a.protein_g
                    )
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            if (
                sortMode === "energy_asc"
            ) {

                return (
                    numericOrInfinity(
                        a.energy_kcal
                    )
                    -
                    numericOrInfinity(
                        b.energy_kcal
                    )
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            if (
                sortMode === "energy_desc"
            ) {

                return (
                    numericOrZero(
                        b.energy_kcal
                    )
                    -
                    numericOrZero(
                        a.energy_kcal
                    )
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            if (
                sortMode === "favourite_first"
            ) {

                const rank = {
                    favourite: 0,
                    neutral: 1,
                    dislike: 2
                };

                return (
                    rank[
                        recipeRating(
                            a
                        )
                    ]
                    -
                    rank[
                        recipeRating(
                            b
                        )
                    ]
                    ||
                    a.title.localeCompare(
                        b.title
                    )
                );
            }


            return (
                a.title.localeCompare(
                    b.title
                )
            );
        }
    );


    return filtered;
}


function createMetaChip(
    text
) {

    const chip =
        document.createElement(
            "span"
        );

    chip.className =
        "recipe-meta-chip";

    chip.textContent =
        text;

    return chip;
}


function renderRecipeCards() {

    const matches =
        filteredAndSortedRecipes();

    recipeCards.innerHTML =
        "";

    recipeResultCount.textContent =
        (
            `${matches.length} `
            +
            (
                matches.length === 1
                    ? "recipe"
                    : "recipes"
            )
        );


    if (!matches.length) {

        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "empty-results";

        empty.textContent =
            "No recipes match these filters.";

        recipeCards.appendChild(
            empty
        );

        return;
    }


    for (
        const recipe
        of matches
    ) {

        const card =
            document.createElement(
                "article"
            );

        card.className =
            "recipe-result-card";

        card.tabIndex =
            0;


        const top =
            document.createElement(
                "div"
            );

        top.className =
            "recipe-result-top";


        const title =
            document.createElement(
                "h2"
            );

        title.textContent =
            recipe.title;

        top.appendChild(
            title
        );


        const rating =
            recipeRating(
                recipe
            );

        const ratingText =
            ratingLabel(
                rating
            );


        if (ratingText) {

            const ratingBadge =
                document.createElement(
                    "span"
                );

            ratingBadge.className =
                (
                    "recipe-rating-badge "
                    +
                    (
                        rating === "favourite"
                            ? "rating-favourite"
                            : "rating-dislike"
                    )
                );

            ratingBadge.textContent =
                ratingText;

            top.appendChild(
                ratingBadge
            );
        }


        card.appendChild(
            top
        );


        const meta =
            document.createElement(
                "div"
            );

        meta.className =
            "recipe-result-meta";


        for (
            const meal
            of recipe.meal_types || []
        ) {

            meta.appendChild(
                createMetaChip(
                    meal
                )
            );
        }


        for (
            const source
            of recipe.protein_sources || []
        ) {

            meta.appendChild(
                createMetaChip(
                    source
                )
            );
        }


        if (
            recipe.active_time_minutes
            !==
            null
            &&
            recipe.active_time_minutes
            !==
            undefined
        ) {

            meta.appendChild(
                createMetaChip(
                    (
                        `${recipe.active_time_minutes}`
                        +
                        " min active"
                    )
                )
            );
        }


        if (
            recipe.total_time_minutes
            !==
            null
            &&
            recipe.total_time_minutes
            !==
            undefined
        ) {

            meta.appendChild(
                createMetaChip(
                    (
                        `${recipe.total_time_minutes}`
                        +
                        " min total"
                    )
                )
            );
        }


        if (
            recipe.protein_g
            !==
            null
            &&
            recipe.protein_g
            !==
            undefined
        ) {

            meta.appendChild(
                createMetaChip(
                    (
                        `${recipe.protein_g}`
                        +
                        " g protein"
                    )
                )
            );
        }


        card.appendChild(
            meta
        );


        const open =
            document.createElement(
                "button"
            );

        open.type =
            "button";

        open.className =
            "recipe-card-open";

        open.textContent =
            "Open recipe";

        open.addEventListener(
            "click",
            event => {

                event.stopPropagation();

                openRecipe(
                    recipe.filename
                );
            }
        );

        card.appendChild(
            open
        );


        card.addEventListener(
            "click",
            () => {

                openRecipe(
                    recipe.filename
                );
            }
        );


        card.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter"
                    ||
                    event.key === " "
                ) {

                    event.preventDefault();

                    openRecipe(
                        recipe.filename
                    );
                }
            }
        );


        recipeCards.appendChild(
            card
        );
    }
}


function clearFilters() {

    recipeSearch.value =
        "";

    ratingFilter.value =
        "";

    mealTypeFilter.value =
        "";

    proteinSourceFilter.value =
        "";

    activeTimeFilter.value =
        "";

    totalTimeFilter.value =
        "";

    minimumProteinFilter.value =
        "";

    cuisineFilter.value =
        "";

    difficultyFilter.value =
        "";

    recipeSort.value =
        "title";

    renderRecipeCards();
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


        if (!recipeResponse.ok) {

            throw new Error(
                "Could not load recipes.json"
            );
        }


        if (!scheduleResponse.ok) {

            throw new Error(
                "Could not load schedule.json"
            );
        }


        recipes =
            await recipeResponse.json();

        schedule =
            await scheduleResponse.json();


        populateRecipeFilterOptions();


        const today =
            localTodayISO();

        const scheduledDates =
            [
                ...new Set(
                    schedule.map(
                        item =>
                            item.date
                    )
                )
            ]
                .sort();


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

        renderRecipeCards();

    } catch (
        error
    ) {

        console.error(
            error
        );

        scheduledRecipes.textContent =
            error.message;

        recipeCards.textContent =
            error.message;
    }
}


for (
    const button
    of navButtons
) {

    button.addEventListener(
        "click",
        () => {

            setScreen(
                button.dataset.screen
            );
        }
    );
}


dateSelect.addEventListener(
    "change",
    updateMealSelector
);


mealSelect.addEventListener(
    "change",
    updateScheduledRecipes
);


const recipeFilterControls = [
    recipeSearch,
    ratingFilter,
    mealTypeFilter,
    proteinSourceFilter,
    activeTimeFilter,
    totalTimeFilter,
    minimumProteinFilter,
    cuisineFilter,
    difficultyFilter,
    recipeSort
];


for (
    const control
    of recipeFilterControls
) {

    control.addEventListener(
        control === recipeSearch
            ? "input"
            : "change",
        renderRecipeCards
    );
}


clearRecipeFilters.addEventListener(
    "click",
    clearFilters
);


backToPlanner.addEventListener(
    "click",
    closeRecipe
);


dateSelect.addEventListener(
    "click",
    () => {

        if (
            typeof dateSelect.showPicker
            ===
            "function"
        ) {

            try {
                dateSelect.showPicker();
            } catch (
                error
            ) {
                // Browser fallback: normal date-input behaviour.
            }
        }
    }
);


setScreen(
    "meals"
);

loadData();
