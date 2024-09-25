// Fade out an element
function fadeOut(el) {
    window.setTimeout(function () {
        el.classList.add("fade");
    }, 5);
    el.style.display = "none";
}

// Fade in an element
function fadeIn(el) {
    el.style.display = "block";
    window.requestAnimationFrame(function () {
        el.classList.remove("fade");
    });
}
