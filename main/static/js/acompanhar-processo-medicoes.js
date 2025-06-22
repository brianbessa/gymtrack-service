let chartInstance = null;

function renderMedicaoChart(labels, valores) {
  const ctx = document.getElementById('graficoMedicao').getContext('2d');
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Valor em cm',
        data: valores,
        borderColor: 'green',
        backgroundColor: 'rgba(0, 200, 0, 0.2)',
        tension: 0.3,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: 'Centímetros'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Data'
          }
        }
      }
    }
  });
}

function buscarMedicoes(parte) {
  fetch(`/grafico/medicoes/${parte}/`)
    .then(res => res.json())
    .then(data => {
      renderMedicaoChart(data.labels, data.valores);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("selectParte");
  buscarMedicoes(select.value);
  select.addEventListener("change", function () {
    buscarMedicoes(this.value);
  });
});