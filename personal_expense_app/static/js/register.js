
document.addEventListener("DOMContentLoaded", function () {

    const password =
        document.getElementById("password");

    const passwordToggle =
        document.getElementById("passwordToggle");

    const passwordIcon =
        document.getElementById("passwordIcon");

    const strengthProgress =
        document.getElementById("strengthProgress");

    const strengthText =
        document.getElementById("strengthText");


    passwordToggle.addEventListener("click", function () {

        if (password.type === "password") {

            password.type = "text";

            passwordIcon.classList.remove("fa-eye");

            passwordIcon.classList.add("fa-eye-slash");

        } else {

            password.type = "password";

            passwordIcon.classList.remove("fa-eye-slash");

            passwordIcon.classList.add("fa-eye");

        }

    });


    password.addEventListener("input", function () {

        const value = password.value;

        let strength = 0;


        if (value.length >= 6) {
            strength++;
        }

        if (/[A-Z]/.test(value)) {
            strength++;
        }

        if (/[0-9]/.test(value)) {
            strength++;
        }

        if (/[^A-Za-z0-9]/.test(value)) {
            strength++;
        }


        if (value.length === 0) {

            strengthProgress.style.width = "0%";

            strengthText.textContent =
                "Enter a password";

        } else if (strength === 1) {

            strengthProgress.style.width = "25%";

            strengthText.textContent =
                "Weak password";

        } else if (strength === 2) {

            strengthProgress.style.width = "50%";

            strengthText.textContent =
                "Fair password";

        } else if (strength === 3) {

            strengthProgress.style.width = "75%";

            strengthText.textContent =
                "Good password";

        } else {

            strengthProgress.style.width = "100%";

            strengthText.textContent =
                "Strong password";

        }

    });


    const inputs =
        document.querySelectorAll(
            ".input-box input"
        );


    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            this.parentElement.classList.add("focused");

        });

        input.addEventListener("blur", function () {

            this.parentElement.classList.remove("focused");

        });

    });


    const form =
        document.querySelector(".register-form");


    form.addEventListener("submit", function () {

        const button =
            document.querySelector(".register-button");

        button.querySelector("span").textContent =
            "Creating Account...";

    });

});
