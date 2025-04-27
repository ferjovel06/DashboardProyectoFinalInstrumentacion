function fetchObservations() {
    fetch('/get_observations/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('observations-container');
            container.innerHTML = '';

            data.observations.forEach((obs, index) => {
                const colorHue = (index + 1) * 60; // Igual que tu template
                const observationHTML = `
                    <div class="mb-2">
                        <div class="d-flex align-items-center">
                            <span
                                class="rounded-circle me-2"
                                style="display:inline-block; width:12px; height:12px; background-color: hsl(${colorHue}, 70%, 55%);"
                            ></span>
                            <span class="fw-bold" style="color: #516F91; flex: 1;">${obs.text}</span>
                        </div>
                        <div class="d-flex justify-content-start">
                            <span class="ms-4 text-muted" style="white-space: nowrap; color: #879CB3;">${obs.timestamp}</span>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', observationHTML);
            });
        })
        .catch(error => console.error('Error al obtener observaciones:', error));
}

// Llamarlo cada 5 segundos
setInterval(fetchObservations, 5000);

// Llamarlo al cargar
fetchObservations();