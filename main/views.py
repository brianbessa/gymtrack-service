from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CadastroForm
from .models import Profile, Cliente, Nutricionista, Notificacao, Mensagem, Exercicio, RegistroCarga
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal, InvalidOperation
from django.utils.timezone import localtime

def home_view(request):
    return render(request, 'home.html')

def pagamento_view(request):
    return render(request, 'pagamento.html')

from .models import Nutricionista

def cadastro_nutricionista_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar_senha = request.POST.get('confirmar_senha')

        crn = request.POST.get('crn')
        data_nascimento = request.POST.get('data_nascimento')
        valor_consulta = request.POST.get('valor_consulta')
        chave_pix = request.POST.get('chave_pix')

        if password != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastro-nutricionista')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()

        Nutricionista.objects.create(
            user=user,
            crn=crn,
            data_nascimento=data_nascimento,
            valor_consulta=valor_consulta,
            chave_pix=chave_pix
        )

        messages.success(request, 'Nutricionista cadastrado com sucesso.')
        return redirect('login')

    return render(request, 'cadastro-nutricionista.html')

def notificacao_nutricionista_view(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_envio')
    return render(request, 'notificacao-nutricionista.html', {'notificacoes': notificacoes})

def registrar_cargas_view(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'registrar-cargas.html', {'exercicios': exercicios, 'active_tab': 'cargas'})

def registrar_medicoes_view(request):
    pch = [
        {'nome': 'Braço esquerdo'},
        {'nome': 'Braço direito'},
        {'nome': 'Cintura'},
        {'nome': 'Quadril'},
        {'nome': 'Coxa direita'},
        {'nome': 'Coxa esquerda'},
        {'nome': 'Panturrilha direita'},
        {'nome': 'Panturrilha esquerda'},
        {'nome': 'Tórax'},
        {'nome': 'Ombros'}
    ]

    return render(request, 'registrar-medicoes.html', {
        'pch': pch,
        'active_tab': 'medicoes',
    })

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                peso=form.cleaned_data.get('peso'),
                altura=form.cleaned_data.get('altura'),
                data_nascimento=form.cleaned_data.get('data_nascimento'),
                experiencia=form.cleaned_data.get('experiencia'),
                objetivo=form.cleaned_data.get('objetivo')
            )

            Cliente.objects.create(user=user)
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('pagamento')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, 'profile'):
                return redirect('notificacao')  
            else:
                return redirect('notificacao-nutricionista')  

    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def perfil_view(request):
    return render(request, 'perfil.html')

def plano_nutricional_view(request):
    return render(request, 'plano-nutricional.html')

def acompanhar_processo_view(request):
    return render(request, 'acompanhar-processo.html')

def treinos_personalizados_view(request):
    return render(request, 'treinos-personalizados.html')

def nutricionista_view(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = None

    if cliente and cliente.nutricionista:
        nutricionistas = [cliente.nutricionista]
    else:
        nutricionistas = Nutricionista.objects.all()

    return render(request, 'nutricionista.html', {
        'nutricionistas': nutricionistas,
        'cliente': cliente, 
    })

def clientes_view(request):
    nutricionista = Nutricionista.objects.get(user=request.user)
    clientes = Cliente.objects.filter(nutricionista=nutricionista)
    return render(request, 'clientes.html', {'clientes': clientes})

def confirmar_consulta(request, nutricionista_id):
    if request.method == 'POST':
        nutricionista = get_object_or_404(Nutricionista, id=nutricionista_id)
        cliente = get_object_or_404(Cliente, user=request.user)
        nome_cliente = cliente.user.get_full_name().strip() or cliente.user.username

        cliente.nutricionista = nutricionista
        cliente.save()

        Notificacao.objects.create(
            usuario=cliente.user,
            titulo='Contrato confirmado!',
            mensagem=f'Você agora está vinculado ao nutricionista {nutricionista.user.get_full_name() or nutricionista.user.username}. Em breve você receberá seu plano alimentar direto em Plano nutricional.'
        )

        Notificacao.objects.create(
            usuario=nutricionista.user,
            titulo=f'{nome_cliente} acabou de te contratar!',
            mensagem=f'''
                Agora é com você: analise o objetivo dele e monte uma dieta personalizada.<br><br>
                <strong>Essas são as informações do {nome_cliente}:</strong>
                <ul>
                    <li>Peso: {cliente.user.profile.peso} kg</li>
                    <li>Altura: {cliente.user.profile.altura} m</li>
                    <li>Experiência: {cliente.user.profile.experiencia}</li>
                    <li>Objetivo principal: {cliente.user.profile.objetivo}</li>
                </ul>
                <p>Se houver qualquer dúvida, entre em contato com o cliente: <strong>{cliente.user.email}</strong></p>
            '''
        )

        return redirect('notificacao')

    
@login_required
def meus_clientes(request):
    nutricionista = Nutricionista.objects.get(user=request.user)
    clientes = Cliente.objects.filter(nutricionista=nutricionista)
    return render(request, 'nutricionista/clientes.html', {'clientes': clientes})

def enviar_notificacao(request, cliente_id):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        mensagem = request.POST['mensagem']
        cliente = Cliente.objects.get(id=cliente_id)
        Notificacao.objects.create(titulo=titulo, mensagem=mensagem, cliente=cliente)
        return redirect('meus_clientes')
    
def minhas_notificacoes(request):
    cliente = Cliente.objects.get(user=request.user)
    notificacoes = Notificacao.objects.filter(cliente=cliente).order_by('-data_envio')
    return render(request, 'cliente/notificacoes.html', {'notificacoes': notificacoes})

@csrf_exempt
def atualizar_perfil(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        profile = request.user.profile

        if hasattr(profile, field):
            setattr(profile, field, value)
            profile.save()
            return JsonResponse({"status": "ok", "field": field, "value": value})

        return JsonResponse({"error": "Campo inválido."}, status=400)

    return JsonResponse({"error": "Método não permitido."}, status=405)

@login_required
def notificacao_view(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_envio')
    return render(request, 'notificacao.html', {'notificacao': notificacoes})

@login_required
def enviar_mensagem(request, cliente_id):
    cliente = get_object_or_404(Cliente, user__id=cliente_id)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        Notificacao.objects.create(
            usuario=cliente.user,
            titulo=titulo,
            mensagem=descricao,
        )

        return HttpResponseRedirect('/clientes?mensagem_enviada=1')
    
def registrar_cargas(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'registrar_cargas.html', {'exercicios': exercicios})

def salvar_carga(request):
    if request.method == "POST":
        exercicio_id = request.POST.get("exercicio_id")
        exercicio = get_object_or_404(Exercicio, id=exercicio_id)

        contador = 1
        while True:
            carga = request.POST.get(f"carga_{contador}")
            reps = request.POST.get(f"reps_{contador}")
            if not carga or not reps:
                break
            RegistroCarga.objects.create(
                usuario=request.user,
                exercicio=exercicio,
                carga=carga,
                repeticoes=reps
            )
            contador += 1

        return JsonResponse({"status": "ok", "mensagem": "Cargas salvas com sucesso!"})

    return JsonResponse({"status": "erro", "mensagem": "Método não permitido."}, status=405)

def listar_series(request, exercicio_id):
    series = RegistroCarga.objects.filter(
        usuario=request.user,
        exercicio_id=exercicio_id
    ).order_by('-data')

    data = []
    for s in series:
        try:
            carga = float(s.carga)  # assume que carga é Decimal no banco
        except (ValueError, TypeError, InvalidOperation):
            carga = 0  # ou pule esse registro com `continue`
        data.append({
            'id': s.id,
            'carga': carga,
            'repeticoes': s.repeticoes,
            'data': localtime(s.data).strftime('%d/%m/%Y %H:%M')
        })

    return JsonResponse({'series': data})

@csrf_exempt
def editar_serie(request, serie_id):
    if request.method == "POST":
        try:
            carga = request.POST.get("carga")
            repeticoes = request.POST.get("repeticoes")
            serie = RegistroCarga.objects.get(id=serie_id)
            serie.carga = carga
            serie.repeticoes = repeticoes
            serie.save()
            return JsonResponse({"status": "ok", "mensagem": "Série atualizada"})
        except RegistroCarga.DoesNotExist:
            return JsonResponse({"status": "erro", "mensagem": "Série não encontrada"})
    return JsonResponse({"status": "erro", "mensagem": "Requisição inválida"})

@csrf_exempt
def deletar_serie(request, serie_id):
    if request.method == "POST":
        try:
            serie = RegistroCarga.objects.get(id=serie_id)
            serie.delete()
            return JsonResponse({"status": "ok", "mensagem": "Série deletada"})
        except RegistroCarga.DoesNotExist:
            return JsonResponse({"status": "erro", "mensagem": "Série não encontrada"})
    return JsonResponse({"status": "erro", "mensagem": "Requisição inválida"})