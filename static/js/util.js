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