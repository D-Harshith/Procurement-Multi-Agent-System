// web/static/agents.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://' + document.domain + ':5000');

    const sourcingOutput = document.getElementById('sourcing-output');
    const negotiationOutput = document.getElementById('negotiation-output');
    const orderOutput = document.getElementById('order-output');
    const finalOutcome = document.getElementById('final-outcome');
    const runButton = document.getElementById('runButton');

    // Prevent multiple clicks
    let isRunning = false;

    runButton.addEventListener('click', () => {
        if (isRunning) {
            return;
        }
        isRunning = true;
        runButton.disabled = true;

        // Clear previous outputs
        sourcingOutput.textContent = '';
        negotiationOutput.textContent = '';
        orderOutput.textContent = '';
        finalOutcome.textContent = '';

        // Trigger agent run
        fetch('/run-agents')
            .then(response => response.json())
            .catch(error => {
                finalOutcome.textContent += `Fetch error: ${error}\n`;
            });
    });

    socket.onopen = () => {};

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const { type, agent, message } = data;

            if (type === 'log') {
                const formattedMessage = `${message}\n`;
                if (agent === 'Sourcing Agent') {
                    sourcingOutput.textContent += formattedMessage;
                    sourcingOutput.scrollTop = sourcingOutput.scrollHeight;
                } else if (agent === 'Negotiation Agent') {
                    negotiationOutput.textContent += formattedMessage;
                    negotiationOutput.scrollTop = negotiationOutput.scrollHeight;
                } else if (agent === 'Order Agent') {
                    orderOutput.textContent += formattedMessage;
                    orderOutput.scrollTop = orderOutput.scrollHeight;
                }
            } else if (type === 'final') {
                console.log('Received Final Outcome:', message); // Temporary log to confirm receipt
                const formattedMessage = `${message}\n`;
                finalOutcome.textContent = formattedMessage;
                finalOutcome.scrollTop = finalOutcome.scrollHeight;
            } else if (type === 'error') {
                const formattedMessage = `${message}\n`;
                finalOutcome.textContent += formattedMessage;
                finalOutcome.scrollTop = finalOutcome.scrollHeight;
            } else if (type === 'complete') {
                isRunning = false;
                runButton.disabled = false;
            }
        } catch (error) {
            finalOutcome.textContent += `Error parsing WebSocket message: ${error}\n`;
        }
    };

    socket.onclose = () => {
        isRunning = false;
        runButton.disabled = false;
    };
});