// web/static/visualizationData.js
// Shared script to manage visualization data across pages
const visualizationData = {
    marketPriceData: { labels: [], prices: [] },
    suppliersData: [],
    demandForecastData: [],
    socket: null,
    clients: [], // To notify visualizations page of updates
};

// Initialize WebSocket connection
visualizationData.init = function() {
    if (visualizationData.socket && visualizationData.socket.readyState === WebSocket.OPEN) {
        return; // Already initialized
    }

    visualizationData.socket = new WebSocket('ws://' + document.domain + ':5000');

    visualizationData.socket.onopen = () => {
        console.log('Visualization WebSocket connected');
    };

    visualizationData.socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const { type, timestamp, price, data: chartData } = data;

            if (type === 'marketPrice') {
                visualizationData.marketPriceData.labels.push(new Date(timestamp).toLocaleTimeString());
                visualizationData.marketPriceData.prices.push(price);
                if (visualizationData.marketPriceData.labels.length > 10) {
                    visualizationData.marketPriceData.labels.shift();
                    visualizationData.marketPriceData.prices.shift();
                }
                // Notify all clients (e.g., visualizations page) of the update
                visualizationData.clients.forEach(client => client());
            } else if (type === 'suppliers') {
                visualizationData.suppliersData = chartData.map(supplier => ({
                    x: supplier.lon,
                    y: supplier.lat,
                    name: supplier.name,
                    quality: supplier.quality
                }));
                visualizationData.clients.forEach(client => client());
            } else if (type === 'demandForecast') {
                visualizationData.demandForecastData = chartData;
                visualizationData.clients.forEach(client => client());
            }
        } catch (error) {
            console.error('Error parsing WebSocket message in visualizationData:', error);
        }
    };

    visualizationData.socket.onclose = () => {
        console.log('Visualization WebSocket disconnected');
    };
};

// Register a client to be notified of updates
visualizationData.registerClient = function(client) {
    visualizationData.clients.push(client);
};

// Unregister a client
visualizationData.unregisterClient = function(client) {
    visualizationData.clients = visualizationData.clients.filter(c => c !== client);
};

// Initialize the WebSocket connection when the script loads
visualizationData.init();