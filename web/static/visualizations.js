// web/static/visualizations.js
document.addEventListener('DOMContentLoaded', () => {
    const connectionStatus = document.getElementById('connection-status');

    // Initialize Market Price Chart
    const marketPriceCtx = document.getElementById('marketPriceChart').getContext('2d');
    const marketPriceChart = new Chart(marketPriceCtx, {
        type: 'line',
        data: {
            labels: visualizationData.marketPriceData.labels,
            datasets: [{
                label: 'Market Price (USD/lb)',
                data: visualizationData.marketPriceData.prices,
                borderColor: '#00704a',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time' } },
                y: { title: { display: true, text: 'Price (USD/lb)' }, min: 3, max: 6 }
            }
        }
    });

    // Initialize Suppliers Map (Scatter Plot)
    const suppliersCtx = document.getElementById('suppliersChart').getContext('2d');
    const suppliersChart = new Chart(suppliersCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Suppliers',
                data: visualizationData.suppliersData,
                backgroundColor: '#00704a',
                pointRadius: 8
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Longitude' }, min: -180, max: 180 },
                y: { title: { display: true, text: 'Latitude' }, min: -90, max: 90 }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const point = context.raw;
                            return `${point.name}: Quality ${point.quality}`;
                        }
                    }
                }
            }
        }
    });

    // Initialize Demand Forecast Chart
    const demandForecastCtx = document.getElementById('demandForecastChart').getContext('2d');
    const demandForecastChart = new Chart(demandForecastCtx, {
        type: 'line',
        data: {
            labels: visualizationData.demandForecastData.map(item => item.month),
            datasets: [{
                label: 'Demand (lbs)',
                data: visualizationData.demandForecastData.map(item => item.demand),
                borderColor: '#00704a',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Month' } },
                y: { title: { display: true, text: 'Demand (lbs)' }, min: 40000, max: 60000 }
            }
        }
    });

    // Function to update charts
    const updateCharts = () => {
        marketPriceChart.data.labels = visualizationData.marketPriceData.labels;
        marketPriceChart.data.datasets[0].data = visualizationData.marketPriceData.prices;
        marketPriceChart.update();

        suppliersChart.data.datasets[0].data = visualizationData.suppliersData;
        suppliersChart.update();

        demandForecastChart.data.labels = visualizationData.demandForecastData.map(item => item.month);
        demandForecastChart.data.datasets[0].data = visualizationData.demandForecastData.map(item => item.demand);
        demandForecastChart.update();
    };

    // Register the update function to be called when data changes
    visualizationData.registerClient(updateCharts);

    // Initial update
    updateCharts();

    // Update connect/disconnect status
    visualizationData.socket.onopen = () => {
        connectionStatus.textContent = 'Connected';
        connectionStatus.className = 'connection-status connected';
    };

    visualizationData.socket.onclose = () => {
        connectionStatus.textContent = 'Disconnected';
        connectionStatus.className = 'connection-status disconnected';
    };

    // Unregister the client when the page unloads
    window.addEventListener('unload', () => {
        visualizationData.unregisterClient(updateCharts);
    });
});