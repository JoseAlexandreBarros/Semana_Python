from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Categoria, Conta
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calculo_total, calcula_equilibrio_financeiro
from extrato.models import Valores
from django.db.models import Sum
from datetime import datetime
from contas.models import ContaPagar,ContaPaga




def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calculo_total(entradas, 'valor')
    total_saidas = calculo_total(saidas, 'valor')
    contas=Conta.objects.all()
    total_contas = calculo_total(contas,'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais=calcula_equilibrio_financeiro()

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    

    
    return render(request, 'home.html',{'contas':contas,'total_contas':total_contas, 'total_entradas':total_entradas, 'total_saidas':total_saidas,'percentual_gastos_essenciais':int(percentual_gastos_essenciais),'percentual_gastos_nao_essenciais':int(percentual_gastos_nao_essenciais),'contas_vencidas': len(contas_vencidas),'contas_vencimento':len(contas_proximas_vencimento)})

def gerenciar(request):
    contas=Conta.objects.all()
    categorias=Categoria.objects.all()
    total_contas = 0

    for conta in contas:
        total_contas += conta.valor
    
    return render(request,'gerenciar.html',{'contas':contas,'categorias':categorias,'total_contas':total_contas})

def cadastrar_banco(request):
    
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR,('Preencha corretamente'))
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()
    
    messages.add_message(request, constants.SUCCESS,('Preenchido corretamente'))
    return redirect('/perfil/gerenciar/')

def deletar_banco(request,id):
    
    conta=Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS,('Conta deletada'))
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']
    
    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})

