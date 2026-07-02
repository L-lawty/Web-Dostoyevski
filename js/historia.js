// ── ACORDEÓN DE LA LÍNEA DE TIEMPO ───────────────────────
// A diferencia de los capítulos de los libros, aquí cada hito
// se abre/cierra de forma independiente (no cierra los demás),
// porque tiene más sentido poder comparar varias fechas a la vez.
function toggleHito(item) {
    const cuerpo = item.querySelector('.hito-cuerpo');
    const inner  = item.querySelector('.hito-cuerpo-inner');
    const abierto = item.classList.contains('abierto');

    if (abierto) {
        item.classList.remove('abierto');
        cuerpo.style.maxHeight = '0';
    } else {
        item.classList.add('abierto');
        cuerpo.style.maxHeight = inner.scrollHeight + 'px';
    }
}