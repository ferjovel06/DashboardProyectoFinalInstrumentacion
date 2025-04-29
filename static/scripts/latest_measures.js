function fetchLatestMeasurement() {
    fetch('/latest/')
        .then(response => response.json())
        .then(data => {
            if (data.temperature !== null) {
                const tempElement = document.getElementById('last_temp');
                if (tempElement) tempElement.innerText = data.temperature.toFixed(1) + ' °C';
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

// Llamar cada 5 segundos
setInterval(fetchLatestMeasurement, 5000);

// Llamar una vez al cargar
fetchLatestMeasurement();
