document.addEventListener('DOMContentLoaded', function () {
    const inputPesquisa = document.getElementById('pesquisaNotificacoes');
    const notificacoes = document.querySelectorAll('.notificacao');

    inputPesquisa.addEventListener('input', function () {
        const termo = inputPesquisa.value.toLowerCase();

        notificacoes.forEach(function (notificacao) {
            const texto = notificacao.textContent.toLowerCase();
            if (texto.includes(termo)) {
                notificacao.style.display = 'flex';
            } else {
                notificacao.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const fileInputs = document.querySelectorAll('.upload-box input[type="file"]');

    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            const nomeArquivo = this.files.length > 0 ? this.files[0].name : 'Nenhum arquivo selecionado';
            const nomeSpan = this.closest('.upload-box').querySelector('.file-nome');
            nomeSpan.textContent = nomeArquivo;
        });
    });
});