from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask import request, jsonify
from pydantic import ValidationError
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cliente, Processo
from logger import logger
from schemas import *
from flask_cors import CORS

import tracemalloc
tracemalloc.start()

info = Info(title="API LawFlow", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)



# definindo tags
home_tag = Tag(name="Documentação LawFlow", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de clientes à base")
processo_tag = Tag(name="Processos", description="Adição, visualização e remoção de processos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": {"model" : ClienteViewSchema}, "409": {"model": ErrorSchema}, "400": {"model": ErrorSchema}})

def add_cliente():
    """Adiciona um novo Cliente à base de dados."""

    data = request.json if request.json is not None else request.form.to_dict()

    adjusted_data = {
        'cpf': data.get('cpf'),
        'nome': data.get('nome'),
        'telefone': int(data['telefone']) if data.get('telefone', '').isdigit() else None,
        'nome_social': data.get('nomeSocial'),
        'rg': data.get('rg'),
        'orgao_expeditor': data.get('orgaoExpeditor'),
        'uf_doc': data.get('ufDoc'),
        'nacionalidade': data.get('nacionalidade'),
        'estado_civil': data.get('estadoCivil'),
        'data_de_nascimento': data.get('dataDeNascimento'),
        'profissao': data.get('profissao'),
        'email': data.get('email'),
        'sexo': data.get('sexo'),
        'rua': data.get('rua'),
        'numero': data.get('numero'),
        'bairro': data.get('bairro'),
        'cidade': data.get('cidade'),
        'uf_endereco': data.get('ufEndereco'),
        'cep': data.get('cep'),
        'complemento': data.get('complemento'),
    }

    # Valida os dados ajustados com o esquema do Cliente
    try:
        form = ClienteSchema(**adjusted_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
    # Transformando a instância form de ClienteSchema em um dictionario
    cliente_data = form.model_dump()  # or form.to_dict() depending on the actual method available

    # Cria o objeto Cliente com o dicionário dos dados validados
    cliente = Cliente(**cliente_data)

    # Tenta adicionar o Cliente ao banco de dados
    with Session() as db:
        try:
            logger.info(f"Tentando adicionar cliente: {cliente}")
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            logger.info(f"Adicionado cliente: {cliente}")
            
            # cliente_serializado = ClienteSchema.dump(cliente)
            # Deserializa o objeto cliente para um dicionário
            cliente_serializado = cliente.to_dict()
            return jsonify(cliente_serializado), 200
            # return jsonify(ClienteSchema.dump(cliente)), 200
        except Exception as error:
            logger.error(f"Erro ao adicionar cliente: {error}")  # Logando a exceção específica
            db.rollback()
            if isinstance(error, IntegrityError):
                return jsonify({"error": "IntegrityError: O CPF do cliente já existe."}), 409
            else:
                return jsonify({"error": "Erro ao adicionar cliente"}), 500


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os Clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.info(f"perscrutando e reunindo clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.info(f"%d clientes econtrados" % len(clientes))
        # retorna a representação de cliente
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um Cliente a partir do cpf do cliente.

    Retorna uma representação dos clientes e processos associados.
    """
    cliente_cpf = query.cpf
    logger.info(f"Coletando dados sobre clientes #{cliente_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first()

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info(f"Cliente econtrado: '{cliente.nome}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um Cliente a partir do cpf de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_cpf = query.cpf
    logger.info(f"Deletando dados sobre o cliente selecionado #{cliente_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Cliente deletado #{cliente_cpf}")
        return {"mesage": "Cliente foi pro espaço", "cpf": cliente_cpf}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/busca_cliente', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def busca_cliente(query: ClienteBuscaNomeSchema):
    """Faz a busca por clientes em que o nome passando é pesquisado a partir do nome completo do cliente

    Retorna uma representação dos clientes e processos associados.
    """
    termo = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome com o termo: {termo}")
    # criando conexão com a base
    session = Session()
    # fazendo a consulta
    clientes = session.query(Cliente).filter(Cliente.nome.ilike(f"%{termo}%")).all()
    
    if not clientes:
        # se não há clientes cadastrados
        return {"cliente não encontrado": []}, 200
    else:
        logger.info(f"%d clientes econtrados" % len(clientes))
        # retorna a representação do cliente
        return apresenta_clientes(clientes), 200


@app.post('/processo', tags=[processo_tag],
          responses={"200": {"model": ProcessoViewSchema}, "409": {"model": ErrorSchema}, "400": {"model": ErrorSchema}})
def add_processo():
    """Adiciona um novo Processo à base de dados e retorna uma representação JSON do Processo."""
    # Tenta obter os dados da requisição
    data = request.json if request.json is not None else request.form.to_dict()
    
    # Prepara os dados ajustando conforme necessário
    adjusted_data = {
        'num_processo': data.get('numProcesso'),
        'prazo': int(data['prazo']) if data.get('prazo', '').isdigit() else None,
        'audiencia': data.get('audiencia') if isinstance(data.get('audiencia'), str) else None,
        'status': data.get('status') if isinstance(data.get('status'), str) else None,
        'processo_relacionado': data.get('processoRelacionado') if isinstance(data.get('processoRelacionado'), str) else None,
        'patrono': data.get('patrono') if isinstance(data.get('patrono'), str) else None,
    }
    
    # Valida os dados ajustados com o esquema do Processo
    try:
        form = ProcessoSchema(**adjusted_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Transformando a instância form de ProcessoSchema em um dictionario
    processo_data = form.model_dump()  # or form.to_dict() depending on the actual method available

    # Cria o objeto Processo com o dicionário dos dados validados
    processo = Processo(**processo_data)
    
    # Tenta adicionar o Processo ao banco de dados
    with Session() as db:
        try:
            logger.info(f"Tentando adicionar processo: {processo}")
            db.add(processo)
            db.commit()
            db.refresh(processo)
            logger.info(f"Adicionado processo: {processo}")
            
            # processo_serializado = ProcessoSchema.dump(processo)
            # Deserializa o objeto processo para um dicionário
            processo_serializado = processo.to_dict()
            return jsonify(processo_serializado), 200
            # return jsonify(ProcessoSchema.dump(processo)), 200
        except Exception as error:
            logger.error(f"Erro ao adicionar processo: {error}")  # Logando a exceção específica
            db.rollback()
            if isinstance(error, IntegrityError):
                return jsonify({"error": "IntegrityError: O número do processo já existe."}), 409
            else:
                return jsonify({"error": "Erro ao adicionar processo"}), 500
    
@app.get('/processos', tags=[processo_tag],
         responses={"200": ListagemProcessoSchema, "404": ErrorSchema})
def get_processos():
    """Faz a busca por todos os processos cadastrados

    Retorna uma representação da listagem dos processos.
    """
    logger.info(f"Pesquisando processos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    processos = session.query(Processo).all()

    if not processos:
        # se não há processos cadastrados
        return {"processos": []}, 200
    else:
        logger.info(f"%d processos econtrados" % len(processos))
        # retorna a representação de processo
        return apresenta_processos(processos), 200
    
@app.get('/processo', tags=[processo_tag],
         responses={"200": ProcessoViewSchema, "404": ErrorSchema})
def get_processo(query: ProcessoBuscaSchema):
    """Faz a busca por um Processo a partir do número do processo

    Retorna uma representação dos processos associados.
    """
    processo_num_processo = query.num_processo
    logger.info(f"Coletando dados sobre processos #{processo_num_processo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    processo = session.query(Processo).filter(Processo.num_processo == processo_num_processo).first()

    if not processo:
        # se o processo não foi encontrado
        error_msg = "Processo não encontrado na base :/"
        logger.warning(f"Erro ao buscar processo '{processo_num_processo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info("Processo econtrado: %s" % processo)
        # retorna a representação do processo
        return apresenta_processo(processo), 200
    
@app.delete('/processo', tags=[processo_tag],
            responses={"200": ProcessoDelSchema, "404": ErrorSchema})
def del_processo(query: ProcessoBuscaSchema):
    """Deleta um processo a partir do número do processo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    processo_num_processo = query.num_processo
    logger.info(f"Deletando dados sobre o processo selecionado #{processo_num_processo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Processo).filter(Processo.num_processo == processo_num_processo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Processo deletado #{processo_num_processo}")
        return {"mesage": "Processo deletado", "processo": processo_num_processo}
    else:
        # se o processo não foi encontrado
        error_msg = "Processo não encontrado na base :/"
        logger.warning(f"Erro ao deletar processo #'{processo_num_processo}', {error_msg}")
        return {"mesage": error_msg}, 404
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)