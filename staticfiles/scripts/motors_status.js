document.addEventListener('DOMContentLoaded', function () {
    function actualizarEstadoMotores() {
        fetch('/get_motores/')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('motor-ph-alcalino-toggle').checked = data.motor_ph_alcalino;
                document.getElementById('motor-ph-acido-toggle').checked = data.motor_ph_acido;
                document.getElementById('motor-tds-altos-toggle').checked = data.motor_tds_altos;

                // Actualizamos el color de fondo de los toggles
                ['motor-ph-alcalino-toggle', 'motor-ph-acido-toggle', 'motor-tds-altos-toggle'].forEach(id => {
                    const motor = document.getElementById(id);
                    motor.style.backgroundColor = motor.checked ? '#516F91' : '';
                });
            })
            .catch(error => console.error('Error actualizando motores:', error));
    }

    // Función para enviar el estado del toggle al backend
    function cambiarEstadoMotor(id, estado) {
        fetch('/cambiar_estado_motor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  // Agregar CSRF token
            },
            body: JSON.stringify({ motor_id: id, estado: estado })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Estado cambiado:', data);
        })
        .catch(error => console.error('Error cambiando estado del motor:', error));
    }

    // Escuchar cambios en los toggles
    document.getElementById('motor-ph-alcalino-toggle').addEventListener('change', function () {
        cambiarEstadoMotor('motor-ph-alcalino', this.checked);
    });
    document.getElementById('motor-ph-acido-toggle').addEventListener('change', function () {
        cambiarEstadoMotor('motor-ph-acido', this.checked);
    });
    document.getElementById('motor-tds-altos-toggle').addEventListener('change', function () {
        cambiarEstadoMotor('motor-tds-altos', this.checked);
    });

    setInterval(actualizarEstadoMotores, 3000); // Actualiza cada 3 segundos
    actualizarEstadoMotores(); // Llamada inicial al cargar la página
});
