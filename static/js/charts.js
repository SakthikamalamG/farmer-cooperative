// Shared chart configurations and utilities
const ChartColors = {
    primary: '#198754',
    secondary: '#6c757d',
    success: '#20c997',
    info: '#0dcaf0',
    warning: '#ffc107',
    danger: '#dc3545',
    palette: ['#198754', '#0d6efd', '#6610f2', '#d63384', '#fd7e14', '#20c997', '#0dcaf0', '#ffc107']
};

function createBarChart(ctx, labels, data, label = 'Data') {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: ChartColors.palette,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

function createPieChart(ctx, labels, data) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ChartColors.palette,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function createLineChart(ctx, labels, data, label = 'Trend') {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: ChartColors.primary,
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

