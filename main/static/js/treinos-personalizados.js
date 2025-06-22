function mostrarTreino(treino) {
    const secoes = ['a', 'b', 'c'];
    secoes.forEach(sec => {
        document.getElementById('treino-' + sec).classList.remove('active');
        document.getElementById('btn-' + sec).classList.remove('active');
    });
    document.getElementById('treino-' + treino).classList.add('active');
    document.getElementById('btn-' + treino).classList.add('active');
}

function trocarExercicio(exercicioId, grupo, index, tipo) {
    console.log("Trocando:", { exercicioId, grupo, index, tipo });

    fetch(`/trocar-exercicio/?exercicio_id=${exercicioId}&grupo=${grupo}&index=${index}&tipo=${tipo}`)
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            location.reload();
        } else {
            console.error("Erro:", data.error);
            alert("Erro ao trocar exercício.\n" + data.error);
        }
        })
        .catch(error => {
        console.error("Erro inesperado:", error);
        alert("Erro ao trocar exercício (catch).");
        });
}

function enviarAvaliacao(nota) {
    fetch('/avaliar/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ nota: nota })
    }).then(res => {
        if (res.ok) {
        document.getElementById('avaliacao').style.display = 'none';
        }
    }).catch(error => {
        console.error("Erro ao enviar avaliação:", error);
    });
}

const objetivo = "{{ objetivo|lower }}";

const diasPorObjetivo = {
    hipertrofia: ["seg", "ter", "qua", "sex"],
    emagrecimento: ["seg", "ter", "qua", "qui", "sex", "sáb"],
    condicionamento: ["seg", "ter", "qui", "sex", "sáb"]
};

const diasAtivos = diasPorObjetivo[objetivo] || [];

diasAtivos.forEach(dia => {
    const cells = document.querySelectorAll(`.dia-${dia}`);
    cells.forEach(cell => cell.classList.add("dia-ativo"));
});