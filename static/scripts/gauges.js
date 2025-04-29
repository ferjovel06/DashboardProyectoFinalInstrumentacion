function createGauge(svgSelector, min, max, gradientId, initialValue, unit) {
    const svg = d3.select(svgSelector).select("svg");
    const width = +svg.attr("width");
    const height = +svg.attr("height");
    const radius = Math.min(width, height) / 2;

    const openAngle = 240 * Math.PI / 180; // 240 grados en radianes

    const scale = d3.scaleLinear()
        .domain([min, max])
        .range([-openAngle / 2, openAngle / 2]);

    const arc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius * 0.85)
        .startAngle(-openAngle / 2)
        .endAngle(openAngle / 2);

    const progressArc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius * 0.85)
        .startAngle(-openAngle / 2);

    // Elimina el gradiente y usa color sólido
    svg.append("path")
        .attr("d", arc)
        .attr("transform", `translate(${width / 2}, ${height / 2})`)
        .attr("fill", "#e0e5ec")
        .attr("stroke", "#c0c5ce")
        .attr("stroke-width", 2);

    const progressPath = svg.append("path")
        .attr("transform", `translate(${width / 2}, ${height / 2})`)
        .attr("fill", "#274C77");

    // Texto valor mínimo (izquierda)
    svg.append("text")
        .attr("x", width / 2 + radius * 0.85 * Math.cos(Math.PI / 1.2))
        .attr("y", height / 2 + radius * 0.85 * Math.sin(Math.PI / 1.2) + 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "18px")
        .attr("fill", "#161A41")
        .attr("opacity", 0.5)
        .text(min);

    // Texto valor máximo (derecha)
    svg.append("text")
        .attr("x", width / 2 - radius * 0.85 * Math.cos(Math.PI / 1.2))
        .attr("y", height / 2 + radius * 0.85 * Math.sin(Math.PI / 1.2) + 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "18px")
        .attr("fill", "#161A41")
        .attr("opacity", 0.5)
        .text(max);

    const text = svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2 + 10)
        .attr("text-anchor", "middle")
        .attr("font-size", "32px")
        .attr("fill", "#161A41")
        .text(`${initialValue}${unit}`);

    function update(value) {
        const angle = scale(value);
        progressPath.transition().duration(750).attr("d", progressArc.endAngle(angle));
        text.text(`${value}${unit}`);
    }

    update(initialValue);
    return update;
}