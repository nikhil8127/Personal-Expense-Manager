// Global Navigation, Sidebar Collapse/Hide Toggle & Mobile Drawer
(function () {
    // 1. Restore collapsed state immediately before DOM fully paints to avoid flash
    const savedState = localStorage.getItem("expense_sidebar_collapsed");
    if (savedState === "true" && window.innerWidth > 768) {
        document.body.classList.add("sidebar-collapsed");
    }

    document.addEventListener("DOMContentLoaded", function () {
        const sidebar = document.querySelector(
            ".dashboard-nav, .analytics-nav, .expense-nav, .income-nav, .transaction-nav, .transactions-nav, .budget-nav, .savings-nav, nav"
        );
        if (!sidebar) return;

        // 2. Create Floating Toggle Button if not already in DOM
        let floatingToggle = document.getElementById("floatingNavToggle");
        if (!floatingToggle) {
            floatingToggle = document.createElement("button");
            floatingToggle.id = "floatingNavToggle";
            floatingToggle.className = "floating-nav-toggle";
            floatingToggle.setAttribute("aria-label", "Open Navigation Menu");
            floatingToggle.innerHTML = '<i class="fa-solid fa-bars"></i> <span>Menu</span>';
            document.body.appendChild(floatingToggle);
        }

        // 3. Inject Collapse / Hide Button into Sidebar Header
        const brandHeader = sidebar.querySelector("h2");
        let collapseBtn = document.getElementById("sidebarCollapseBtn");
        if (brandHeader && !collapseBtn) {
            collapseBtn = document.createElement("button");
            collapseBtn.id = "sidebarCollapseBtn";
            collapseBtn.className = "sidebar-collapse-btn";
            collapseBtn.setAttribute("type", "button");
            collapseBtn.setAttribute("title", "Hide Navigation Sidebar (Ctrl+B)");
            collapseBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
            brandHeader.appendChild(collapseBtn);
        }

        // 4. Create Mobile Overlay if not present
        let overlay = document.querySelector(".sidebar-overlay");
        if (!overlay) {
            overlay = document.createElement("div");
            overlay.className = "sidebar-overlay";
            document.body.appendChild(overlay);
        }

        // 5. Toggle Functions
        function toggleSidebar(forceState) {
            if (window.innerWidth <= 768) {
                // Mobile behavior: drawer slide-over
                sidebar.classList.toggle("show-mobile");
                overlay.classList.toggle("active");
            } else {
                // Desktop behavior: collapse sidebar & expand content
                const isCurrentlyCollapsed = document.body.classList.contains("sidebar-collapsed");
                const shouldCollapse = forceState !== undefined ? forceState : !isCurrentlyCollapsed;

                if (shouldCollapse) {
                    document.body.classList.add("sidebar-collapsed");
                    localStorage.setItem("expense_sidebar_collapsed", "true");
                } else {
                    document.body.classList.remove("sidebar-collapsed");
                    localStorage.setItem("expense_sidebar_collapsed", "false");
                }
            }
        }

        // Event listeners
        if (collapseBtn) {
            collapseBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                toggleSidebar(true);
            });
        }

        if (floatingToggle) {
            floatingToggle.addEventListener("click", function (e) {
                e.stopPropagation();
                toggleSidebar(false);
            });
        }

        const mobileToggle = document.getElementById("mobileNavToggle");
        if (mobileToggle) {
            mobileToggle.addEventListener("click", function (e) {
                e.stopPropagation();
                toggleSidebar();
            });
        }

        overlay.addEventListener("click", function () {
            sidebar.classList.remove("show-mobile");
            overlay.classList.remove("active");
        });

        // 6. Keyboard Shortcut: Ctrl + B or '[' to Toggle Navigation
        document.addEventListener("keydown", function (e) {
            // Ignore if typing in an input, textarea, or select
            const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
            if (activeTag === "input" || activeTag === "textarea" || activeTag === "select") {
                return;
            }

            if ((e.ctrlKey && (e.key === "b" || e.key === "B")) || e.key === "[") {
                e.preventDefault();
                toggleSidebar();
            }
        });
    });
})();
