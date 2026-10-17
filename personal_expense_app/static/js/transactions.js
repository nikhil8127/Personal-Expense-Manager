
const searchInput = document.getElementById("searchInput");
const typeFilter = document.getElementById("typeFilter");

const rows = document.querySelectorAll(".transaction-row");

const incomeCount = document.getElementById("incomeCount");
const expenseCount = document.getElementById("expenseCount");


function updateCounts() {

    let income = 0;
    let expense = 0;

    rows.forEach(function(row) {

        const type = row
            .querySelector(".type-badge")
            ?.textContent
            .trim()
            .toLowerCase();

        if (type === "income") {
            income++;
        }

        if (type === "expense") {
            expense++;
        }

    });

    if (incomeCount) {
        incomeCount.textContent = income;
    }

    if (expenseCount) {
        expenseCount.textContent = expense;
    }

}


function filterTransactions() {

    const searchText = searchInput.value.toLowerCase();
    const selectedType = typeFilter.value.toLowerCase();

    rows.forEach(function(row) {

        const rowText = row.textContent.toLowerCase();

        const typeBadge = row.querySelector(".type-badge");

        const rowType = typeBadge
            ? typeBadge.textContent.trim().toLowerCase()
            : "";

        const searchMatch = rowText.includes(searchText);

        const typeMatch =
            selectedType === "all" ||
            rowType === selectedType;

        if (searchMatch && typeMatch) {

            row.style.display = "";

            row.style.animation = "rowAppear 0.4s ease";

        } else {

            row.style.display = "none";

        }

    });

}


if (searchInput) {

    searchInput.addEventListener("input", function() {

        filterTransactions();

    });

}


if (typeFilter) {

    typeFilter.addEventListener("change", function() {

        filterTransactions();

    });

}


updateCounts();

