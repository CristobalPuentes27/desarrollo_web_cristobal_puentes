// Funciones para manejar comentarios
function cargarComentarios() {
    if (typeof avisoId === 'undefined') {
        console.error('avisoId no está definido');
        return;
    }
    
    fetch(`/aviso/${avisoId}/comentarios`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar comentarios');
            }
            return response.json();
        })
        .then(comentarios => {
            const lista = document.getElementById('lista-comentarios');
            if (!lista) return;
            
            lista.innerHTML = '';
            
            if (comentarios.length === 0) {
                lista.innerHTML = '<p>No hay comentarios aún. ¡Sé el primero en comentar!</p>';
                return;
            }
            
            comentarios.forEach(comentario => {
                const comentarioDiv = document.createElement('div');
                comentarioDiv.className = 'comentario-item';
                comentarioDiv.innerHTML = `
                    <div class="comentario-header">
                        <strong>${escapeHtml(comentario.nombre)}</strong>
                        <span class="comentario-fecha">${comentario.fecha}</span>
                    </div>
                    <div class="comentario-texto">${escapeHtml(comentario.texto)}</div>
                `;
                lista.appendChild(comentarioDiv);
            });
        })
        .catch(error => {
            console.error('Error al cargar comentarios:', error);
            const lista = document.getElementById('lista-comentarios');
            if (lista) {
                lista.innerHTML = '<p>Error al cargar los comentarios</p>';
            }
        });
}
// Agregar esta función nueva para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'success') {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    
    // Agregar al body
    document.body.appendChild(notificacion);
    
    // Mostrar con animación
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);
    
    // Ocultar automáticamente después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        // Remover del DOM después de la animación
        setTimeout(() => {
            if (notificacion.parentNode) {
                notificacion.parentNode.removeChild(notificacion);
            }
        }, 300);
    }, 3000);
}

// Modificar la función agregarComentario
function agregarComentario() {
    const form = document.getElementById('form-comentario');
    if (!form) return;
    
    const formData = new FormData(form);
    
    const datos = {
        nombre: formData.get('nombre'),
        texto: formData.get('texto')
    };
    
    // Validación del cliente
    if (!validarFormulario(datos)) {
        return;
    }
    
    // Limpiar errores anteriores
    limpiarErrores();
    
    fetch(`/aviso/${avisoId}/comentario`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            form.reset();
            cargarComentarios();
            // CAMBIO AQUÍ: Usar notificación en lugar de alert
            mostrarNotificacion('Comentario agregado exitosamente', 'success');
        } else {
            // CAMBIO AQUÍ: Usar notificación de error
            mostrarNotificacion(data.errores.join(', '), 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al enviar el comentario', 'error');
    });
}

// Modificar la función mostrarErrores para usar notificaciones
function mostrarErrores(errores) {
    errores.forEach(error => {
        mostrarNotificacion(error, 'error');
    });
}

function validarFormulario(datos) {
    let valido = true;
    
    if (datos.nombre.length < 3 || datos.nombre.length > 80) {
        mostrarError('nombre', 'El nombre debe tener entre 3 y 80 caracteres');
        valido = false;
    }
    
    if (datos.texto.length < 5) {
        mostrarError('texto', 'El comentario debe tener al menos 5 caracteres');
        valido = false;
    }
    
    return valido;
}


function limpiarErrores() {
    const errorElements = document.querySelectorAll('[id^="error-"]');
    errorElements.forEach(el => {
        el.textContent = '';
    });
}

function mostrarErrores(errores) {
    errores.forEach(error => {
        alert(`Error: ${error}`);
    });
}

function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return unsafe;
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Cargar comentarios al inicio
    cargarComentarios();
    
    // Manejar envío del formulario
    const form = document.getElementById('form-comentario');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            agregarComentario();
        });
    }
});