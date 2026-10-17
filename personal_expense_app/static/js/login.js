
document.addEventListener("DOMContentLoaded", function () {

    const password =
        document.getElementById("password");

    const passwordToggle =
        document.getElementById("passwordToggle");

    const passwordIcon =
        document.getElementById("passwordIcon");


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


    const loginForm =
        document.querySelector(".login-form");


    loginForm.addEventListener("submit", function () {

        const button =
            document.querySelector(".login-button");

        button.classList.add("loading");

        button.querySelector("span").textContent =
            "Logging in...";

    });

});
