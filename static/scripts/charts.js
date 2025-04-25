document.addEventListener("DOMContentLoaded", function() {
    const rawJson = document.getElementById("mediciones-data").textContent;
    const rawData = JSON.parse(rawJson);

    // Función para procesar los datos y crear un gráfico
    function crearGrafico(id, key) {
        const data = rawData.map(d => {
            const parsedDate = new Date(d.timestamp);
            return {
                date: parsedDate,
                value: +d[key]  // Usar el valor de 'key' (temperatura, ph, tds)
            };
        });

        // dimensiones
        const margin = { top: 10, right: 30, bottom: 30, left: 60 },
              width = 460 - margin.left - margin.right,
              height = 400 - margin.top - margin.bottom;
        
        const svg = d3.select(id)
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        // Ejes
        const x = d3.scaleTime()
          .domain(d3.extent(data, d => d.date))
          .range([0, width]);
        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));
        
        const y = d3.scaleLinear()
          .domain(d3.extent(data, d => d.value))
          .range([height, 0]);
        svg.append("g")
          .call(d3.axisLeft(y));
        
        // Línea
        svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "#69b3a2")
          .attr("stroke-width", 1.5)
          .attr("d", d3.line()
            .x(d => x(d.date))
            .y(d => y(d.value))
          );
        
        // Puntos
        svg.selectAll("circle")
          .data(data)
          .enter()
          .append("circle")
            .attr("cx", d => x(d.date))
            .attr("cy", d => y(d.value))
            .attr("r", 2)
            .attr("fill", "#69b3a2");
    }

    // Crear gráficos para temperatura, pH y TDS
    crearGrafico("#grafica-temp", "temperature");
    crearGrafico("#grafica-ph", "ph");
    crearGrafico("#grafica-tds", "tds");
});