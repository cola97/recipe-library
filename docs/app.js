let recipes = [];
let schedule = [];
let filteredRecipes = [];


const dateSelect =
    document.getElementById("dateSelect");

const mealSelect =
    document.getElementById("mealSelect");

const scheduledRecipes =
    document.getElementById("scheduledRecipes");

const recipeSearch =
    document.getElementById("recipeSearch");

const allRecipes =
    document.getElementById("allRecipes");

const openLibraryRecipe =
    document.getElementById("openLibraryRecipe");

const recipeFrame =
    document.getElementById("recipeFrame");

const viewerPlaceholder =
    document.getElementById("viewerPlaceholder");

const currentContext =
    document.getElementById("currentContext");


function localTodayISO() {

    const now = new Date();

    const year =
        now.getFullYear();

    const month =
        String(now.getMonth() + 1).padStart(2, "0");

    const day =
        String(now.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}


function displayDate(isoDate) {

    if (!isoDate) {
        return "";
    }

    const [
        year,
        month,
        day
    ] = isoDate.split("-");

    return `${day}/${month}/${year}`;
}


function getRecipe(filename) {

    return recipes.find(
        recipe =>
            recipe.filename === filename
    );

}


function openRecipe(filename, contextText = "") {

    const recipe =
        getRecipe(filename);

    recipeFrame.src =
        `./recipes/${encodeURIComponent(filename)}`;

    recipeFrame.hidden = false;

    viewerPlaceholder.hidden = true;

    if (contextText) {

        currentContext.textContent =
            contextText;

    } else if (recipe) {

        currentContext.textContent =
            recipe.title;

    } else {

        currentContext.textContent =
            filename;

    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


function getMealsForDate(date) {

    const types = [
        ...new Set(
            schedule
                .filter(
                    item =>
                        item.date === date
                )
                .map(
                    item =>
                        item.meal_type
                )
        )
    ];

    return types;
}


function updateMealSelector() {

    const date =
        dateSelect.value;

    const existingMeal =
        mealSelect.value;

    const meals =
        getMealsForDate(date);

    mealSelect.innerHTML = "";

    if (meals.length === 0) {

        const option =
            document.createElement("option");

        option.value = "";
        option.textContent =
            "No scheduled meals";

        mealSelect.appendChild(option);

        updateScheduledRecipes();

        return;
    }

    for (const meal of meals) {

        const option =
            document.createElement("option");

        option.value = meal;
        option.textContent = meal;

        mealSelect.appendChild(option);

    }

    if (meals.includes(existingMeal)) {

        mealSelect.value =
            existingMeal;

    } else if (meals.includes("Breakfast")) {

        mealSelect.value =
            "Breakfast";

    } else {

        mealSelect.value =
            meals[0];

    }

    updateScheduledRecipes();
}


function updateScheduledRecipes() {

    const date =
        dateSelect.value;

    const meal =
        mealSelect.value;

    scheduledRecipes.innerHTML = "";

    if (!date || !meal) {

        const message =
            document.createElement("div");

        message.textContent =
            "No scheduled recipe.";

        scheduledRecipes.appendChild(
            message
        );

        return;
    }

    const matches =
        schedule.filter(
            item =>
                item.date === date &&
                item.meal_type === meal
        );

    if (matches.length === 0) {

        const message =
            document.createElement("div");

        message.textContent =
            "No recipe is scheduled for this meal.";

        scheduledRecipes.appendChild(
            message
        );

        currentContext.textContent =
            `${displayDate(date)} — ${meal}`;

        return;
    }

    for (const item of matches) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "scheduled-button";

        button.textContent =
            item.title;

        button.addEventListener(
            "click",
            () => {

                openRecipe(
                    item.file,
                    `${displayDate(item.date)} — ${item.meal_type} — ${item.title}`
                );

            }
        );

        scheduledRecipes.appendChild(
            button
        );

    }

    currentContext.textContent =
        `${displayDate(date)} — ${meal}`;

    /*
       If exactly one recipe matches the selected
       date and meal, open it automatically.
    */

    if (matches.length === 1) {

        const item =
            matches[0];

        openRecipe(
            item.file,
            `${displayDate(item.date)} — ${item.meal_type} — ${item.title}`
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
                    ...(recipe.meal_types || [])
                ]
                    .join(" ")
                    .toLocaleLowerCase();

                return searchable.includes(
                    query
                );

            }
        );

    allRecipes.innerHTML = "";

    for (const recipe of filteredRecipes) {

        const option =
            document.createElement("option");

        option.value =
            recipe.filename;

        const typeText =
            recipe.meal_types?.length
                ? ` — ${recipe.meal_types.join(", ")}`
                : "";

        option.textContent =
            `${recipe.title}${typeText}`;

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
        ] = await Promise.all([
            fetch("./recipes.json"),
            fetch("./schedule.json")
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

        populateRecipeLibrary();

        /*
           Start on today's date.

           If today's date has no schedule but scheduled
           dates exist, use the earliest scheduled date
           instead. This is convenient during initial
           testing.
        */

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

        } else if (scheduledDates.length) {

            dateSelect.value =
                scheduledDates[0];

        } else {

            dateSelect.value =
                today;

        }

        updateMealSelector();

    }

    catch (error) {

        console.error(error);

        currentContext.textContent =
            "The recipe library could not be loaded.";

        scheduledRecipes.textContent =
            error.message;

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

        openRecipe(filename);

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

        openRecipe(filename);

    }
);


loadData();