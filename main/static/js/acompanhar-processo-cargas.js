let chartInstance = null;
let chartSeriesReps = null;

function renderChart(labels, data) {
const ctx = document.getElementById('graficoCargas').getContext('2d');
if (chartInstance) {
    chartInstance.destroy();
}

chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
    labels: labels,
    datasets: [{
        label: 'Carga (kg)',
        data: data,
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 123, 255, 0.2)',
        tension: 0.3,
        fill: true,
        pointRadius: 5,
        pointHoverRadius: 7
    }]
    },
    options: {
    responsive: true,
    scales: {
        y: {
        beginAtZero: true,
        title: {
            display: true,
            text: 'Carga (kg)'
        }
        },
        x: {
        title: {
            display: true,
            text: 'Data e Hora'
        }
        }
    },
    plugins: {
        legend: {
        display: true
        },
        title: {
        display: false
        }
    }
    }
});
}

function buscarDadosDoGrafico(exercicioId) {
fetch(`/grafico/cargas/${exercicioId}/`)
    .then(response => response.json())
    .then(data => {
    renderChart(data.labels, data.data);
    document.getElementById("cardMaxCarga").innerText = data.max_carga + " kg";
    document.getElementById("cardTotalReps").innerText = data.total_reps;
    document.getElementById("cardTotalSeries").innerText = data.total_series;

    const overview = `
        No exercício selecionado, você atingiu sua maior carga de <strong>${data.max_carga}kg</strong>${data.data_max_carga ? ` em ${data.data_max_carga}` : ""}.
        <br>
        Você realizou <strong>${data.total_reps}</strong> repetições em <strong>${data.total_series}</strong> séries.
        <br>
        Sua média de repetições por série é <strong>${data.media_reps_por_serie}</strong>.
        <br>
        A evolução da carga foi de <strong>${(data.min_carga > 0 ? Math.round(((data.max_carga - data.min_carga) / data.min_carga) * 100) : 0)}%</strong> desde a menor carga registrada.
    `;
    document.getElementById("overviewTexto").innerHTML = overview;
    });

fetch(`/grafico/series-repeticoes/${exercicioId}/`)
    .then(response => response.json())
    .then(data => {
    console.log("Dados recebidos para gráfico séries/reps:", data); 
    renderBarChart(data.labels, data.data);
    });

}

document.addEventListener("DOMContentLoaded", function () {
const exercicioSelect = document.getElementById("exercicioSelect");
const exercicioId = exercicioSelect.value;
buscarDadosDoGrafico(exercicioId);

exercicioSelect.addEventListener("change", function () {
    buscarDadosDoGrafico(this.value);
});
});

function renderBarChart(labels, data) {
const ctx = document.getElementById('graficoSeriesReps').getContext('2d');
if (chartSeriesReps) {
    chartSeriesReps.destroy();
}

chartSeriesReps = new Chart(ctx, {
    type: 'bar',
    data: {
    labels: labels,
    datasets: [{
        label: 'Total de repetições por dia',
        data: data,
        backgroundColor: 'rgba(40, 167, 69, 0.6)',
        borderColor: 'rgba(40, 167, 69, 1)',
        borderWidth: 1
    }]
    },
    options: {
    responsive: true,
    scales: {
        y: {
        beginAtZero: true,
        title: {
            display: true,
            text: 'Repetições'
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