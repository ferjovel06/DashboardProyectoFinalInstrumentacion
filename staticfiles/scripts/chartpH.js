function actualizarGraficoPH() {
    fetch('/ph_data/')
        .then(response => response.json())
        .then(json => {
            crearGraficoGenerico("#grafica-ph", json.data, [0, 14], "ph", "#69b3a2");
        });
}

// Solo para la página de pH
if (document.getElementById("grafica-ph")) {
    actualizarGraficoPH();
    setInterval(actualizarGraficoPH, 5000); // Actualiza cada 5 segundos
}