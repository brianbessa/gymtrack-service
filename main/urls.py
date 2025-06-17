from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('notificacao/', views.notificacao_view, name='notificacao'),
    path('pagamento', views.pagamento_view, name='pagamento'),
    path('cadastro-nutricionista/', views.cadastro_nutricionista_view, name='cadastro-nutricionista'),
    path('notificacao-nutricionista/', views.notificacao_nutricionista_view, name='notificacao-nutricionista'),
    path('registrar-cargas/', views.registrar_cargas_view, name='registrar-cargas'),
    path('registrar-medicoes/', views.registrar_medicoes_view, name='registrar-medicoes'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('plano-nutricional/', views.plano_nutricional_view, name='plano-nutricional'),
    path('treinos-personalizados/', views.treinos_personalizados_view, name='treinos-personalizados'),
    path('acompanhar-processo/', views.acompanhar_processo_cargas_view, name='acompanhar-processo-cargas'),
    path('acompanhar-processo-medicoes/', views.acompanhar_processo_medicoes_view, name='acompanhar-processo-medicoes'),
    path('nutricionista/', views.nutricionista_view, name='nutricionista'),
    path('clientes', views.clientes_view, name='clientes'),
    path('atualizar-perfil/', views.atualizar_perfil, name='atualizar_perfil'),
    path('confirmar-consulta/<int:nutricionista_id>/', views.confirmar_consulta, name='confirmar_consulta'),
    path('nutricionista/enviar-notificacao/<int:cliente_id>/', views.enviar_notificacao, name='enviar_notificacao'),
    path('clientes/<int:cliente_id>/enviar-mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('registrar-cargas/', views.registrar_cargas, name='registrar-cargas'),
    path('salvar-carga/', views.salvar_carga, name='salvar_carga'),
    path('listar-series/<int:exercicio_id>/', views.listar_series, name='listar_series'),
    path('editar-serie/<int:serie_id>/', views.editar_serie, name='editar_serie'),
    path('deletar-serie/<int:serie_id>/', views.deletar_serie, name='deletar_serie'),
    path("grafico/cargas/<int:exercicio_id>/", views.grafico_cargas, name="grafico_cargas"),
    path("grafico/series-repeticoes/<int:exercicio_id>/", views.grafico_series_repeticoes, name="grafico_series_repeticoes"),
    path("grafico/medicoes/<str:parte_corpo>/", views.grafico_medicoes, name="grafico_medicoes"),
    path('api/buscar-alimento/', views.buscar_alimento_api, name='buscar_alimento_api'),
    path('trocar-exercicio/', views.trocar_exercicio_view, name='trocar_exercicio'),
    path('avaliar/', views.avaliar, name='avaliar'),
]
