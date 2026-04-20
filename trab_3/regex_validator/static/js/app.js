document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card, .hero, .metric-card");
    cards.forEach((card, index) => {
        card.style.animationDelay = `${Math.min(index * 0.06, 0.32)}s`;
    });
});
