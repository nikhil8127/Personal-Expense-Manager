// Modernized Dashboard Charts with Chart.js
document.addEventListener("DOMContentLoaded", function () {
    if (typeof Chart !== "undefined") {
        Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif";
        Chart.defaults.color = "#64748b";
    }

    // 1. Finance Overview Bar Chart
    const financeCanvas = document.getElementById("financeChart");
    if (financeCanvas && typeof Chart !== "undefined") {
        new Chart(financeCanvas, {
            type: "bar",
            data: {
                labels: ["Income", "Expense", "Net Balance"],
                datasets: [{
                    label: "Amount (₹)",
                    data: [income, expense, balance],
                    backgroundColor: [
                        "rgba(16, 185, 129, 0.85)",
                        "rgba(239, 68, 68, 0.85)",
                        "rgba(37, 99, 235, 0.85)"
                    ],
                    borderColor: [
                        "#10b981",
                        "#ef4444",
                        "#2563eb"
                    ],
                    borderWidth: 1.5,
                    borderRadius: 8,
                    borderSkipped: false,
                    maxBarThickness: 45
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1200,
                    easing: "easeOutQuart"
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: "#0f172a",
                        titleFont: { size: 13, weight: "700" },
                        bodyFont: { size: 13, weight: "600" },
                        padding: 12,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (context) {
                                return " ₹" + Number(context.raw).toLocaleString("en-IN", {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                });
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: "#f1f5f9"
                        },
                        ticks: {
                            font: { size: 12 },
                            callback: function (value) {
                                return "₹" + value.toLocaleString("en-IN");
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: { size: 12, weight: "600" },
                            color: "#334155"
                        }
                    }
                }
            }
        });
    }

    // 2. Income vs Expense Doughnut Chart
    const summaryCanvas = document.getElementById("summaryChart");
    if (summaryCanvas && typeof Chart !== "undefined") {
        const total = (income + expense) || 1;
        new Chart(summaryCanvas, {
            type: "doughnut",
            data: {
                labels: ["Income", "Expense"],
                datasets: [{
                    data: [income, expense],
                    backgroundColor: [
                        "#10b981",
                        "#ef4444"
                    ],
                    hoverBackgroundColor: [
                        "#059669",
                        "#dc2626"
                    ],
                    borderWidth: 0,
                    spacing: 4,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "72%",
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1400
                },
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            boxWidth: 12,
                            boxHeight: 12,
                            borderRadius: 6,
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 20,
                            font: { size: 13, weight: "600" },
                            color: "#334155"
                        }
                    },
                    tooltip: {
                        backgroundColor: "#0f172a",
                        padding: 12,
                        cornerRadius: 8,
                        titleFont: { size: 13, weight: "700" },
                        bodyFont: { size: 13, weight: "600" },
                        callbacks: {
                            label: function (context) {
                                const val = Number(context.raw);
                                const pct = ((val / total) * 100).toFixed(1);
                                return ` ₹${val.toLocaleString("en-IN", { minimumFractionDigits: 2 })} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
});
