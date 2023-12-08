function saveFiles(elem) {
    if ('webkitdirectory' in elem) {
        const csrfToken = document.getElementById('csrf_token').value;
        const files = elem.files;
        var formData = new FormData();
        var counter = 0;
        for (const file of files) {
            counter++;
            // Aquí puedes realizar la lógica para guardar el archivo
            formData.append('files[]', file);
            if (counter == 250) {
                makeRequest(formData, csrfToken, false);
                counter = 0;
                formData = new FormData();
            }
        }
        makeRequest(formData, csrfToken, true);
    } else {
        alert('El navegador no admite la propiedad "webkitdirectory".');
    }
}

function makeRequest(formData, csrfToken, final) {
    fetch('/save-tmp-files', {method: "POST", body: formData, headers: {
        'X-CSRFToken': csrfToken,
    }})
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta del servidor:', data);
            if (final) {
                document.getElementById("submit-btn").disabled = false;
            }
        })
        .catch(error => {
            console.error('Error al enviar el archivo:', error);
        });
}

let form = document.getElementById("form");

form.onsubmit = function(){
    document.getElementById("submit-btn").style.display = 'none';
    document.getElementById("envio").innerHTML ="<img src='static/images/loading.gif' width='100' height='100'> Subiendo Estudio... Esto puede tardar varios minutos.</img>";
    return true;
}

var institution = document.getElementById('institution');
var equipment = document.getElementById('equipo');
const csrfToken = document.getElementById('csrf_token').value;
institution.addEventListener('change', function () {
    var institution_id = institution.value;

    // Realizar una solicitud Fetch para obtener los datos para el segundo select
    fetch('/get_equipments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: 'institution_id=' + institution_id
    })
    .then(response => response.json())
    .then(data => {
        // Limpiar las opciones existentes en el segundo select
        while (equipment.firstChild) {
            equipment.removeChild(equipment.firstChild);
        }
        // Llenar el segundo select con los nuevos datos
        data.forEach(function (value) {
            var option = document.createElement('option');
            option.value = value.id;
            option.text = value.brand + ' - ' + value.model + ' - ' + value.potency;
            equipment.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));
});
