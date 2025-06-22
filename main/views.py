from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CadastroForm
from .models import Profile, Cliente, Nutricionista, Notificacao, Mensagem, Exercicio, RegistroCarga, Medicao, TreinoPersonalizado, Avaliacao, PlanoNutricional
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.http import HttpResponse
import json
import random
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal, InvalidOperation
from django.utils.timezone import localtime
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.urls import reverse
from datetime import datetime, timedelta, date
import requests
from django.conf import settings
from deep_translator import GoogleTranslator
from utils import gerar_qr_pix, processar_txt_inteligente
import re

def home_view(request):
    return render(request, 'home.html')

def pagamento_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    chave_pix = "exemplo@pix.com" 
    nome = user.first_name or user.username
    cidade = "Rio de Janeiro"
    valor = 49.90

    qr_code_base64 = gerar_qr_pix(chave_pix, nome, cidade, valor)

    numero_pedido = random.randint(1000000, 9999999)
    data_pedido = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    return render(request, 'pagamento.html', {
        'qr_code': qr_code_base64,
        'nome': nome,
        'email': user.email,
        'valor': valor,
        'numero_pedido': numero_pedido,
        'data_pedido': data_pedido,
    })

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

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Esse nome de usuário já existe. Experimente outro.'

        if User.objects.filter(email=email).exists():
            errors['email'] = 'Esse email já está em uso. Experimente outro.'

        if password != confirmar_senha:
            errors['confirmar_senha'] = 'As senhas não coincidem.'

        if data_nascimento:
            try:
                data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
                hoje = date.today()

                if data_nasc > hoje:
                    errors['data_nascimento'] = 'A data de nascimento não pode ser no futuro.'
                else:
                    idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
                    if idade > 120:
                        errors['data_nascimento'] = 'Data de nascimento inválida.'
                    if idade < 18:
                        errors['data_nascimento'] = 'Você deve ter pelo menos 18 anos para se cadastrar.'

            except ValueError:
                errors['data_nascimento'] = 'Data de nascimento inválida.'

        else:
            errors['data_nascimento'] = 'Por favor, informe sua data de nascimento.'

        CRN_REGEX = r'^\d{4,6}/[1-9]( [A-Z]{2})?$' 

        if not crn:
            errors['crn'] = 'O CRN é obrigatório.'
        else:
            if not re.match(CRN_REGEX, crn):
                errors['crn'] = 'CRN inválido. Formato esperado: 12345/5 ou 12345/5 SP.'

        if errors:
            return render(request, 'cadastro-nutricionista.html', {
                'form_data': request.POST,
                'errors': errors
            })

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

@login_required
def registrar_medicoes_view(request):
    pch = [
        {'value': 'braco_esquerdo', 'nome': 'Braço esquerdo'},
        {'value': 'braco_direito', 'nome': 'Braço direito'},
        {'value': 'cintura', 'nome': 'Cintura'},
        {'value': 'quadril', 'nome': 'Quadril'},
        {'value': 'coxa_direita', 'nome': 'Coxa direita'},
        {'value': 'coxa_esquerda', 'nome': 'Coxa esquerda'},
        {'value': 'panturrilha_direita', 'nome': 'Panturrilha direita'},
        {'value': 'panturrilha_esquerda', 'nome': 'Panturrilha esquerda'},
        {'value': 'peso', 'nome': 'Peso'}
    ]

    if request.method == 'POST':
        parte = request.POST.get('parteCorpo')
        valor = request.POST.get('medicaoInput')
        print("Parte:", parte)
        print("Valor:", valor)

        if parte and valor:
            nova_medicao = Medicao.objects.create(
                usuario=request.user,
                parte_corpo=parte,
                valor_cm=valor
            )
            print("Salvo:", nova_medicao)
            return redirect(f"{reverse('registrar-medicoes')}?scroll=tabela")

    medicoes = Medicao.objects.filter(usuario=request.user).order_by('-data_registro')

    return render(request, 'registrar-medicoes.html', {
        'pch': pch,
        'medicoes': medicoes,
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
            login(request, user)
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
    cliente = get_object_or_404(Cliente, user=request.user)
    planos = PlanoNutricional.objects.filter(cliente=cliente)

    ordem_refeicoes = [
        'café da manhã',
        'lanche da manhã',
        'almoço',
        'lanche da tarde',
        'jantar',
        'ceia'
    ]

    planos_ordenados = sorted(
        planos,
        key=lambda plano: ordem_refeicoes.index(plano.refeicao.lower())
        if plano.refeicao.lower() in ordem_refeicoes else len(ordem_refeicoes)
    )

    return render(request, 'plano-nutricional.html', {
        'planos': planos_ordenados,
    })

def acompanhar_processo_cargas_view(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'acompanhar-processo-cargas.html', {'exercicios': exercicios, 'active_tab': 'cargas'})

@login_required
def acompanhar_processo_medicoes_view(request):
    peso_medicoes = Medicao.objects.filter(
        usuario=request.user,
        parte_corpo='peso'
    ).order_by('-data_registro')

    return render(request, 'acompanhar-processo-medicoes.html', {
        'partes_corpo': Medicao.PARTE_CORPO_CHOICES,
        'peso_medicoes': peso_medicoes,
        'active_tab': 'medicoes',
    })

def selecionar_exercicios(grupo, quantidade):
    exercicios = list(Exercicio.objects.filter(grupo__iexact=grupo))
    random.shuffle(exercicios)
    return exercicios[:quantidade]

@transaction.atomic
def gerar_ou_obter_treino(user, tipo, configuracao):
    treino = TreinoPersonalizado.objects.filter(user=user, tipo=tipo)
    if treino.exists():
        return treino

    exercicios_selecionados = []
    for grupo, qtd in configuracao:
        exercicios_selecionados += selecionar_exercicios(grupo, qtd)

    treino_criado = []
    for ex in exercicios_selecionados:
        series = random.randint(2, 4)
        repeticoes = random.randint(6, 12)
        treino = TreinoPersonalizado.objects.create(
            user=user,
            tipo=tipo,
            exercicio=ex,
            series=series,
            repeticoes=repeticoes
        )
        treino_criado.append(treino)

    return treino_criado

def treinos_personalizados_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.profile
    objetivo = profile.objetivo.lower() 

    treino_a = gerar_ou_obter_treino(request.user, 'A', [
        ('peitoral', 3), ('tríceps', 2), ('ombros', 2)
    ])

    treino_b = gerar_ou_obter_treino(request.user, 'B', [
        ('costas', 3), ('bíceps', 2), ('trapézio', 1), ('antebraço', 1)
    ])

    treino_c = gerar_ou_obter_treino(request.user, 'C', [
        ('quadríceps', 3), ('posterior de coxa', 2), ('panturrilhas', 2)
    ])

    ja_avaliou = Avaliacao.objects.filter(usuario=request.user).exists()

    dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    context = {
        'objetivo': objetivo,
        'treino_a': treino_a,
        'treino_b': treino_b,
        'treino_c': treino_c,
        'ja_avaliou': ja_avaliou,
        'dias_semana': dias_semana
    }

    return render(request, 'treinos-personalizados.html', context)

def trocar_exercicio_view(request):
    try:
        grupo = request.GET.get('grupo')
        tipo = request.GET.get('tipo')
        index = request.GET.get('index')
        exercicio_id = request.GET.get('exercicio_id')

        if not grupo or not tipo or not index or not exercicio_id:
            return JsonResponse({'success': False, 'error': 'Parâmetros faltando'})

        index = int(index)
        exercicio_id = int(exercicio_id)
        user = request.user

        treino_queryset = TreinoPersonalizado.objects.filter(user=user, tipo=tipo)
        treino_list = list(treino_queryset)

        if index >= len(treino_list):
            return JsonResponse({'success': False, 'error': 'Índice fora do alcance'})

        ids_ja_usados = [t.exercicio.id for t in treino_list]

        exercicios_possiveis = list(
            Exercicio.objects.filter(grupo=grupo).exclude(id__in=ids_ja_usados)
        )

        if not exercicios_possiveis:
            return JsonResponse({'success': False, 'error': 'Nenhum exercício alternativo disponível'})

        novo_exercicio = random.choice(exercicios_possiveis)

        treino_list[index].exercicio = novo_exercicio
        treino_list[index].save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def nutricionista_view(request):
    try:
        cliente = Cliente.objects.select_related('nutricionista__user').get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = None

    if cliente and cliente.nutricionista:
        nutricionistas = [cliente.nutricionista]
    else:
        nutricionistas = Nutricionista.objects.select_related('user').all()

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
            cliente=cliente,
            titulo='Contrato confirmado!',
            mensagem=f'Você agora está vinculado ao nutricionista {nutricionista.user.get_full_name() or nutricionista.user.username}. Em breve você receberá seu plano alimentar direto em Plano nutricional.'
        )

        Notificacao.objects.create(
            usuario=nutricionista.user,
            cliente=cliente,
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

        try:
            if hasattr(request.user, 'nutricionista'):
                profile = request.user.nutricionista
            else:
                profile = request.user.profile
        except (Profile.DoesNotExist, Nutricionista.DoesNotExist):
            return JsonResponse({"error": "Perfil não encontrado."}, status=404)

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

        messages.success(request, 'mensagem_enviada')
        return redirect('clientes')

    return redirect('clientes')
    
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
            carga = float(s.carga)
        except (ValueError, TypeError, InvalidOperation):
            carga = 0  
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

@login_required
def grafico_cargas(request, exercicio_id):
    try:
        registros = RegistroCarga.objects.filter(usuario=request.user, exercicio_id=exercicio_id).order_by('data')

        if not registros.exists():
            return JsonResponse({
                'labels': [],
                'data': [],
                'max_carga': 0,
                'min_carga': 0,
                'total_reps': 0,
                'total_series': 0,
                'media_reps_por_serie': 0,
                'data_max_carga': None,
            })

        labels = [r.data.strftime("%d/%m %H:%M") for r in registros]
        data = [r.carga for r in registros]

        total_reps = sum(r.repeticoes for r in registros)
        total_series = registros.count()
        max_carga = max(r.carga for r in registros)
        min_carga = min(r.carga for r in registros)
        media_reps_por_serie = total_reps / total_series if total_series else 0

        data_max_carga = registros.filter(carga=max_carga).first()
        data_max_carga = data_max_carga.data.strftime("%d/%m") if data_max_carga else None

        return JsonResponse({
            'labels': labels,
            'data': data,
            'max_carga': max_carga,
            'min_carga': min_carga,
            'total_reps': total_reps,
            'total_series': total_series,
            'media_reps_por_serie': round(media_reps_por_serie, 1),
            'data_max_carga': data_max_carga,
        })

    except Exception as e:
        print("Erro na view grafico_cargas:", e)
        return JsonResponse({'erro': 'Erro interno no servidor'}, status=500)

@login_required
def grafico_series_repeticoes(request, exercicio_id):
    try:
        registros = (
            RegistroCarga.objects
            .filter(usuario=request.user, exercicio_id=exercicio_id)
            .exclude(data__isnull=True)
            .annotate(data_formatada=TruncDate('data'))
            .values('data_formatada')
            .annotate(total_reps=Sum('repeticoes'))
            .order_by('data_formatada')
        )

        labels = []
        data = []

        for r in registros:
            data_formatada = r.get('data_formatada')
            try:
                labels.append(data_formatada.strftime('%d/%m'))
            except Exception as e:
                print(f"[ERRO] data: {data_formatada}, tipo: {type(data_formatada)}, erro: {e}")
                labels.append("Erro")
            data.append(r['total_reps'])

        return JsonResponse({'labels': labels, 'data': data})

    except Exception as e:
        print(f"Erro na view grafico_series_repeticoes: {e}")
        return JsonResponse({'erro': 'Erro ao gerar gráfico'}, status=500)

@login_required
def grafico_medicoes(request, parte_corpo):
    try:
        medicoes = Medicao.objects.filter(
            usuario=request.user,
            parte_corpo=parte_corpo
        ).order_by('data_registro')

        if not medicoes.exists():
            return JsonResponse({
                'labels': [],
                'valores': []
            })

        labels = [m.data_registro.strftime("%d/%m/%Y %H:%M") for m in medicoes]
        valores = [float(m.valor_cm) for m in medicoes]

        return JsonResponse({
            'labels': labels,
            'valores': valores
        })

    except Exception as e:
        print("Erro na view grafico_medicoes:", e)
        return JsonResponse({'erro': 'Erro interno'}, status=500)
    
@csrf_exempt
def buscar_alimento_api(request):
    nome = request.GET.get('nome')
    quantidade = request.GET.get('quantidade', 1)

    if not nome:
        return JsonResponse({'error': 'Nome do alimento não fornecido'}, status=400)

    try:
        nome_em_ingles = GoogleTranslator(source='pt', target='en').translate(nome)
    except Exception as e:
        return JsonResponse({'error': f'Erro na tradução: {str(e)}'}, status=500)

    headers = {
        'X-Api-Key': settings.CALORIE_NINJAS_API_KEY
    }
    url = f'https://api.calorieninjas.com/v1/nutrition?query={quantidade} {nome_em_ingles}'

    try:
        response = requests.get(url, headers=headers)
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def avaliar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nota = data.get('nota')
        usuario = request.user if request.user.is_authenticated else None

        if usuario and Avaliacao.objects.filter(usuario=usuario).exists():
            return JsonResponse({'success': False, 'message': 'Usuário já avaliou.'})

        Avaliacao.objects.create(usuario=usuario, nota=nota)
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Método inválido'}, status=400)

def upload_plano_txt(request, cliente_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        arquivo = request.FILES.get('arquivo_txt')

        if arquivo and arquivo.name.endswith('.txt'):
            conteudo = arquivo.read().decode('utf-8')
            plano_dict = processar_txt_inteligente(conteudo)

            PlanoNutricional.objects.filter(cliente=cliente).delete()

            for refeicao, dados in plano_dict.items():
                descricao = '\n'.join(dados["alimentos"])
                PlanoNutricional.objects.create(
                    cliente=cliente,
                    refeicao=refeicao.title(),
                    descricao=descricao,
                    horario=dados["horario"]
                )

            messages.success(request, 'Plano nutricional importado com sucesso!')
        else:
            messages.error(request, 'Erro: envie um arquivo .txt válido.')

    return redirect('notificacao-nutricionista')

@login_required
def atualizar_foto(request):
    if request.method == 'POST' and request.FILES.get('foto'):
        nutricionista = request.user.nutricionista
        nutricionista.foto = request.FILES['foto']
        nutricionista.save()
        return redirect('notificacao-nutricionista')
    return JsonResponse({'erro': 'Requisição inválida'}, status=400)