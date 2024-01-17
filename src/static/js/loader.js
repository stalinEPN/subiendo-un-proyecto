document.addEventListener("DOMContentLoaded", function () {
    const loadingOverlay = document.getElementById("loading");
    const sidebarLinks = document.querySelectorAll(".sidebar a");

    sidebarLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            loadingOverlay.style.display = "flex";

            const targetURL = this.getAttribute("href");

            setTimeout(function () {
                window.location.href = targetURL;
            }, 100); 
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const btnVer = document.getElementById("abrirVer");
    const detect1 = document.getElementById("detectar1");

    detect1.addEventListener("click", function () {
        btnVer.click();
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const btnAdm = document.getElementById("abrirAdm");
    const detect2 = document.getElementById("detectar2");

    detect2.addEventListener("click", function () {
        btnAdm.click();
    });
});

