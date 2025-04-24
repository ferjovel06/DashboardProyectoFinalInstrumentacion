function createGauge(svgSelector, min, max, gradientId, initialValue, unit) {
    const svg = d3.select(svgSelector).select("svg");
    const width = +svg.attr("width");
    const height = +svg.attr("height");
    const radius = Math.min(width, height) / 2;

    const scale = d3.scaleLinear()
        .domain([min, max])
        .range([-Math.PI / 1.2, Math.PI / 1.2]);

    const arc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius * 0.85)
        .startAngle(-Math.PI / 1.2)
        .endAngle(Math.PI / 1.2);

    const progressArc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius * 0.85)
        .startAngle(-Math.PI / 1.2);

    const defs = svg.append("defs");
    const gradient = defs.append("linearGradient")
        .attr("id", gradientId)
        .attr("x1", "0%").attr("y1", "100%")
        .attr("x2", "100%").attr("y2", "0%");
    
    gradient.append("stop").attr("offset", "0%").attr("stop-color", "#1e90ff").attr("stop-opacity", 0.9);
    gradient.append("stop").attr("offset", "50%").attr("stop-color", "#32cd32").attr("stop-opacity", 0.9);
    gradient.append("stop").attr("offset", "100%").attr("stop-color", "#ffa500").attr("stop-opacity", 0.9);

    svg.append("path")
        .attr("d", arc)
        .attr("transform", `translate(${width / 2}, ${height / 2})`)
        .attr("fill", "#e0e5ec")
        .attr("stroke", "#c0c5ce")
        .attr("stroke-width", 2);

    const progressPath = svg.append("path")
        .attr("transform", `translate(${width / 2}, ${height / 2})`)
        .attr("fill", `url(#${gradientId})`);

    const text = svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2 + 10)
        .attr("text-anchor", "middle")
        .attr("font-size", "24px")
        .attr("fill", "#333")
        .text(`${initialValue}${unit}`);

    function update(value) {
        const angle = scale(value);
        progressPath.transition().duration(750).attr("d", progressArc.endAngle(angle));
        text.text(`${value}${unit}`);
    }

    update(initialValue);
    return update;
}