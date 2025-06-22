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

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const filter = this.value.toLowerCase();
            const cards = document.querySelectorAll('.cards-container .card');

            cards.forEach(card => {
                const nome = card.querySelector('.nutricionista-nome').textContent.toLowerCase();
                card.style.display = nome.includes(filter) ? 'block' : 'none';
            });
        });
    }
});