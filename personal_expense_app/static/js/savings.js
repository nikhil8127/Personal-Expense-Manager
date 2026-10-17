
document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".goal-card");

    cards.forEach(function (card, index) {

        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";

        setTimeout(function () {

            card.style.transition =
                "opacity 0.4s ease, transform 0.4s ease";

            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, Math.min(index * 80, 400));

    });


    const progressBars =
        document.querySelectorAll(".progress-fill");

    progressBars.forEach(function (bar) {

        const width = bar.style.width;

        bar.style.width = "0";

        setTimeout(function () {

            bar.style.width = width;

        }, 150);

    });


    const modal =
        document.getElementById("editGoalModal");

    const editForm =
        document.getElementById("editGoalForm");

    const goalName =
        document.getElementById("edit_goal_name");

    const targetAmount =
        document.getElementById("edit_target_amount");

    const deadline =
        document.getElementById("edit_deadline");

    const monthlyTarget =
        document.getElementById("edit_monthly_target");


    window.openEditGoal = function (
        goalId,
        name,
        target,
        goalDeadline,
        monthly
    ) {

        if (!modal || !editForm) {
            return;
        }

        goalName.value = name || "";

        targetAmount.value = target || "";

        deadline.value = goalDeadline || "";

        monthlyTarget.value = monthly || "";

        editForm.action =
            "/edit_savings/" + goalId;

        modal.classList.add("show");

        modal.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "modal-open"
        );

        setTimeout(function () {

            goalName.focus();

        }, 100);

    };


    window.closeEditGoal = function () {

        if (!modal) {
            return;
        }

        modal.classList.remove("show");

        modal.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "modal-open"
        );

    };


    if (modal) {

        modal.addEventListener(
            "click",
            function (event) {

                if (event.target === modal) {

                    window.closeEditGoal();

                }

            }
        );

    }


    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                modal &&
                modal.classList.contains("show")
            ) {

                window.closeEditGoal();

            }

        }
    );


    if (editForm) {

        editForm.addEventListener(
            "submit",
            function (event) {

                const name =
                    goalName.value.trim();

                const target =
                    parseFloat(
                        targetAmount.value
                    );

                const monthly =
                    monthlyTarget.value
                        ? parseFloat(
                            monthlyTarget.value
                        )
                        : 0;

                if (!name) {

                    event.preventDefault();

                    alert(
                        "Please enter a goal name."
                    );

                    goalName.focus();

                    return;

                }

                if (
                    isNaN(target) ||
                    target <= 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please enter a valid target amount."
                    );

                    targetAmount.focus();

                    return;

                }

                if (
                    isNaN(monthly) ||
                    monthly < 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please enter a valid monthly saving target."
                    );

                    monthlyTarget.focus();

                    return;

                }

            }
        );

    }


    const addMoneyForms =
        document.querySelectorAll(
            ".add-money-form"
        );

    addMoneyForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const input =
                    form.querySelector(
                        'input[name="amount"]'
                    );

                if (!input) {
                    return;
                }

                const amount =
                    parseFloat(input.value);

                if (
                    isNaN(amount) ||
                    amount <= 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please enter a valid amount."
                    );

                    input.focus();

                }

            }
        );

    });


    const withdrawForms =
        document.querySelectorAll(
            ".withdraw-money-form"
        );

    withdrawForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const input =
                    form.querySelector(
                        'input[name="amount"]'
                    );

                if (!input) {
                    return;
                }

                const amount =
                    parseFloat(input.value);

                const maximum =
                    parseFloat(input.max);

                if (
                    isNaN(amount) ||
                    amount <= 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please enter a valid withdrawal amount."
                    );

                    input.focus();

                    return;

                }

                if (
                    !isNaN(maximum) &&
                    amount > maximum
                ) {

                    event.preventDefault();

                    alert(
                        "You cannot withdraw more than the saved amount."
                    );

                    input.focus();

                    return;

                }

                const confirmWithdraw =
                    confirm(
                        "Are you sure you want to withdraw ₹" +
                        amount.toFixed(2) +
                        " from this savings goal?"
                    );

                if (!confirmWithdraw) {

                    event.preventDefault();

                }

            }
        );

    });


    const deleteForms =
        document.querySelectorAll(
            '.goal-menu form'
        );

    deleteForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const confirmed =
                    confirm(
                        "Delete this savings goal?"
                    );

                if (!confirmed) {

                    event.preventDefault();

                }

            }
        );

    });

});