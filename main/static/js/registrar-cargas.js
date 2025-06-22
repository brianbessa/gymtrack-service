document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById('modalCarga');
  const titulo = document.getElementById('tituloExercicio');
  const exercicioIdInput = document.getElementById('exercicio_id');
  const seriesContainer = document.getElementById('seriesContainer');
  let contadorSerie = 0;

  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', async function (e) {
      e.preventDefault();
      const nome = this.querySelector('h3').innerText;
      const id = this.dataset.id;
      exercicioIdInput.value = id;
      titulo.innerText = nome;
      seriesContainer.innerHTML = "";
      contadorSerie = 0;

      await carregarSeriesAnteriores(id);

      adicionarSerie();
      modal.classList.add('show');
    });
  });

  async function carregarSeriesAnteriores(exercicioId) {
    try {
      const response = await fetch(`/listar-series/${exercicioId}/`);
      if (!response.ok) throw new Error("Erro ao buscar séries anteriores");

      const data = await response.json();
      seriesContainer.innerHTML = '';

      if (data.series.length > 0) {
        const divAntigas = document.createElement("div");
        divAntigas.innerHTML = "<h4>Histórico:</h4>";
        divAntigas.style.marginBottom = '20px';

        const tabela = document.createElement("table");
        tabela.className = "tabela-series";

        const thead = document.createElement("thead");
        thead.innerHTML = `
          <tr>
            <th>Carga (kg)</th>
            <th>Repetições</th>
            <th>Data</th>
            <th>Ações</th>
          </tr>
        `;
        tabela.appendChild(thead);

        const tbody = document.createElement("tbody");

        data.series.forEach(serie => {
          const tr = document.createElement("tr");
          tr.dataset.id = serie.id;

          tr.innerHTML = `
            <td>${serie.carga}</td>
            <td>${serie.repeticoes}</td>
            <td>${serie.data}</td>
            <td class="acoes">
              <button type="button" class="btn-acao editar-btn" title="Editar">
                <i class="fas fa-pen-to-square"></i>
              </button>
              <button type="button" class="btn-acao deletar-btn" title="Excluir">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          `;

          tbody.appendChild(tr);
        });

        tabela.appendChild(tbody);
        divAntigas.appendChild(tabela);
        seriesContainer.appendChild(divAntigas);
      }
    } catch (error) {
      console.error("Erro ao recarregar séries:", error);
    }
  }

  window.adicionarSerie = function () {
    contadorSerie++;
    const div = document.createElement('div');
    div.className = 'linha-serie';
    div.innerHTML = `
      <span class="num-serie">${contadorSerie}</span>
      <input type="number" name="carga_${contadorSerie}" placeholder="Carga (kg)" step="0.1">
      <input type="number" name="reps_${contadorSerie}" placeholder="Repetições" >
      <button type="button" onclick="removerSerie(this)" class="btn-remover">❌</button>
    `;
    seriesContainer.appendChild(div);
  }

  window.removerSerie = function (button) {
    const linha = button.parentElement;
    linha.remove();
    document.querySelectorAll('.linha-serie').forEach((linha, index) => {
      linha.querySelector('.num-serie').innerText = index + 1;
    });
    contadorSerie = document.querySelectorAll('.linha-serie').length;
  }

  window.fecharModal = function () {
    modal.classList.remove('show');
    seriesContainer.innerHTML = "";
    contadorSerie = 0;
  }

  window.filtrarCategoria = function () {
    const filtro = document.getElementById('filterSelect').value;
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
      const categoria = card.dataset.categoria;
      card.style.display = (filtro === 'Todos' || categoria === filtro) ? 'flex' : 'none';
    });
  }

  window.filtrarExercicios = function () {
    const input = document.getElementById("searchInput");
    const filtro = input.value.toLowerCase();
    const cards = document.querySelectorAll(".card");
    cards.forEach(card => {
      const titulo = card.querySelector("h3").textContent.toLowerCase();
      card.style.display = titulo.includes(filtro) ? "" : "none";
    });
  }

  document.getElementById('formCarga').addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = this;
    const formData = new FormData(form);

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
        body: formData
      });

      const data = await response.json();

      if (response.ok && data.status === "ok") {
        const exercicioId = exercicioIdInput.value;
        alert(data.mensagem);
        await carregarSeriesAnteriores(exercicioId);
        document.querySelectorAll('.linha-serie').forEach(linha => linha.remove());
        contadorSerie = 0;
        adicionarSerie();
      } else {
        alert("Erro ao salvar: " + data.mensagem);
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro ao salvar as cargas.");
    }
  });

  document.addEventListener("click", async function (e) {
    if (e.target.classList.contains("deletar-btn")) {
      const linha = e.target.closest("tr");
      const serieId = linha?.dataset?.id;
      if (!serieId) {
        console.warn("ID da série não encontrado.");
        return;
      }

      if (confirm("Deseja realmente deletar esta série?")) {
        try {
          const response = await fetch(`/deletar-serie/${serieId}/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
          });
          const data = await response.json();
          if (data.status === "ok") {
            linha.remove();
          } else {
            alert("Erro ao deletar: " + data.mensagem);
          }
        } catch (error) {
          console.error("Erro ao deletar série:", error);
        }
      }
    }

    if (e.target.classList.contains("editar-btn")) {
      const linha = e.target.closest("tr");
      const serieId = linha?.dataset?.id;
      if (!serieId) {
        console.warn("ID da série não encontrado.");
        return;
      }

      const cells = linha.querySelectorAll("td");
      const novaCarga = prompt("Nova carga (kg):", cells[0].textContent);
      const novasReps = prompt("Novas repetições:", cells[1].textContent);
      if (novaCarga !== null && novasReps !== null) {
        try {
          const formData = new FormData();
          formData.append("carga", novaCarga);
          formData.append("repeticoes", novasReps);
          const response = await fetch(`/editar-serie/${serieId}/`, {
            method: "POST",
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
          });
          const data = await response.json();
          if (data.status === "ok") {
            cells[0].textContent = novaCarga;
            cells[1].textContent = novasReps;
          } else {
            alert("Erro ao editar: " + data.mensagem);
          }
        } catch (error) {
          console.error("Erro ao editar série:", error);
        }
      }
    }
  });
});