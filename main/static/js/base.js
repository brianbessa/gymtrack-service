function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

document.addEventListener("DOMContentLoaded", function () {
    const profileBtn = document.querySelector('.user');
    const container = document.querySelector('.container');
    const overlay = document.getElementById('profileOverlay');
    const closeBtn = document.getElementById('closeProfile');

    if (profileBtn) {
    profileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        container.classList.add('blurred');
        overlay.style.display = 'flex';
    });
    }

    if (closeBtn) {
    closeBtn.addEventListener('click', () => {
        container.classList.remove('blurred');
        overlay.style.display = 'none';
    });
    }
});

function enableEdit(button) {
    const container = button.closest('.info-item');
    const input = container.querySelector('.editable-field');
    input.removeAttribute('readonly');
    input.focus();

    input.addEventListener('blur', () => {
    input.setAttribute('readonly', true);
    saveField(input.dataset.field, input.value);
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        input.blur();
    }
    });
}

function saveField(fieldName, value) {
    fetch("{% url 'atualizar_perfil' %}", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({ field: fieldName, value: value }),
    })

    .then(response => {
        if (!response.ok) throw new Error("Erro ao salvar.");
        return response.json();
    })

    .then(data => {
        console.log("Campo salvo com sucesso:", data);
    })

    .catch(error => {
        alert("Erro ao salvar campo.");
        console.error(error);
    });
}

function abrirEditorRestricoes(valor) {
    const input = document.getElementById('restricoesInput');
    input.value = valor;
    document.getElementById('restricoesModal').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('restricoesModal').style.display = 'none';
}

function salvarRestricoes() {
    const novaRestricao = document.getElementById('restricoesInput').value;

    fetch("{% url 'atualizar_perfil' %}", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({ field: "restricoes_alimentares", value: novaRestricao }),
    })

    .then(response => {
        if (!response.ok) throw new Error("Erro ao salvar.");
        return response.json();
    })

    .then(data => {
        fecharModal();
        alert("Restrições salvas com sucesso!");
    })
    
    .catch(error => {
        alert("Erro ao salvar.");
        console.error(error);
    });
}