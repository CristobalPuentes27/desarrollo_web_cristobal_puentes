document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formAviso");
    const contactarPor = document.getElementById("contactarPor");
    const extraContactos = document.getElementById("extraContactos");
    const fechaEntrega = document.getElementById("fechaEntrega");
    
    const contenedorFotos = document.getElementById("contenedorFotos");

    // fecha actual + 3 horas
    const ahora = new Date();
    ahora.setHours(ahora.getHours());


    const fechaMinima = ahora.toISOString().slice(0, 16);
    fechaEntrega.value = fechaMinima;
    fechaEntrega.min = fechaMinima;

    // para las redes sociales
    contactarPor.addEventListener("change", () => {
        extraContactos.innerHTML = "";
        const checks = contactarPor.querySelectorAll("input[type='checkbox']");
        const seleccionadas = Array.from(contactarPor.querySelectorAll("input[type='checkbox']:checked"))
            .map(opt => opt.value);

        const yaSelecionada = Array.from(checks).filter(chk => chk.checked);

        if (yaSelecionada.length >= 5) {
            checks.forEach(chk => {
                if (!chk.checked) chk.disabled = true;
            });
        } else {

            checks.forEach(chk => chk.disabled = false);
        }
        seleccionadas.forEach(red => {
            const label = document.createElement("label");
            label.textContent = `ID o URL de ${red}: `;

            const input = document.createElement("input");
            input.type = "text";
            input.name = `contacto_${red}`;


            extraContactos.appendChild(label);
            extraContactos.appendChild(input);
            extraContactos.appendChild(document.createElement("br"));
            extraContactos.appendChild(document.createElement("br"));
        });

    });

    // Validacion
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        let errores = [];

        // Nombre
        const nombre = document.getElementById("nombre").value.trim();
        if (nombre.length < 3 || nombre.length > 200) {
            errores.push("El nombre debe tener entre 3 y 200 caracteres.");
        }

        // Email
        const email = document.getElementById("email").value.trim();
        const emailRegex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        if (!emailRegex.test(email) || email.length > 100) {
            errores.push("El correo no es válido (máximo 100 caracteres).");
        }
        // Teléfono (opcional)
        const telefono = document.getElementById("telefono").value.trim();
        if (telefono !== "") {
            const telRegex = /^\+\d{3}\.\d{8}$/;
            if (!telRegex.test(telefono)) {
                errores.push("El número de celular debe ser válido (+NNN.NNNNNNNN).");
            }
        }

        // Redes sociales 
        const seleccionadas = Array.from(contactarPor.querySelectorAll("input[type='checkbox']:checked"))
            .map(opt => opt.value);

        if (seleccionadas.length > 0) {
            seleccionadas.forEach(red => {
                const input = form.querySelector(`input[name="contacto_${red}"]`);
                if (!input || input.value.trim() === "") {
                    errores.push(`Debe ingresar un ID o URL válido para ${red}.`);
                } else if (input.value.length < 4 || input.value.length > 50) {
                    errores.push(`El contacto de ${red} debe tener entre 4 y 50 caracteres.`);
                }
            });
        }
        // Tipo de mascota
        const tipo = document.getElementById("tipo").value;
        if (tipo === "") {
            errores.push("Debe seleccionar un tipo de mascota.");
        }

        // Cantidad
        const cantidad = parseInt(document.getElementById("cantidad").value);
        if (isNaN(cantidad) || cantidad < 1) {
            errores.push("La cantidad debe ser un número entero mayor o igual a 1.");
        }

        // Edad
        const edad = parseInt(document.getElementById("edad").value);
        const unidadEdad = document.getElementById("unidadEdad").value;
        if (isNaN(edad) || edad < 1 || unidadEdad === "") {
            errores.push("Debe ingresar una edad válida y seleccionar la unidad.");
        }
        const fotos = contenedorFotos.querySelectorAll("input[type='file']");
        let algunaSeleccionada = false;
        fotos.forEach(f => {
            if (f.files.length > 0) algunaSeleccionada = true;
        });
        if (!algunaSeleccionada) {
            errores.push("Debe subir al menos una foto de la mascota.");
        }

        // Fecha de entrega

        if (fechaEntrega.value === "") {
            errores.push("Debe ingresar una fecha de entrega.");
        } else if (fechaEntrega.value < fechaEntrega.min) {
            errores.push("La fecha de entrega debe ser mayor o igual a la fecha mínima permitida.");
        }

        // Resultado
        if (errores.length > 0) {
    alert("Errores encontrados:\n\n" + errores.join("\n"));
} else {
    e.preventDefault(); // solo detenemos si es válido, para mostrar modal
    document.getElementById("modalConfirmacion").style.display = "block";

    document.getElementById("btnSi").onclick = () => {
        form.submit(); // ahora sí enviamos el formulario al backend Flask
    };

    document.getElementById("btnNo").onclick = () => {
        document.getElementById("modalConfirmacion").style.display = "none";
    };
}
    });

});
