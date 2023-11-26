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
                makeRequest(formData, csrfToken);
                counter = 0;
                formData = new FormData();
            }
        }
        makeRequest(formData, csrfToken);
        document.getElementById("submit-btn").disabled = false;
    } else {
        alert('El navegador no admite la propiedad "webkitdirectory".');
    }
}

function makeRequest(formData, csrfToken) {
    fetch('/save-tmp-files', {method: "POST", body: formData, headers: {
        'X-CSRFToken': csrfToken,
    }})
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta del servidor:', data);
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
