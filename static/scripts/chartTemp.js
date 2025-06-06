function actualizarGraficoTemp() {
    fetch('/temp_data/')
        .then(response => response.json())
        .then(json => {
            crearGraficoGenerico("#grafica-temp", json.data, [-55, 125], "temp", "#69b3a2");
        });
}

// Solo para la página de Temperatura
if (document.getElementById("grafica-temp")) {
    actualizarGraficoTemp();
    setInterval(actualizarGraficoTemp, 5000); // Actualiza cada 5 segundos
}