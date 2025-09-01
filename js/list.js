// Diccionario de actividades
const actividades = [
    {
        Publicacion: "2025-08-18 12:00",
        Entrega: "2025-08-20 10:00",
        Comuna: "Puerto Montt",
        Sector: "Centro",
        Cantidad: 1,
        Tipo: "Gato",
        Edad: "1 año",
        Contacto: "Ana Torres",
        Fotos: ["https://http.cat/images/102.jpg"]
    },
    {
        Publicacion: "2025-08-17 19:00",
        Entrega: "2025-08-21 14:00",
        Comuna: "Ñuñoa",
        Sector: "Plaza Ñuñoa",
        Cantidad: 1,
        Tipo: "Perro",
        Edad: "2 años",
        Contacto: "Carlos Pérez",
        Fotos: ["https://http.dog/414.jpg"]
    },
    {
        Publicacion: "2025-08-16 09:30",
        Entrega: "2025-08-22 16:00",
        Comuna: "Puente Alto",
        Sector: "Los Aromos",
        Cantidad: 1,
        Tipo: "Gato",
        Edad: "1 año",
        Contacto: "Cristobal Puentes",
        Fotos: ["../data/kuro1.jpg", "../data/kuro2.jpg", "../data/kuro3.jpg"]
    },
    {
        Publicacion: "2025-08-15 11:15",
        Entrega: "2025-08-23 09:00",
        Comuna: "La Florida",
        Sector: "Vicuña Mackenna",
        Cantidad: 5,
        Tipo: "Gatos",
        Edad: "3 meses",
        Contacto: "María González",
        Fotos: ["https://images.pexels.com/photos/45170/kittens-cat-cat-puppy-rush-45170.jpeg?auto=compress&cs=tinysrgb&w=600"]
    },
    {
        Publicacion: "2025-08-14 14:45",
        Entrega: "2025-08-24 12:00",
        Comuna: "santiago",
        Sector: "Beauchef 851",
        Cantidad: 1,
        Tipo: "Perros",
        Edad: "10 meses",
        Contacto: "Michis Beauchef",
        Fotos: ["../data/michisbeauchef1.jpg", "../data/michisbeauchef2.jpg", "../data/michisbeauchef3.jpg", "../data/michisbeauchef4.jpg", "../data/michisbeauchef5.jpg"]
    }

];

function renderTabla() {
    const container = document.getElementById("tabla-container");
    container.innerHTML = "";

    let html = `<table border="1" cellspacing="0" cellpadding="6">
    <thead>
      <tr>
        <th>Fecha Publicación</th>
        <th>Fecha Entrega</th>
        <th>Comuna</th>
        <th>Cantidad</th>
        <th>Tipo</th>
        <th>Edad</th>
        <th>Contacto</th>
        <th>Cantidad de fotos</th>
      </tr>
    </thead>
    <tbody>`;

    actividades.forEach((act, index) => {
        html += `
      <tr onclick="mostrarDetalle(${index})" style="cursor:pointer;">
        <td>${act.Publicacion}</td>
        <td>${act.Entrega}</td>
        <td>${act.Comuna}</td>
        <td>${act.Cantidad}</td>
        <td>${act.Tipo}</td>
        <td>${act.Edad}</td>
        <td>${act.Contacto}</td>
        <td>${act.Fotos.length}</td>
      </tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;

    document.getElementById("tabla-container").style.display = "block";
    document.getElementById("detalle-container").style.display = "none";
}

// Mostrar detalle de un aviso
function mostrarDetalle(index) {
    const act = actividades[index];
    const detalle = document.getElementById("detalle-container");

    let html = `
    <h2>Detalle Aviso</h2>
    <p><strong>Fecha Publicación:</strong> ${act.Publicacion}</p>
    <p><strong>Fecha Entrega:</strong> ${act.Entrega}</p>
    <p><strong>Comuna:</strong> ${act.Comuna}</p>
    <p><strong>Sector:</strong> ${act.Sector}</p>
    <p><strong>Cantidad:</strong> ${act.Cantidad}</p>
    <p><strong>Tipo:</strong> ${act.Tipo}</p>
    <p><strong>Edad:</strong> ${act.Edad}</p>
    <p><strong>Contacto:</strong> ${act.Contacto}</p>
    <p><strong>Total Fotos:</strong> ${act.Fotos.length}</p>

    <div class="fotos">`;

    act.Fotos.forEach(f => {
        html += `<img src="${f}" alt="foto mascota" width="320" height="240" onclick="abrirModal('${f}')">`;
    });

    html += `</div>
    <br>
    <button onclick="renderTabla()">Volver al listado</button>
    <a href="index.html" class= "fakebutton">Volver a la portada</a>
  `;

    detalle.innerHTML = html;

    document.getElementById("tabla-container").style.display = "none";
    document.getElementById("detalle-container").style.display = "block";
}

// Modal de fotos
function abrirModal(src) {
    document.getElementById("imagenModal").src = src;
    document.getElementById("modal").style.display = "flex";
}

document.addEventListener("DOMContentLoaded", () => {
    renderTabla();

    // ahora sí, después que DOM existe
    document.getElementById("cerrarModal").addEventListener("click", () => {
        document.getElementById("modal").style.display = "none";
    });
});
