document.addEventListener('DOMContentLoaded', function () {
    function actualizarEstadoMotores() {
        fetch('/get_motores/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('motor-ph-alcalino-toggle').checked = data.motor_ph_alcalino;
                document.getElementById('motor-ph-acido-toggle').checked = data.motor_ph_acido;
                document.getElementById('motor-tds-altos-toggle').checked = data.motor_tds_altos;
                ['motor-ph-alcalino-toggle', 'motor-ph-acido-toggle', 'motor-tds-altos-toggle'].forEach(id => {
                    const motor = document.getElementById(id);
                    motor.style.backgroundColor = motor.checked ? '#516F91' : '';
                });
            })
            .catch(error => console.error('Error actualizando motores:', error));
    }

    setInterval(actualizarEstadoMotores, 3000);
    actualizarEstadoMotores();

    function enviarOrdenMotor(motor, state) {
        fetch('/set_motor_state/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({motor: motor, state: state})
        })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('Error al cambiar el estado del motor');
                }
            })
            .catch(error => {
                alert('Error de comunicación con el servidor');
            });
    }

    document.getElementById('motor-ph-alcalino-toggle').addEventListener('change', function () {
        enviarOrdenMotor('ph_alcalino', this.checked);
    });
    document.getElementById('motor-ph-acido-toggle').addEventListener('change', function () {
        enviarOrdenMotor('ph_acido', this.checked);
    });
    document.getElementById('motor-tds-altos-toggle').addEventListener('change', function () {
        enviarOrdenMotor('tds_altos', this.checked);
    });

    const autoModeToggle = document.getElementById('auto-mode-toggle');
    const autoModeLabel = document.getElementById('auto-mode-label');
    const motorToggles = [
        document.getElementById('motor-ph-alcalino-toggle'),
        document.getElementById('motor-ph-acido-toggle'),
        document.getElementById('motor-tds-altos-toggle')
    ];

    function setMotoresDisabled(disabled) {
        motorToggles.forEach(toggle => {
            toggle.disabled = disabled;
            toggle.style.opacity = disabled ? 0.5 : 1;  // Visual feedback
        });
    }


    // 🔥 IMPORTANTE: Al cargar la página, bloquear motores si corresponde
    setMotoresDisabled(!autoModeToggle.checked);
    autoModeLabel.textContent = autoModeToggle.checked ? "Manual" : "Auto";

    autoModeToggle.addEventListener('change', function () {
        const autoModeEnabled = this.checked;
        fetch('/set_auto_mode/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mode: autoModeEnabled ? "manual" : "auto"})
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setMotoresDisabled(!autoModeEnabled);
                    autoModeLabel.textContent = autoModeToggle.checked ? "Manual" : "Auto";
                } else {
                    alert('Error al cambiar modo automático');
                }
            })
            .catch(error => {
                alert('Error de comunicación con el servidor');
            });
    });
});