function convertTemperature(value, targetUnit) {
    if (targetUnit === 'C') return value; // Already in Celsius
    if (targetUnit === 'F') return value * 9 / 5 + 32; // Convert to Fahrenheit
    if (targetUnit === 'K') return value + 273.15; // Convert to Kelvin
    return value;
}

function fetchLatestMeasurement() {
    fetch('/latest/')
        .then(response => response.json())
        .then(data => {
            const currentUnit = localStorage.getItem('temperatureUnit') || 'C'; // Get the selected unit

            if (data.temperature !== null) {
                const tempElement = document.getElementById('last_temp');
                if (tempElement) {
                    const convertedTemp = convertTemperature(data.temperature, currentUnit);
                    tempElement.innerText = convertedTemp.toFixed(2) + ` °${currentUnit}`;
                }
            }
            if (data.ph !== null) {
                const phElement = document.getElementById('last_ph');
                if (phElement) phElement.innerText = data.ph.toFixed(2);
            }
            if (data.tds !== null) {
                const tdsElement = document.getElementById('last_tds');
                if (tdsElement) tdsElement.innerText = data.tds.toFixed(0) + ' ppm';
            }
            if (data.ec !== null) {
                const ecElement = document.getElementById('last_ec');
                if (ecElement) ecElement.innerText = data.ec.toFixed(2) + ' mS/cm';
            }
        })
        .catch(error => {
            console.error('Error fetching latest measurement:', error);
        });
}

// Llamar cada 3 segundos
setInterval(fetchLatestMeasurement, 3000);

// Llamar una vez al cargar
fetchLatestMeasurement();
