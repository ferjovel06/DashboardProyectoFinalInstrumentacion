let currentUnit = 'C'; // Default unit is Celsius

function changeTemperatureUnit(direction) {
    const tempElement = document.querySelector('.temperature-text');
    let tempValue = parseFloat(tempElement.textContent);

    if (currentUnit === 'C') {
        tempValue = direction === 'up' ? tempValue * 9 / 5 + 32 : tempValue + 273.15;
        currentUnit = direction === 'up' ? 'F' : 'K';
    } else if (currentUnit === 'F') {
        tempValue = direction === 'up' ? (tempValue - 32) * 5 / 9 + 273.15 : (tempValue - 32) * 5 / 9;
        currentUnit = direction === 'up' ? 'K' : 'C';
    } else if (currentUnit === 'K') {
        tempValue = direction === 'up' ? tempValue - 273.15 : (tempValue - 273.15) * 9 / 5 + 32;
        currentUnit = direction === 'up' ? 'C' : 'F';
    }

    tempElement.textContent = `${tempValue.toFixed(2)} °${currentUnit}`;
}