// web/server.js
const express = require('express');
const { WebSocketServer } = require('ws');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 5000;

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));
app.use('/static', express.static(path.join(__dirname, 'static')));

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Serve the visualizations page
app.get('/visualizations.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'visualizations.html'));
});

// Start the Express server
const server = app.listen(port, () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});

// WebSocket server
const wss = new WebSocketServer({ server });

let clients = [];

// Simulate market price updates
let marketPrice = 4.5; // Starting price in USD/lb
setInterval(() => {
    const fluctuation = (Math.random() * 0.4 - 0.2).toFixed(2);
    marketPrice = Math.max(3.5, Math.min(6.0, marketPrice + parseFloat(fluctuation)));
    clients.forEach(client => {
        if (client.readyState === 1) {
            client.send(JSON.stringify({
                type: 'marketPrice',
                price: marketPrice,
                timestamp: new Date().toISOString()
            }));
        }
    });
}, 15000);

// Simulated supplier data
const supplierData = [
    { name: "Supplier A", lat: 4.6, lon: -74.0, quality: 85 },
    { name: "Supplier B", lat: 9.9, lon: 38.7, quality: 90 },
    { name: "Supplier C", lat: 15.5, lon: 108.2, quality: 80 },
    { name: "Supplier D", lat: -6.2, lon: 106.8, quality: 88 },
    { name: "Supplier E", lat: -1.3, lon: -78.4, quality: 82 }
];

// Simulated demand forecast
const demandForecast = [
    { month: "Apr 2025", demand: 45000 },
    { month: "May 2025", demand: 47000 },
    { month: "Jun 2025", demand: 50000 },
    { month: "Jul 2025", demand: 48000 },
    { month: "Aug 2025", demand: 51000 },
    { month: "Sep 2025", demand: 53000 }
];

wss.on('connection', (ws) => {
    console.log('WebSocket client connected');
    clients.push(ws);

    // Send initial visualization data
    ws.send(JSON.stringify({ type: 'marketPrice', price: marketPrice, timestamp: new Date().toISOString() }));
    ws.send(JSON.stringify({ type: 'suppliers', data: supplierData }));
    ws.send(JSON.stringify({ type: 'demandForecast', data: demandForecast }));

    ws.on('close', () => {
        console.log('WebSocket client disconnected');
        clients = clients.filter(client => client !== ws);
    });
});

let currentPythonProcess = null;

// Run agents endpoint
app.get('/run-agents', (req, res) => {
    // Use an environment variable for the Python command, default to your local path
    const pythonCommand = process.env.PYTHON_COMMAND || 'F:\\Indiana University Bloomington\\Projects\\Multi agent system\\venv\\Scripts\\python.exe';
    const pythonPath = process.env.PYTHONPATH || 'F:\\Indiana University Bloomington\\Projects\\Multi agent system';

    // Spawn a child process to run the Python script
    const pythonProcess = spawn(pythonCommand, ['main.py'], {
        cwd: __dirname,
        env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONPATH: pythonPath }
    });

    currentPythonProcess = pythonProcess;

    let stopLogging = false;

    // Stream stdout from Python process to WebSocket clients
    pythonProcess.stdout.on('data', (data) => {
        const message = data.toString();
        clients.forEach(client => {
            if (client.readyState === 1) {
                let agentType = 'System';
                if (message.includes('Coffee Bean Sourcing Specialist') || message.includes('Sourcing')) {
                    agentType = 'Sourcing Agent';
                } else if (message.includes('Contract Negotiation Specialist') || message.includes('Negotiation')) {
                    agentType = 'Negotiation Agent';
                } else if (message.includes('Order Management Specialist') || message.includes('Order')) {
                    agentType = 'Order Agent';
                } else if (message.includes('Final Outcome')) {
                    agentType = 'Final Outcome';
                    stopLogging = true;
                }

                if (stopLogging && agentType !== 'Final Outcome') {
                    return;
                }

                client.send(JSON.stringify({
                    agent: agentType,
                    message: message.trim(),
                    timestamp: new Date().toISOString()
                }));
            }
        });
    });

    pythonProcess.stderr.on('data', (data) => {
        const errorMessage = `Python error: ${data.toString()}`;
        console.error(errorMessage);
        clients.forEach(client => {
            if (client.readyState === 1) {
                client.send(JSON.stringify({
                    agent: 'Final Outcome',
                    message: errorMessage,
                    timestamp: new Date().toISOString()
                }));
            }
        });
    });

    pythonProcess.on('error', (error) => {
        const errorMessage = `Failed to spawn Python process: ${error.message}`;
        console.error(errorMessage);
        clients.forEach(client => {
            if (client.readyState === 1) {
                client.send(JSON.stringify({
                    agent: 'Final Outcome',
                    message: errorMessage,
                    timestamp: new Date().toISOString()
                }));
            }
        });
    });

    pythonProcess.on('close', (code) => {
        const closeMessage = `Python process exited with code ${code}`;
        console.log(closeMessage);
        clients.forEach(client => {
            if (client.readyState === 1) {
                client.send(JSON.stringify({
                    agent: 'Final Outcome',
                    message: closeMessage,
                    timestamp: new Date().toISOString()
                }));
            }
        });
        currentPythonProcess = null;
    });

    res.json({ status: 'Agents running', pid: pythonProcess.pid });
});

// Stop agents endpoint
app.post('/stop-agents', (req, res) => {
    if (currentPythonProcess) {
        currentPythonProcess.kill('SIGTERM');
        currentPythonProcess = null;
        res.json({ status: 'Agents stopped' });
    } else {
        res.json({ status: 'No running process' });
    }
});