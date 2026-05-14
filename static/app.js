const themeToggle = document.getElementById("theme-toggle");
const LIGHT_THEME = "light-mode";
const DARK_THEME = "dark-mode";

function updateToggleLabel() {
    if (!themeToggle) {
        return;
    }

    const isLight = document.body.classList.contains(LIGHT_THEME);
    themeToggle.textContent = isLight ? "Switch to Dark" : "Switch to Light";
}

function loadTheme() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === LIGHT_THEME) {
        document.body.classList.add(LIGHT_THEME);
    } else {
        document.body.classList.remove(LIGHT_THEME);
    }

    updateToggleLabel();
}

function toggleTheme() {
    document.body.classList.toggle(LIGHT_THEME);
    const isLight = document.body.classList.contains(LIGHT_THEME);

    localStorage.setItem("theme", isLight ? LIGHT_THEME : DARK_THEME);
    updateToggleLabel();
}

if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
}

loadTheme();