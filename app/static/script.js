const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("active");
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

// Animate fun-fact tab
const funFactTab = document.querySelector(".fun-fact-tab");
if (funFactTab) observer.observe(funFactTab);

// Animate portfolio note separately
const portfolioNote = document.querySelector(".portfolio-note");
const noteObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("active");
    }
  });
}, { threshold: 0.2 });

if (portfolioNote) noteObserver.observe(portfolioNote);

// Language Toggle
let currentLang = "en";

const toggleBtn = document.getElementById("langToggle");

if (toggleBtn) {
  toggleBtn.addEventListener("click", () => {
    currentLang = currentLang === "en" ? "de" : "en";

    document.querySelectorAll("[data-en]").forEach((el) => {
      el.textContent = el.dataset[currentLang];
    });

    toggleBtn.textContent = currentLang === "en" ? "🇬🇧 EN" : "🇩🇪 DE";
  });
}
