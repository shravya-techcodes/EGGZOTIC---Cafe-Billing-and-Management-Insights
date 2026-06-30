window.onload = function () {
    const canvas = document.getElementById("salesChart");
    if (canvas) {
        const ctx = canvas.getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: chartLabels,
                datasets: [{
                    label: "Sales Amount",
                    data: chartTotals,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Days"
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Amount"
                        }
                    }
                }
            }
        });
    }
}
