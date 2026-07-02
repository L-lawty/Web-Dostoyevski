// ── TABS ────────────────────────────────────────────────
function cambiarTab(e, id) {
    document.querySelectorAll('.tabs-nav button').forEach(b => b.classList.remove('activo'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('activo'));
    e.target.classList.add('activo');
    document.getElementById('tab-' + id).classList.add('activo');
    // Ocultar cualquier detalle de personaje abierto al cambiar tab
    document.querySelectorAll('.personaje-detalle').forEach(d => d.classList.remove('activo'));
}

// ── PERSONAJES ───────────────────────────────────────────
function mostrarPersonaje(e, id) {
    const detalle = document.getElementById('detalle-' + id);
    const yaAbierto = detalle.classList.contains('activo');

    // Quitar activo de todas las cards y detalles
    document.querySelectorAll('.personaje-card').forEach(c => c.classList.remove('activo'));
    document.querySelectorAll('.personaje-detalle').forEach(d => d.classList.remove('activo'));

    if (!yaAbierto) {
        detalle.classList.add('activo');
        // Marcar la card correspondiente
        e.currentTarget.classList.add('activo');
        // Scroll suave al detalle
        detalle.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// ── ACORDEÓN DE CAPÍTULOS ────────────────────────────────
function toggleCapitulo(item) {
    const cuerpo = item.querySelector('.capitulo-cuerpo');
    const inner  = item.querySelector('.capitulo-cuerpo-inner');
    const abierto = item.classList.contains('abierto');

    // Cerrar todos primero
    document.querySelectorAll('.capitulo-item').forEach(i => {
        i.classList.remove('abierto');
        i.querySelector('.capitulo-cuerpo').style.maxHeight = '0';
    });

    // Si no estaba abierto, abrir este
    if (!abierto) {
        item.classList.add('abierto');
        cuerpo.style.maxHeight = inner.scrollHeight + 'px';
    }
}