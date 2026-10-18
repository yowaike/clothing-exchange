document.addEventListener("DOMContentLoaded", () => {
    const catalog = document.querySelector("#catalog");
    const catalogLink = document.querySelector("a[href='#catalog']");

    if (catalog && catalogLink) {
        catalogLink.addEventListener("click", () => {
            catalog.classList.add("catalog-visited");
        });
    }
});
