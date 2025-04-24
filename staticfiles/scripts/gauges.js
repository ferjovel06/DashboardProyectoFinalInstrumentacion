const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");
const radius = Math.min(width, height) / 2;

const minTemp = -55;
const maxTemp = 125;
const currentTemp = {{ last_temp | default: "null"}};

// Define el arco del gauge
const arc = d3.arc()
    .innerRadius(radius * 0.7)
    .outerRadius(radius * 0.9)
    .startAngle(-Math.PI / 2)
    .endAngle(Math.PI / 2);

// Gradiente de color
const defs = svg.append("defs");
const gradient = defs.append("linearGradient")
    .attr("id", "temperatureGradient")
    .attr("x1", "0%")
    .attr("x2", "100%")
    .attr("y1", "0%")
    .attr("y2", "0%");

gradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "blue");
gradient.append("stop")
    .attr("offset", "50%")
    .attr("stop-color", "green");
gradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "red");

// Dibuja el arco
svg.append("path")
    .attr("d", arc)
    .attr("transform", `translate(${width / 2}, ${height / 2})`)
    .attr("fill", "url(#temperatureGradient)");

// Calcula el ángulo de la aguja
const scale = d3.scaleLinear()
    .domain([minTemp, maxTemp])
    .range([-Math.PI / 2, Math.PI / 2]);

const needleAngle = scale(currentTemp);

// Dibuja la aguja
const needleLength = radius * 0.8;
const needle = svg.append("line")
    .attr("x1", width / 2)
    .attr("y1", height / 2)
    .attr("x2", width / 2 + needleLength * Math.sin(needleAngle))
    .attr("y2", height / 2 + needleLength * -Math.cos(needleAngle))

    .attr("stroke", "black")
    .attr("stroke-width", 2);

// Texto de la temperatura actual
svg.append("text")
    .attr("x", width / 2)
    .attr("y", height / 2 + radius * 0.6)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .attr("fill", "#333")
    .text(currentTemp !== null ? `${currentTemp}°C` : "N/A");