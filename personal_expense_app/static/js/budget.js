
const budgetInput = document.getElementById("budget");
const previewAmount = document.getElementById("previewAmount");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

const budgetValue = parseFloat(
    document.getElementById("budgetValue")?.textContent || 0
);

const expenseValue = parseFloat(
    document.getElementById("expenseValue")?.textContent || 0
);

const remainingValue = document.getElementById("remainingValue");

const statusIcon = document.getElementById("statusIcon");
const statusTitle = document.getElementById("statusTitle");
const statusMessage = document.getElementById("statusMessage");


function updateBudgetPreview() {

    const budget = parseFloat(budgetInput.value);

    if (isNaN(budget) || budget <= 0) {

        previewAmount.textContent = "₹0.00";

        progressBar.style.width = "0%";

        progressText.textContent =
            "Enter your budget to see the progress.";

        return;

    }

    previewAmount.textContent = "₹" + budget.toFixed(2);

    let percentage = 0;

    if (expenseValue > 0) {
        percentage = (expenseValue / budget) * 100;
    }

    if (percentage > 100) {
        percentage = 100;
    }

    progressBar.style.width = percentage + "%";

    if (expenseValue === 0) {

        progressText.textContent =
            "No expenses recorded yet.";

    } else if (percentage < 50) {

        progressText.textContent =
            Math.round(percentage) +
            "% of your budget has been used.";

    } else if (percentage < 80) {

        progressText.textContent =
            Math.round(percentage) +
            "% used. Keep monitoring your spending.";

    } else if (percentage < 100) {

        progressText.textContent =
            Math.round(percentage) +
            "% used. You are approaching your budget limit.";

    } else {

        progressText.textContent =
            "Your expenses have reached or exceeded your budget.";

    }

}


function updateStatus() {

    if (!statusIcon || !statusTitle || !statusMessage) {
        return;
    }

    if (budgetValue <= 0) {

        statusTitle.textContent = "Set a Budget";

        statusMessage.textContent =
            "Set your monthly budget to start tracking your spending.";

        statusIcon.className = "status-icon";

        return;

    }

    const percentage = (expenseValue / budgetValue) * 100;

    if (percentage < 50) {

        statusTitle.textContent = "Budget Looking Good";

        statusMessage.textContent =
            "Your spending is currently below half of your budget.";

        statusIcon.className =
            "status-icon status-good";

        statusIcon.innerHTML =
            '<i class="fa-solid fa-circle-check"></i>';

    } else if (percentage < 80) {

        statusTitle.textContent = "Monitor Your Spending";

        statusMessage.textContent =
            "You are using a significant part of your budget.";

        statusIcon.className =
            "status-icon status-warning";

        statusIcon.innerHTML =
            '<i class="fa-solid fa-triangle-exclamation"></i>';

    } else {

        statusTitle.textContent = "Budget Limit Near";

        statusMessage.textContent =
            "Your expenses are close to or above your budget.";

        statusIcon.className =
            "status-icon status-danger";

        statusIcon.innerHTML =
            '<i class="fa-solid fa-circle-exclamation"></i>';

    }

}


if (budgetInput) {

    budgetInput.addEventListener(
        "input",
        updateBudgetPreview
    );

}


updateBudgetPreview();

updateStatus();


const budgetForm = document.getElementById("budgetForm");

if (budgetForm) {

    budgetForm.addEventListener("submit", function() {

        const button =
            this.querySelector(".budget-button");

        if (button) {

            button.style.opacity = "0.8";

            button.querySelector("span").innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Saving Budget...';

        }

    });

}

