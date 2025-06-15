import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymtrack.settings')
django.setup()

from main.models import Exercicio

lista_exercicios = [
    {'nome': 'Supino Reto com Barra', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Reto com Halteres', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Inclinado com Barra', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Inclinado com Halteres', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Declinado', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Crucifixo Reto', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Crucifixo Inclinado', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Pullover com Halter', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Crossover no Cabo', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Pec Deck (Voador)', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Máquina Reto', 'grupo': 'Peitoral', 'categoria': 'Superiores'},
    {'nome': 'Supino Máquina Inclinado', 'grupo': 'Peitoral', 'categoria': 'Superiores'},

    {'nome': 'Rosca Direta com Barra', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca Direta com Halteres', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca Alternada', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca Martelo', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca Concentrada', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca 21', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca Scott com Barra', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca na Polia Baixa', 'grupo': 'Bíceps', 'categoria': 'Superiores'},
    {'nome': 'Rosca na Máquina Scott', 'grupo': 'Bíceps', 'categoria': 'Superiores'},

    {'nome': 'Tríceps Testa com Barra', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Testa com Halteres', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Coice', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Francês', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Mergulho entre Bancos', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Pulley com Barra Reta', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Pulley com Corda', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Tríceps Unilateral na Polia', 'grupo': 'Tríceps', 'categoria': 'Superiores'},
    {'nome': 'Mergulho na Máquina', 'grupo': 'Tríceps', 'categoria': 'Superiores'},

    {'nome': 'Desenvolvimento com Barra', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Desenvolvimento com Halteres', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Desenvolvimento na Máquina', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Elevação Lateral com Halteres', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Elevação Lateral no Cabo', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Elevação Frontal com Halteres', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Elevação Posterior com Halteres', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Crucifixo Invertido na Máquina', 'grupo': 'Ombros', 'categoria': 'Superiores'},
    {'nome': 'Arnold Press', 'grupo': 'Ombros', 'categoria': 'Superiores'},

    {'nome': 'Remada Curvada com Barra', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Remada Unilateral com Halter', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Remada Cavalinho', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Remada Baixa na Polia', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Remada Alta na Polia', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Remada Máquina Hammer', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Puxada na Frente', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Puxada Atrás', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Puxada Supinada', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Barra Fixa (Pull-up)', 'grupo': 'Costas', 'categoria': 'Superiores'},
    {'nome': 'Chin-up', 'grupo': 'Costas', 'categoria': 'Superiores'},

    {'nome': 'Encolhimento de Ombros com Halteres', 'grupo': 'Trapézio', 'categoria': 'Superiores'},
    {'nome': 'Encolhimento de Ombros com Barra', 'grupo': 'Trapézio', 'categoria': 'Superiores'},
    {'nome': 'Remada Alta com Barra', 'grupo': 'Trapézio', 'categoria': 'Superiores'},

    {'nome': 'Rosca Inversa com Barra', 'grupo': 'Antebraço', 'categoria': 'Superiores'},
    {'nome': 'Rosca Punho com Halteres', 'grupo': 'Antebraço', 'categoria': 'Superiores'},

    {'nome': 'Agachamento Livre', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Agachamento no Smith', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Agachamento Frontal', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Leg Press 45°', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Leg Press Horizontal', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Cadeira Extensora', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Avanço com Halteres', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Avanço no Smith', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Passada Estacionária', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},
    {'nome': 'Agachamento Búlgaro', 'grupo': 'Quadríceps', 'categoria': 'Inferiores'},

    {'nome': 'Mesa Flexora', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Flexão de Joelhos em Pé', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Stiff com Halteres', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Stiff com Barra', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Peso Morto Romeno', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Glute Ham Raise', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},
    {'nome': 'Levantamento Terra (convencional)', 'grupo': 'Posterior de Coxa', 'categoria': 'Inferiores'},

    {'nome': 'Cadeira Abdutora', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},
    {'nome': 'Elevação Pélvica no Banco (Hip Thrust)', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},
    {'nome': 'Elevação Pélvica na Máquina', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},
    {'nome': 'Glúteo no Cabo', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},
    {'nome': 'Agachamento Sumo com Halteres', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},
    {'nome': 'Extensão de Quadril na Máquina', 'grupo': 'Glúteos', 'categoria': 'Inferiores'},

    {'nome': 'Cadeira Adutora', 'grupo': 'Adutores', 'categoria': 'Inferiores'},
    {'nome': 'Agachamento Sumo com Barra', 'grupo': 'Adutores', 'categoria': 'Inferiores'},

    {'nome': 'Cadeira Abdutora', 'grupo': 'Abdutores', 'categoria': 'Inferiores'},
    {'nome': 'Abdução de Quadril no Cabo', 'grupo': 'Abdutores', 'categoria': 'Inferiores'},
    {'nome': 'Abdução em Pé com Faixa Elástica', 'grupo': 'Abdutores', 'categoria': 'Inferiores'},

    {'nome': 'Elevação de Panturrilha em Pé', 'grupo': 'Panturrilhas', 'categoria': 'Inferiores'},
    {'nome': 'Elevação de Panturrilha Sentado', 'grupo': 'Panturrilhas', 'categoria': 'Inferiores'},
    {'nome': 'Elevação de Panturrilha na Leg Press', 'grupo': 'Panturrilhas', 'categoria': 'Inferiores'},
    {'nome': 'Gêmeos no Step com Peso Corporal', 'grupo': 'Panturrilhas', 'categoria': 'Inferiores'},
    {'nome': 'Panturrilha no Smith Machine', 'grupo': 'Panturrilhas', 'categoria': 'Inferiores'},

    {'nome': 'Abdominal Supra no Solo', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Supra na Máquina', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal com Corda no Cabo', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Infra com Pernas Elevadas', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Infra na Paralela', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Infra com Banco Inclinado', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Infra Suspenso na Barra Fixa', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Canivete', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Bicicleta', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal com Bola Suíça', 'grupo': 'Core', 'categoria': 'Core'},

    {'nome': 'Abdominal Oblíquo no Solo', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Oblíquo com Halter em Pé', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Oblíquo na Polia Baixa', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Twist Russo com Peso', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Abdominal Oblíquo na Prancha', 'grupo': 'Core', 'categoria': 'Core'},

    {'nome': 'Extensão Lombar no Solo', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Extensão Lombar no Banco Roman Chair', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Good Morning com Barra', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Superman no Solo', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Stiff com Peso Leve (foco lombar)', 'grupo': 'Core', 'categoria': 'Core'},

    {'nome': 'Prancha Frontal', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Prancha Lateral', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Prancha com Elevação de Braço e Perna', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Prancha com Bola Suíça', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Prancha no TRX', 'grupo': 'Core', 'categoria': 'Core'},

    {'nome': 'Mountain Climbers', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Escalador Cruzado', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Ab Roll com Roda Abdominal', 'grupo': 'Core', 'categoria': 'Core'},
    {'nome': 'Lançamento de Medicine Ball Rotacional', 'grupo': 'Core', 'categoria': 'Core'}
]

for item in lista_exercicios:
    Exercicio.objects.get_or_create(nome=item['nome'], grupo=item['grupo'], categoria=item['categoria'])

print("Importação finalizada.")
