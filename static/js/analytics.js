/**
 * Chart.js initialization for analytics dashboard.
 */
function initAnalyticsCharts(lineData, pieData, barData) {
    const colors = {
        primary: '#0d6efd',
        success: '#198754',
        warning: '#ffc107',
        danger: '#dc3545',
        gray: '#6c757d',
    };

    const statusColors = {
        SAFE: colors.success,
        WARNING: colors.warning,
        DANGER: colors.danger,
    };

    const lineCtx = document.getElementById('lineChart');
    if (lineCtx) {
        new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: lineData.labels,
                datasets: [{
                    label: 'Daily Average',
                    data: lineData.values,
                    borderColor: colors.primary,
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true,
                    tension: 0.3,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } },
            },
        });
    }

    const pieCtx = document.getElementById('pieChart');
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: pieData.labels.length ? pieData.labels : ['No Data'],
                datasets: [{
                    data: pieData.values.length ? pieData.values : [1],
                    backgroundColor: pieData.labels.map((l) => statusColors[l] || colors.gray),
                }],
            },
            options: { responsive: true },
        });
    }

    const barCtx = document.getElementById('barChart');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: barData.labels.length ? barData.labels : ['No Rooms'],
                datasets: [{
                    label: 'Peak Reading',
                    data: barData.values.length ? barData.values : [0],
                    backgroundColor: colors.primary,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } },
            },
        });
    }
}
