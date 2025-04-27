function fetchLatestMeasurement() {
    fetch('/latest/')
        .then(response => response.json())
        .then(data => {
            if (data.temperature !== null) {
                document.getElementById('last_temp').innerText = data.temperature.toFixed(1) + ' °C';
            }
            if (data.ph !== null) {
                document.getElementById('last_ph').innerText = data.ph.toFixed(2);
            }
            if (data.tds !== null) {
                document.getElementById('last_tds').innerText = data.tds.toFixed(0) + ' ppm';
            }
            if (data.ec !== null) {
                document.getElementById('last_ec').innerText = data.ec.toFixed(2) + ' mS/cm';
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
