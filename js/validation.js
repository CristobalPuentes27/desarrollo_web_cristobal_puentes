document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formAviso");
  const contactarPor = document.getElementById("contactarPor");
  const extraContactos = document.getElementById("extraContactos");
  
  // ================= REDES SOCIALES DINÁMICAS =================
  contactarPor.addEventListener("change", () => {
  extraContactos.innerHTML = ""; 
  const seleccionadas = Array.from(contactarPor.querySelectorAll("input[type='checkbox']:checked"))
                             .map(opt => opt.value);

  seleccionadas.forEach(red => {
    const label = document.createElement("label");
    label.textContent = `ID o URL de ${red}: `;

    const input = document.createElement("input");
    input.type = "text";
    input.name = `contacto_${red}`;
    input.minLength = 4;
    input.maxLength = 50;

    extraContactos.appendChild(label);
    extraContactos.appendChild(input);
    extraContactos.appendChild(document.createElement("br"));
    extraContactos.appendChild(document.createElement("br"));
  });
});

  // ================= VALIDACIONES DEL FORMULARIO =================
  form.addEventListener("submit", (e) => {
    e.preventDefault(); // evitar envío real
    
    let errores = [];

    // Nombre
    const nombre = document.getElementById("nombre").value.trim();
    if (nombre.length < 3 || nombre.length > 200) {
      errores.push("El nombre debe tener entre 3 y 200 caracteres.");
    }

    // Email
    const email = document.getElementById("email").value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email) || email.length > 100) {
      errores.push("El correo no es válido (máximo 100 caracteres).");
    }

    // Teléfono (opcional, pero si lo llenan debe cumplir formato)
    const telefono = document.getElementById("telefono").value.trim();
    if (telefono !== "") {
      const telRegex = /^\+\d{3}\.\d{8,12}$/; // ejemplo: +569.12345678
      if (!telRegex.test(telefono)) {
        errores.push("El número de celular debe ser válido (+NNN.NNNNNNNN).");
      }
    }

    // Redes sociales (si existen inputs creados)
    const redesInputs = extraContactos.querySelectorAll("input[type='text']");
    redesInputs.forEach(input => {
      if (input.value.trim().length > 0 &&
          (input.value.length < 4 || input.value.length > 50)) {
        errores.push(`El campo ${input.name} debe tener entre 4 y 50 caracteres.`);
      }
    });

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

    // Fecha de entrega
    const fechaEntrega = document.getElementById("fechaEntrega").value;
    if (fechaEntrega === "") {
      errores.push("Debe ingresar una fecha de entrega.");
    }

    // Fotos
   const contenedorFotos = document.getElementById("contenedorFotos");
const listaFotos = document.getElementById("listaFotos");
const MAX_FOTOS = 5;

function actualizarListaFotos() {
  listaFotos.innerHTML = "";
  const inputs = contenedorFotos.querySelectorAll("input[type='file']");

  inputs.forEach((input, idx) => {
    if (input.files.length > 0) {
      const li = document.createElement("li");
      li.textContent = `Foto ${idx + 1}: ${input.files[0].name}`;
      listaFotos.appendChild(li);
    }
  });
}

function agregarNuevoInputSiCorresponde(input) {
  const inputs = contenedorFotos.querySelectorAll("input[type='file']");
  const total = inputs.length;

  // Si este input tiene archivo y aún no hemos llegado al máximo
  if (input.files.length > 0 && total < MAX_FOTOS) {
    const nuevoInput = document.createElement("input");
    nuevoInput.type = "file";
    nuevoInput.name = "foto[]";
    nuevoInput.accept = "image/*";

    // cada vez que cambie, actualiza lista y revisa si hay que crear otro input
    nuevoInput.addEventListener("change", (e) => {
      actualizarListaFotos();
      agregarNuevoInputSiCorresponde(e.target);
    });

    contenedorFotos.appendChild(document.createElement("br"));
    contenedorFotos.appendChild(nuevoInput);
  }
}

// enganchar el primer input
const primerInput = contenedorFotos.querySelector("input[type='file']");
primerInput.addEventListener("change", (e) => {
  actualizarListaFotos();
  agregarNuevoInputSiCorresponde(e.target);
});
    actualizarListaFotos();

    const totalFotos = contenedorFotos.querySelectorAll("input[type='file']").length;


    // ================= RESULTADO =================
    if (errores.length > 0) {
      alert("Errores encontrados:\n\n" + errores.join("\n"));
    } else {
      if (confirm("¿Está seguro que desea agregar este aviso de adopción?")) {
        alert("Hemos recibido la información de adopción, muchas gracias y suerte!");
        window.location.href = "index.html"; // volver a portada
      }
    }
  });
});
