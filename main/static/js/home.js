function calcularIMCeTMB() {
    const altura = parseFloat(document.getElementById('altura').value);
    const peso = parseFloat(document.getElementById('peso').value);
    const idade = parseInt(document.getElementById('idade').value);
    const sexo = document.getElementById('sexo').value;
    const atividade = parseFloat(document.querySelector('input[name="atividade"]:checked').value);

    if (!altura || !peso || !idade || !sexo) {
        alert("Preencha todos os campos!");
        return;
    }

    const alturaM = altura / 100;
    const imc = peso / (alturaM * alturaM);

    let tmb;
    if (sexo === "masculino") {
        tmb = 88.36 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade);
    } else {
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade);
    }

    const tmbTotal = tmb * atividade;

    let classificacao = "";
    let classeIMC = "";
    if (imc < 18.5) {
        classificacao = "Magreza (Grau 0)";
        classeIMC = "imc-magreza";
    } else if (imc < 25) {
        classificacao = "Normal (Grau 0)";
        classeIMC = "imc-normal";
    } else if (imc < 30) {
        classificacao = "Sobrepeso (Grau I)";
        classeIMC = "imc-sobrepeso";
    } else if (imc < 40) {
        classificacao = "Obesidade (Grau II)";
        classeIMC = "imc-obesidade";
    } else {
        classificacao = "Obesidade Grave (Grau III)";
        classeIMC = "imc-obesidade-grave";
    }

    const conteudo = `
        <strong>Resultado:</strong>
        <div class="resultado-linha">
            <span class="icone">✅</span>
            <b>IMC:</b>
            <span class="${classeIMC}">${imc.toFixed(2)} - ${classificacao}</span>
        </div>
        <div class="resultado-linha">
            <span class="icone">🔥</span>
            <b>TMB:</b> ${tmb.toFixed(2)} kcal/dia
        </div>
        <div class="resultado-linha">
            <span class="icone">🏃‍♂️</span>
            <b>Gasto Diário com Atividade:</b> ${tmbTotal.toFixed(2)} kcal/dia
        </div>
    `;

    document.getElementById('conteudoModal').innerHTML = conteudo;
    document.getElementById('modalResultado').style.display = 'block';
}

async function buscarAlimento() {
    const nome = document.getElementById('alimento').value;
    const quantidade = parseFloat(document.getElementById('quantidade').value) || 1;
    const tabela = document.getElementById('tabelaAlimento').querySelector("tbody");

    if (!nome) return alert("Digite um alimento!");

    tabela.innerHTML = "<tr><td colspan='2'>Buscando...</td></tr>";

    try {
        const res = await fetch(`/api/buscar-alimento/?nome=${nome}&quantidade=${quantidade}`);
        const data = await res.json();
        const alimento = data.items?.[0];

    if (!alimento) {
        tabela.innerHTML = "<tr><td colspan='2'>Alimento não encontrado</td></tr>";
        return;
    }

    tabela.innerHTML = `
        <tr><td>Calorias</td><td>${alimento.calories.toFixed(2)} kcal</td></tr>
        <tr><td>Carboidratos</td><td>${alimento.carbohydrates_total_g.toFixed(2)} g</td></tr>
        <tr><td>Proteínas</td><td>${alimento.protein_g.toFixed(2)} g</td></tr>
        <tr><td>Gorduras totais</td><td>${alimento.fat_total_g.toFixed(2)} g</td></tr>
        <tr><td>Gorduras saturadas</td><td>${alimento.fat_saturated_g.toFixed(2)} g</td></tr>
    `;
    } catch (err) {
        tabela.innerHTML = "<tr><td colspan='2'>Erro na busca</td></tr>";
        console.error(err);
    }
}

function fecharModal() {
    document.getElementById('modalResultado').style.display = 'none';
}