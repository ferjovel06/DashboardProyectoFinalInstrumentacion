function actualizarGraficoTds() {
    fetch('/tds_data/')
        .then(response => response.json())
        .then(json => {
            crearGraficoGenerico("#grafica-tds", json.data, [0, 2000], "tds", "#69b3a2");
        });
}

// Solo para la página de Solidos Totales Disueltos
if (document.getElementById("grafica-tds")) {
    actualizarGraficoTds();
    setInterval(actualizarGraficoTds, 5000); // Actualiza cada 5 segundos
}