function fetchpHIndicator() {
    fetch('/latest/')
        .then(response => response.json())
        .then(data => {
            const phElement = document.getElementById('last_ph');
            const alcalinoElement = document.getElementById('alcalino');
            const neutroElement = document.getElementById('neutro');
            const acidoElement = document.getElementById('acido');

            // Actualiza el valor de pH
            if (data.ph !== null && phElement) {
                phElement.innerText = data.ph.toFixed(2);  // Muestra el pH con 2 decimales
            }

            // Actualiza las clases dinámicamente
            if (data.ph > 8) {
                alcalinoElement.classList.add('active');
                neutroElement.classList.remove('active');
                acidoElement.classList.remove('active');
            } else if (data.ph >= 6.5 && data.ph <= 8) {
                alcalinoElement.classList.remove('active');
                neutroElement.classList.add('active');
                acidoElement.classList.remove('active');
            } else {
                alcalinoElement.classList.remove('active');
                neutroElement.classList.remove('active');
                acidoElement.classList.add('active');
            }
        })
        .catch(error => {
            console.error('Error fetching latest measurement:', error);
        });
}

// Llamar cada 5 segundos para actualizar en tiempo real
setInterval(fetchpHIndicator, 5000);

// Llamar inmediatamente al cargar para obtener los datos iniciales
fetchpHIndicator();
