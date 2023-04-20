document.addEventListener("DOMContentLoaded", function () {

    // Agrega un evento a cada botón de editar de usuarios
    document.querySelectorAll("[id^=GuardarCambios]").forEach((button) => {
        button.addEventListener("click", () => {
            const id = button.id.replace("GuardarCambios", "");
            guardarUsuario(id);
        });
    });
    

    // Función para guardar los cambios de un usuario
    function guardarUsuario(id) {
        const userId = document.getElementById("id"+id).value;
        const nombre = document.getElementById("nombre"+id).value;
        const apellido_materno = document.getElementById("apellido_materno"+id).value;
        const apellido_paterno = document.getElementById("apellido_paterno"+id).value;
        const telefono_particular = document.getElementById("telefono_particular"+id).value;
        const telefono_celular = document.getElementById("telefono_celular"+id).value;
        const genero = document.getElementById("genero"+id).value;
        const ultimo_grado_estudios = document.getElementById("ultimo_grado_estudios"+id).value;
        const institucion = document.getElementById("institucion"+id).value;
        const domicilio_calle = document.getElementById("domicilio_calle"+id).value;
        const domicilio_numero_exterior = document.getElementById("domicilio_numero_exterior"+id).value;
        const domicilio_numero_interior = document.getElementById("domicilio_numero_interior"+id).value;
        const domicilio_codigo_postal = document.getElementById("domicilio_codigo_postal"+id).value;

        const data = {
            id: userId,
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

    // Agregamos eventos al boton para guardar administradores
    document.querySelectorAll("[id^=GuardarAdmin]").forEach((button) => {
        button.addEventListener("click", () => {
            const id = button.id.replace("GuardarAdmin", "");
            guardarAdmin(id);
        });
    });

    // Funcion para guardar los cambios de un administrador
    function guardarAdmin(id) {
        const userId = document.getElementById("id"+id).value;
        const nombre = document.getElementById("nombre"+id).value;
        const apellido_materno = document.getElementById("apellido_materno"+id).value;
        const apellido_paterno = document.getElementById("apellido_paterno"+id).value;
        const telefono_celular = document.getElementById("telefono_celular"+id).value;
        const nivel_acceso = document.getElementById("nivel_acceso"+id).value;

        const data = {
            id: userId,
            nombre: nombre,
            apellido_materno: apellido_materno,
            apellido_paterno: apellido_paterno,
            telefono_celular: telefono_celular,
            nivel_acceso: nivel_acceso,
        };

        fetch(`/administracion/administradores/editar/${id}`, {
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
                    throw new Error("Error al actualizar el administrador");
                }
            })
            .then((jsonData) => {
                if (jsonData.status === "success") {
                    Swal.fire({
                        title: "Éxito",
                        text: "Administrador actualizado con éxito",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                    }).then(() => {
                        location.reload(); // Recarga la página para mostrar los cambios
                    });
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "Error al actualizar el administrador",
                        icon: "error",
                        confirmButtonText: "Aceptar",
                    });
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                Swal.fire({
                    title: "Error",
                    text: "Error al actualizar el administrador",
                    icon: "error",
                    confirmButtonText: "Aceptar",
                });
            });
    }


});
