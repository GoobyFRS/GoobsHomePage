const themeToggle = document.getElementById("theme-toggle");

function loadTheme() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
    }
}

function toggleTheme() {
    document.body.classList.toggle("light-mode");

    const isLight = document.body.classList.contains("light-mode");

    localStorage.setItem("theme", isLight ? "light" : "dark");
}

if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
}

loadTheme();