// Add Income Interaction Enhancements
document.addEventListener("DOMContentLoaded", function () {
    const amountInput = document.getElementById("amount");
    const amountPreview = document.getElementById("amountPreview");
    const incomeForm = document.getElementById("incomeForm");
    const dateInput = document.getElementById("date");

    // 1. Auto-fill Today's Date if empty
    if (dateInput && !dateInput.value) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, "0");
        const dd = String(today.getDate()).padStart(2, "0");
        dateInput.value = `${yyyy}-${mm}-${dd}`;
    }

    // 2. Real-time Amount Preview Formatting
    function updatePreview() {
        if (!amountInput || !amountPreview) return;
        const val = parseFloat(amountInput.value);
        if (!isNaN(val) && val > 0) {
            amountPreview.textContent = "+₹" + val.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            amountPreview.classList.add("show");
        } else {
            amountPreview.textContent = "₹0.00";
            amountPreview.classList.remove("show");
        }
    }

    if (amountInput) {
        amountInput.addEventListener("input", updatePreview);
    }

    // 3. Quick Amount Chips
    const chips = document.querySelectorAll(".amount-chip");
    chips.forEach(chip => {
        chip.addEventListener("click", function () {
            const addVal = parseFloat(this.getAttribute("data-amount")) || 0;
            const currentVal = parseFloat(amountInput.value) || 0;
            amountInput.value = (currentVal + addVal).toFixed(2);
            updatePreview();
        });
    });

    // 4. Focus Icon Styling
    const formInputs = document.querySelectorAll(
        "#incomeForm input, #incomeForm select, #incomeForm textarea"
    );

    formInputs.forEach(input => {
        input.addEventListener("focus", function () {
            const icon = this.parentElement.querySelector("i");
            if (icon) icon.style.color = "#10b981";
        });
        input.addEventListener("blur", function () {
            const icon = this.parentElement.querySelector("i");
            if (icon) icon.style.color = "";
        });
    });

    // 5. Submit loading spinner
    if (incomeForm) {
        incomeForm.addEventListener("submit", function () {
            const submitBtn = this.querySelector(".income-submit");
            if (submitBtn) {
                submitBtn.style.opacity = "0.85";
                submitBtn.querySelector("span").innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving Income...';
            }
        });
    }
});
