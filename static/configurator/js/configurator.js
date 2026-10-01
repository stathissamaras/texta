const img = document.getElementById('preview');
const sel = {kentrika: 'white', plaina: 'white'};

document.querySelectorAll('.swatch').forEach(el => {
    el.addEventListener('click', () => {
        const zone = el.dataset.zone;
        document.querySelectorAll(`.swatch[data-zone="${zone}"]`)
                .forEach(s => s.classList.remove('border-dark', 'border-3'));
        el.classList.add('border-dark', 'border-3');
        sel[zone] = el.dataset.code;
        img.src = `eikona/${sel.kentrika}/${sel.plaina}/`;
    });
});

// ---- μεγεθυντικός φακός ----
const wrap = document.getElementById('zoom-wrap');
const lens = document.getElementById('zoom-lens');
const ZOOM = 3;

wrap.addEventListener('mouseleave', () => lens.style.display = 'none');

wrap.addEventListener('mousemove', e => {
    const r = img.getBoundingClientRect();
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;
    const lw = lens.offsetWidth, lh = lens.offsetHeight;

    lens.style.backgroundImage = `url(${img.src})`;
    lens.style.backgroundSize = `${r.width * ZOOM}px ${r.height * ZOOM}px`;
    lens.style.backgroundPosition = `${lw / 2 - x * ZOOM}px ${lh / 2 - y * ZOOM}px`;
    lens.style.left = `${x - lw / 2}px`;
    lens.style.top = `${y - lh / 2}px`;
    lens.style.display = 'block';
});