from flask import json, render_template, request, redirect, flash, Response, Blueprint, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import locale

from api.service.GravacaoService import *
from api.service.ProgramaService import *
from api.service.ProducaoInternaService import *
from api.service.ClienteExternoService import *
from api.service.FuncionarioService import *

gravacaoBp = Blueprint("gravacaoBp", __name__)

# -------------------------
# Rotas
# -------------------------
@gravacaoBp.route('/')
def menu():
    return render_template('menu.html')

@gravacaoBp.route('/gravacoes', methods=['GET'])
def nova_gravacao():
    gravações = carregar_gravacoes()
    programa = carregar_programas()
    producaoInterna = carregar_estudio()
    clienteExterno = carregar_externas()
    funcionarios = carregar_funcionarios()

    return render_template('index.html', gravações=gravações, programa=programa, producaoInterna=producaoInterna, clienteExterno=clienteExterno, funcionarios=funcionarios)

@gravacaoBp.route('/gravacoes', methods=['POST'])
def adicionar():
    data = request.form.to_dict()
    
    # Chame o service e GUARDE o resultado que ele retorna
    resultado = inserir_gravacao(data)

    # Verifique se a operação foi bem-sucedida
    if resultado.get("success"):
        flash("Gravação adicionada com sucesso!", "success")
    else:
        # Se falhou, exiba a mensagem de erro exata que o service nos deu
        mensagem_erro = resultado.get("message", "Ocorreu um erro desconhecido ao salvar.")
        flash(f"Falha ao adicionar gravação: {mensagem_erro}", "error")
        
        # É uma boa prática redirecionar de volta para a página do formulário
        # para que o utilizador possa ver a mensagem de erro.
        return redirect('/gravacoes')

    return redirect('/gravacoes')

@gravacaoBp.route('/gravacoes/editar/<int:id>', methods=['GET'])
def editar(id):

    gravacao = carregar_gravacao(id)
    programa = carregar_programas()
    producaoInterna = carregar_estudio()
    clienteExterno = carregar_externas()
    funcionarios = carregar_funcionarios()

    return render_template("editar.html", gravacao=gravacao, programa=programa, producaoInterna=producaoInterna, clienteExterno=clienteExterno, funcionarios=funcionarios)

@gravacaoBp.route('/gravacoes/editar/<int:id>', methods=['POST'])
def atualizarGravacao(id):
    data = request.form.to_dict()

    atualizar_gravacao(id, data)

    return redirect('/gravacoes')

@gravacaoBp.route('/gravacoes/excluir/<int:id>', methods=['POST'])
def excluir(id):
    excluir_gravacao(id)

    return redirect('/gravacoes')

@gravacaoBp.route('/cronograma')
def visualizar_tudo():
    gravações = carregar_gravacoes()
    estudio = []
    externa = []

    hoje = datetime.now().date()

    for item in gravações:
        # Compara apenas a parte da data do timestamp da gravação com a data de hoje
        if item.data_hora.date() == hoje:
            if item.tipo == "Externa":
                externa.append(item)
            else: # 'Interna' e 'Ao Vivo' vão para a mesma tabela
                estudio.append(item)

    return render_template('cronograma.html', estudio=estudio, externa=externa)

@gravacaoBp.route('/relatorios')
def relatorios():
    gravações = carregar_gravacoes()
    total_horas_mes = defaultdict(float)
    total_horas_programa = defaultdict(float)

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')

    for g in gravações:
        if g.get('excluido') or 'duracao' not in g or 'data' not in g:
            continue
        
        try:
            duracao = int(g['duracao'])
            data_obj = datetime.strptime(g['data'], '%Y-%m-%d')
            mes_ano = data_obj.strftime('%B/%Y')
            programa = g['programa']
            
            total_horas_mes[mes_ano.capitalize()] += duracao / 60
            total_horas_programa[programa] += duracao / 60
        except (ValueError, TypeError):
            continue
            
    return render_template(
        'relatorios.html',
        total_horas_mes=dict(total_horas_mes),
        total_horas_programa=dict(total_horas_programa)
    )

@gravacaoBp.route('/exportar_relatorios/<tipo>')
def exportar_relatorios(tipo):
    gravações = carregar_gravacoes()
    total_horas_mes = defaultdict(float)
    total_horas_programa = defaultdict(float)

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')

    for g in gravações:
        if g.get('excluido') or 'duracao' not in g or 'data' not in g:
            continue
        
        try:
            duracao = int(g['duracao'])
            data_obj = datetime.strptime(g['data'], '%Y-%m-%d')
            mes_ano = data_obj.strftime('%B/%Y')
            programa = g['programa']
            
            total_horas_mes[mes_ano.capitalize()] += duracao / 60
            total_horas_programa[programa] += duracao / 60
        except (ValueError, TypeError):
            continue

    csv_data = "Relatório de Horas por Mês\n"
    csv_data += "Mês/Ano,Horas\n"
    for mes, horas in total_horas_mes.items():
        csv_data += f"{mes},{horas:.2f}\n"

    csv_data += "\nRelatório de Horas por Programa\n"
    csv_data += "Programa,Horas\n"
    for programa, horas in total_horas_programa.items():
        csv_data += f"{programa},{horas:.2f}\n"
    
    if tipo == 'csv':
        mimetype = 'text/csv'
        filename = 'relatorios_agregados.csv'
    elif tipo == 'xls':
        mimetype = 'text/csv'
        filename = 'relatorios_agregados.xls'
    else:
        return "Tipo de exportação inválido", 400

    response = Response(csv_data, mimetype=mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.charset = 'utf-8-sig'
    return response

@gravacaoBp.route('/exportar_detalhado/<tipo>')
def exportar_detalhado(tipo):
    gravações = carregar_gravacoes()
    headers = [
        "Tipo","Data","Turno","Programa","Funcionário","Horário","Duração (min)",
        "Criado por","Criado em","IP Criação","Última edição por","Data de edição","IP Edição",
        "Excluído","Excluído por","Data de exclusão","IP Exclusão"
    ]
    csv_data = ",".join(headers) + "\n"

    for g in gravações:
        linha = [
            g.get('tipo',''),
            g.get('data',''),
            g.get('turno',''),
            g.get('programa',''),
            g.get('funcionario',''),
            g.get('horario',''),
            str(g.get('duracao','')),
            g.get('criador',''),
            g.get('criado_em',''),
            g.get('ip_criacao',''),
            g.get('ultima_edicao_por',''),
            g.get('data_edicao',''),
            g.get('ip_edicao',''),
            "Sim" if g.get('excluido') else "Não",
            g.get('excluido_por',''),
            g.get('data_exclusao',''),
            g.get('ip_exclusao','')
        ]
        csv_data += ",".join(l.replace(",", " ") if isinstance(l, str) else l for l in linha) + "\n"

    if tipo == 'csv':
        mimetype = 'text/csv'
        filename = 'relatorios_detalhados.csv'
    elif tipo == 'xls':
        mimetype = 'text/csv'
        filename = 'relatorios_detalhados.xls'
    else:
        return "Tipo de exportação inválido", 400

    response = Response(csv_data, mimetype=mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.charset = 'utf-8-sig'
    return response