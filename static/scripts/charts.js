function crearGraficoGenerico(selector, data, yDomain, dataKey, color) {
    d3.select(selector).selectAll("*").remove(); // Limpia la gráfica anterior

    const margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select(selector)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const x = d3.scaleTime()
        .domain(d3.extent(data, d => new Date(d.timestamp)))
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    const y = d3.scaleLinear()
        .domain(yDomain)
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", color)
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(d => x(new Date(d.timestamp)))
            .y(d => y(d[dataKey]))
        );

    svg.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(new Date(d.timestamp)))
        .attr("cy", d => y(d[dataKey]))
        .attr("r", 2)
        .attr("fill", color);
}