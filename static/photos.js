document.addEventListener("DOMContentLoaded", () => {
    const btnAgregarFoto = document.getElementById("agregarFoto");
    const contenedorFotos = document.getElementById("contenedorFotos");
    const MAX_FOTOS = 5;

    btnAgregarFoto.addEventListener("click", () => {
        const totalFotos = contenedorFotos.querySelectorAll("input[type='file']").length;

        if (totalFotos >= MAX_FOTOS) {
            alert("No puede agregar más de 5 fotos.");
            return;
        }


        const nuevoInput = document.createElement("input");
        nuevoInput.type = "file";
        nuevoInput.name = "foto[]";
        nuevoInput.accept = "image/*";

        contenedorFotos.insertBefore(document.createElement("br"), btnAgregarFoto);
        contenedorFotos.insertBefore(nuevoInput, btnAgregarFoto);
    });
});
