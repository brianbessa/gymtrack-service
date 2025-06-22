function abrirModal(elemento) {
  const parte = elemento.getAttribute("data-nome");
  const label = elemento.getAttribute("data-label");
  document.getElementById("tituloParte").innerText = `Registrar ${label}`;
  document.getElementById("parteCorpo").value = parte;
  document.getElementById("medicaoInput").value = '';
  document.getElementById("modalRegistro").style.display = "flex";
}

function fecharModal() {
  document.getElementById("modalRegistro").style.display = "none";
}

function filtrarPartes() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const cards = document.querySelectorAll(".card");

  cards.forEach(card => {
    const nome = card.getAttribute("data-nome").toLowerCase();
    if (nome.includes(input)) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
}

function filtrarTabela() {
  const input = document.getElementById("searchTabelaInput").value.toLowerCase();
  const linhas = document.querySelectorAll("tbody tr");

  linhas.forEach(linha => {
    const parte = linha.cells[0]?.innerText.toLowerCase() || "";
    linha.style.display = parte.includes(input) ? "" : "none";
  });
}

window.addEventListener('DOMContentLoaded', () => {
    const url = new URL(window.location.href);
    const scrollTarget = url.searchParams.get("scroll");

    if (scrollTarget === "tabela") {
        const tabela = document.getElementById("tabelaRegistros");
        if (tabela) {
        tabela.scrollIntoView({ behavior: "smooth" });
        }
    }
});