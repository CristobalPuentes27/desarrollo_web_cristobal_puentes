document.addEventListener("DOMContentLoaded", () => {
    const selectRegion = document.getElementById("select-region");
    const selectComuna = document.getElementById("select-comuna");

    fetch("/api/regiones")
        .then(res => res.json())
        .then(data => {
            // llenar regiones
            data.forEach(region => {
                const option = document.createElement("option");
                option.value = region.id;  // ID real
                option.textContent = region.nombre;
                selectRegion.appendChild(option);
            });

            // cambiar comunas al seleccionar una región
            selectRegion.addEventListener("change", () => {
                const regionId = parseInt(selectRegion.value);
                selectComuna.innerHTML = '<option value="">Seleccione una comuna</option>';

                if (!regionId) return;

                const regionSeleccionada = data.find(r => r.id === regionId);
                if (regionSeleccionada) {
                    regionSeleccionada.comunas.forEach(comuna => {
                        const opt = document.createElement("option");
                        opt.value = comuna.id;  // ID real
                        opt.textContent = comuna.nombre;
                        selectComuna.appendChild(opt);
                    });
                }
            });
        })
        .catch(err => {
            console.error("Error cargando regiones y comunas:", err);
        });
});
