const themeToggle = document.getElementById("theme-toggle");

function loadTheme() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "minecraft-light") {
        document.body.classList.add("minecraft-light-mode");
    }
}

function toggleTheme() {
    document.body.classList.toggle("minecraft-light-mode");

    const isMinecraftLight = document.body.classList.contains("minecraft-light-mode");

    localStorage.setItem("theme", isMinecraftLight ? "minecraft-light" : "win98-dark");
}

if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
}

loadTheme();