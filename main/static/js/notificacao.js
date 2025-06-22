const sidebar = document.querySelector(".sidebar");
const notificacoes = document.querySelectorAll(".notificacao-container");

const ajustarMargem = () => {
    const larguraSidebar = sidebar.offsetWidth;
    notificacoes.forEach(el => {
        el.style.marginLeft = `${larguraSidebar + 20}px`;
    });
};

document.getElementById('searchInput').addEventListener('keyup', function () {
    const filtro = this.value.toLowerCase();
    const notificacoes = document.querySelectorAll('.notificacao-container');

    notificacoes.forEach(function (el) {
        const texto = el.textContent.toLowerCase();
        el.style.display = texto.includes(filtro) ? 'block' : 'none';
    });
});

document.querySelectorAll('.marcar-lida').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        const notificacao = this.closest('.notificacao');
        if (this.checked) {
        notificacao.classList.add('apagada');
        } else {
        notificacao.classList.remove('apagada');
        }
    });
});

document.getElementById('marcarTodasBtn').addEventListener('click', function () {
    document.querySelectorAll('.marcar-lida').forEach(function (checkbox) {
        checkbox.checked = true;
        checkbox.closest('.notificacao').classList.add('apagada');
    });
});

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("open");
}