document.addEventListener("DOMContentLoaded", function () {
    // ... Aquí va el código de las gráficas ...

    const loginButton = document.getElementById("GuardarCambios");
    loginButton.addEventListener("click", guardarUsuario);
    

    function guardarUsuario() {
        const id = document.getElementById("id").value;
        const nombre = document.getElementById("nombre").value;
        const apellido_materno = document.getElementById("apellido_materno").value;
        const apellido_paterno = document.getElementById("apellido_paterno").value;
        const telefono_particular = document.getElementById("telefono_particular").value;
        const telefono_celular = document.getElementById("telefono_celular").value;
        const genero = document.getElementById("genero").value;
        const ultimo_grado_estudios = document.getElementById("ultimo_grado_estudios").value;
        const institucion = document.getElementById("institucion").value;
        const domicilio_calle = document.getElementById("domicilio_calle").value;
        const domicilio_numero_exterior = document.getElementById("domicilio_numero_exterior").value;
        const domicilio_numero_interior = document.getElementById("domicilio_numero_interior").value;
        const domicilio_codigo_postal = document.getElementById("domicilio_codigo_postal").value;

        const data = {
            id: id,
            nombre: nombre,
            apellido_materno: apellido_materno,
            apellido_paterno: apellido_paterno,
            telefono_particular: telefono_particular,
            telefono_celular: telefono_celular,
            genero: genero,
            ultimo_grado_estudios: ultimo_grado_estudios,
            institucion: institucion,
            domicilio_calle: domicilio_calle,
            domicilio_numero_exterior: domicilio_numero_exterior,
            domicilio_numero_interior: domicilio_numero_interior,
            domicilio_codigo_postal: domicilio_codigo_postal,
        };

        fetch(`/administracion/usuarios/editar/${id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error("Error al actualizar el usuario");
                }
            })
            .then((jsonData) => {
                if (jsonData.status === "success") {
                    Swal.fire({
                        title: "Éxito",
                        text: "Usuario actualizado con éxito",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                    }).then(() => {
                        location.reload(); // Recarga la página para mostrar los cambios
                    });
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "Error al actualizar el usuario",
                        icon: "error",
                        confirmButtonText: "Aceptar",
                    });
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                Swal.fire({
                    title: "Error",
                    text: "Error al actualizar el usuario",
                    icon: "error",
                    confirmButtonText: "Aceptar",
                });
            });
    }
});
