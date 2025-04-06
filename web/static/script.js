// web/static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://' + document.domain + ':5000');

    const sourcingStatus = document.getElementById('sourcing-status');
    const negotiationStatus = document.getElementById('negotiation-status');
    const orderStatus = document.getElementById('order-status');
    const connectionStatus = document.getElementById('connection-status');
    const runButton = document.getElementById('runButton');
    const logsOutput = document.getElementById('logs-output');
    const agentFilter = document.getElementById('agent-filter');

    let isRunning = false;
    let stopLogging = false;
    let pythonProcess = null; // To store the Python process ID for stopping
    let allLogs = []; // Store all logs for filtering

    // Update connect/disconnect status
    socket.onopen = () => {
        console.log('WebSocket connected');
        connectionStatus.textContent = 'Connected';
        connectionStatus.className = 'connection-status connected';
    };

    socket.onclose = () => {
        console.log('WebSocket disconnected');
        connectionStatus.textContent = 'Disconnected';
        connectionStatus.className = 'connection-status disconnected';
        isRunning = false;
        runButton.textContent = '▶';
        runButton.className = 'run-button idle';
        runButton.title = 'Run Agents';
    };

    // Run/Stop button handler
    runButton.addEventListener('click', () => {
        if (isRunning) {
            // Stop the process
            fetch('/stop-agents', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    console.log(data.status);
                    isRunning = false;
                    runButton.textContent = '▶';
                    runButton.className = 'run-button idle';
                    runButton.title = 'Run Agents';
                    stopLogging = false;
                    pythonProcess = null;
                })
                .catch(error => {
                    console.error('Error stopping agents:', error);
                    logsOutput.textContent += `[${new Date().toISOString()}] Error stopping agents: ${error}\n`;
                    logsOutput.scrollTop = logsOutput.scrollHeight;
                });
        } else {
            // Start the process
            isRunning = true;
            stopLogging = false;
            runButton.textContent = '■';
            runButton.className = 'run-button running';
            runButton.title = 'Stop Agents';

            // Clear previous outputs and reset statuses
            allLogs = [];
            logsOutput.textContent = '';
            sourcingStatus.textContent = 'Pending';
            sourcingStatus.className = 'status pending';
            negotiationStatus.textContent = 'Pending';
            negotiationStatus.className = 'status pending';
            orderStatus.textContent = 'Pending';
            orderStatus.className = 'status pending';

            // Trigger agent run via HTTP request
            fetch('/run-agents')
                .then(response => response.json())
                .then(data => {
                    console.log(data.status);
                    pythonProcess = data.pid; // Store the process ID
                })
                .catch(error => {
                    console.error('Error:', error);
                    logsOutput.textContent += `[${new Date().toISOString()}] Fetch error: ${error}\n`;
                    logsOutput.scrollTop = logsOutput.scrollHeight;
                    isRunning = false;
                    runButton.textContent = '▶';
                    runButton.className = 'run-button idle';
                    runButton.title = 'Run Agents';
                });
        }
    });

    // Handle WebSocket messages
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const { agent, message, timestamp } = data;
            const formattedMessage = `[${timestamp}] ${message}\n`;

            // Check if we should stop logging
            if (stopLogging && agent !== 'Final Outcome') {
                return;
            }

            // Store the log
            allLogs.push({ agent, message: formattedMessage });

            // Update statuses
            if (agent === 'Sourcing Agent') {
                sourcingStatus.textContent = 'Active';
                sourcingStatus.className = 'status active';
            } else if (agent === 'Negotiation Agent') {
                negotiationStatus.textContent = 'Active';
                negotiationStatus.className = 'status active';
            } else if (agent === 'Order Agent') {
                orderStatus.textContent = 'Active';
                orderStatus.className = 'status active';
            } else if (agent === 'Final Outcome') {
                stopLogging = true;
                if (message.includes('Python process exited') || message.includes('Python error') || message.includes('Failed to spawn Python process')) {
                    isRunning = false;
                    runButton.textContent = '▶';
                    runButton.className = 'run-button idle';
                    runButton.title = 'Run Agents';
                }
            }

            // Update logs display based on filter
            updateLogsDisplay();
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
            allLogs.push({ agent: 'Final Outcome', message: `[${new Date().toISOString()}] Error parsing WebSocket message: ${error}\n` });
            updateLogsDisplay();
            isRunning = false;
            runButton.textContent = '▶';
            runButton.className = 'run-button idle';
            runButton.title = 'Run Agents';
        }
    };

    // Update logs display based on filter
    function updateLogsDisplay() {
        const filterValue = agentFilter.value;
        logsOutput.textContent = '';
        const filteredLogs = allLogs.filter(log => filterValue === 'ALL' || log.agent === filterValue);
        filteredLogs.forEach(log => {
            logsOutput.textContent += log.message;
        });
        logsOutput.scrollTop = logsOutput.scrollHeight;
    }

    // Update logs when filter changes
    agentFilter.addEventListener('change', updateLogsDisplay);
});