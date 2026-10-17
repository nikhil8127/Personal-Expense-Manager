// Enhanced Interactive Analytics, Number Counters & Lightbox
document.addEventListener("DOMContentLoaded", function () {

    // 1. Staggered Entrance Animation for Cards
    const animateCards = document.querySelectorAll(".animate-card, .chart-card, .breakdown-card");
    animateCards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(16px)";
        setTimeout(() => {
            card.style.transition = "opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1)";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, Math.min(index * 50, 400));
    });

    // 2. Animate Number Counters (Count-up effect)
    const counters = document.querySelectorAll(".counter-number");
    counters.forEach(counter => {
        const targetValue = parseFloat(counter.getAttribute("data-value"));
        if (isNaN(targetValue)) return;

        let startTime = null;
        const duration = 900; // ms

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            // Ease-out cubic curve
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentVal = targetValue * easeProgress;

            counter.textContent = "₹" + currentVal.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                counter.textContent = "₹" + targetValue.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
            }
        }

        requestAnimationFrame(step);
    });

    // 3. Progress Bar Fill Animation
    const progressFills = document.querySelectorAll(".progress-bar-fill");
    progressFills.forEach(fill => {
        const finalWidth = fill.style.width;
        fill.style.width = "0%";
        setTimeout(() => {
            fill.style.width = finalWidth;
        }, 150);
    });

    // 4. Click to Zoom Lightbox Modal
    const chartImages = document.querySelectorAll(".chart-image-container img");

    function closeLightbox() {
        document.querySelectorAll(".chart-image-container img.zoomed").forEach(img => {
            img.classList.remove("zoomed");
        });
        const backdrop = document.getElementById("chartZoomBackdrop");
        if (backdrop) backdrop.remove();
    }

    chartImages.forEach(image => {
        image.addEventListener("click", function (e) {
            e.stopPropagation();
            const isZoomed = this.classList.contains("zoomed");

            closeLightbox();

            if (!isZoomed) {
                this.classList.add("zoomed");

                const backdrop = document.createElement("div");
                backdrop.id = "chartZoomBackdrop";
                backdrop.style.position = "fixed";
                backdrop.style.inset = "0";
                backdrop.style.background = "rgba(15, 23, 42, 0.8)";
                backdrop.style.backdropFilter = "blur(6px)";
                backdrop.style.zIndex = "1999";
                backdrop.style.cursor = "zoom-out";
                backdrop.style.display = "flex";
                backdrop.style.alignItems = "flex-start";
                backdrop.style.justifyContent = "flex-end";
                backdrop.style.padding = "24px 30px";
                backdrop.innerHTML = `
                    <button type="button" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: white; width: 42px; height: 42px; border-radius: 50%; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: all 0.2s;">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                `;

                document.body.appendChild(backdrop);
                backdrop.addEventListener("click", closeLightbox);
            }
        });
    });

    // Close on Escape Key
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            closeLightbox();
        }
    });
});
