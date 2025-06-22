function openModal(id) {
    const modal = document.getElementById(`modal-${id}`);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(id) {
    const modal = document.getElementById(`modal-${id}`);
    if (modal) {
        modal.style.display = 'none';
    }
}

const searchInput = document.getElementById('searchInput');

searchInput.addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    const cards = document.querySelectorAll('.cards-container .card');

    cards.forEach(card => {
        const nome = card.querySelector('.nutricionista-nome').textContent.toLowerCase();
        if (nome.includes(filter)) {
        card.style.display = 'block';
        } else {
        card.style.display = 'none';
        }
    });
});