from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    restricoes_alimentares = models.TextField(blank=True, null=True)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    experiencia = models.CharField(max_length=50, choices=[
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ], null=True, blank=True)
    objetivo = models.CharField(max_length=50, choices=[
        ('Hipertrofia', 'Hipertrofia'),
        ('Emagrecimento', 'Emagrecimento'),
        ('Condicionamento', 'Condicionamento'),
    ], null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
class Nutricionista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crn = models.CharField(max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)
    valor_consulta = models.DecimalField(max_digits=6, decimal_places=2)
    chave_pix = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='nutricionistas/fotos/', null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return f'Nutricionista: {self.user.username}'

    def is_online(self):
        if self.last_seen:
            return (timezone.now() - self.last_seen).total_seconds() < 60
        return False

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.SET_NULL, null=True, blank=True)

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacao')
    titulo = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    mensagem = models.TextField()
    icone = models.CharField(max_length=10, default="🔔")
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.username}: {self.titulo}"
    
class Mensagem(models.Model):
    nutricionista = models.ForeignKey('Nutricionista', on_delete=models.CASCADE)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.user.username}"
    
class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class RegistroCarga(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    carga = models.DecimalField(max_digits=5, decimal_places=2)
    repeticoes = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    series = models.IntegerField(null=True, blank=True)

class Medicao(models.Model):
    PARTE_CORPO_CHOICES = [
        ('braco_direito', 'Braço Direito'),
        ('braco_esquerdo', 'Braço Esquerdo'),
        ('peito', 'Peitoral'),
        ('cintura', 'Cintura'),
        ('quadril', 'Quadril'),
        ('coxa_direita', 'Coxa Direita'),
        ('coxa_esquerda', 'Coxa Esquerda'),
        ('panturrilha_direita', 'Panturrilha Direita'),
        ('panturrilha_esquerda', 'Panturrilha Esquerda'),
        ('peso', 'Peso'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    parte_corpo = models.CharField(max_length=30, choices=PARTE_CORPO_CHOICES)
    valor_cm = models.DecimalField(max_digits=5, decimal_places=2)
    data_registro = models.DateTimeField(auto_now_add=True)

class TreinoPersonalizado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.IntegerField()
    repeticoes = models.IntegerField()

    class Meta:
        unique_together = ('user', 'tipo', 'exercicio')

    def __str__(self):
        return f"{self.user.username} - Treino {self.tipo} - {self.exercicio.nome}"

class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.PositiveSmallIntegerField() 
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação {self.nota} por {self.usuario}'
    
class PlanoNutricional(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    refeicao = models.CharField(max_length=100)  
    descricao = models.TextField()               
    criado_em = models.DateTimeField(auto_now_add=True)
    horario = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.refeicao} - {self.cliente}"