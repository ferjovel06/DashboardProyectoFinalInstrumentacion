function updateDateTime() {
    const now = new Date();
    const options = {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
        hourCycle: "h12",
    };
    const dateOptions = {
        weekday: "long",
        year: "numeric",
        month: "short",
        day: "numeric",
    };
    let time = now.toLocaleTimeString("es-ES", options);
    time = time.replace("a. m.", "AM").replace("p. m.", "PM");
    const date = now.toLocaleDateString("es-ES", dateOptions);
    const capitalizedDate =
        date.charAt(0).toUpperCase() + date.slice(1);
    document.getElementById(
        "datetime"
    ).textContent = `${time}      ${capitalizedDate}`;
}

setInterval(updateDateTime, 1000);
updateDateTime();