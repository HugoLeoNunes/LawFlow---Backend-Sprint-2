from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cliente, Processo
from logger import logger
from schemas import *
from flask_cors import CORS

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
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo Cliente à base de dados."""

    cliente = Cliente(
        cpf=form.cpf,
        nome=form.nome,
        telefone=form.telefone,
        nome_social=form.nome_social,
        rg=form.rg,
        orgao_expeditor=form.orgao_expeditor,
        uf_doc=form.uf_doc,
        nacionalidade=form.nacionalidade,
        estado_civil=form.estado_civil,
        data_de_nascimento=form.data_de_nascimento,
        profissao=form.profissao,
        email=form.email,
        sexo=form.sexo,
        rua=form.rua,
        numero=form.numero,
        bairro=form.bairro,
        cidade=form.cidade,
        uf_endereco=form.uf_endereco,
        cep=form.cep,
        complemento=form.complemento)
    
    """Retorna uma representação dos clientes e processos associados."""

    logger.info(f"Adicionando cliente de cpf: '{cliente.cpf}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        # efetivando o camando de adição de novo cliente na tabela
        session.commit()
        logger.info(f"Adicionado o cpf do cliente: '{cliente.cpf}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo cpf já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.cpf}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso ocorra um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.cpf}', {error_msg}")
        return {"mesage": error_msg}, 400


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
          responses={"200": ProcessoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_processo(form: ProcessoSchema):
    """Adiciona um novo Processo à base de dados

    Retorna uma representação dos Processos.
    """
    
    processo = Processo(
        num_processo=form.num_processo,
        prazo=form.prazo,
        audiencia=form.audiencia,
        status=form.status,
        processo_relacionado=form.processo_relacionado,
        patrono=form.patrono
    )

    logger.info(f"Adicionando processo de número: '{processo.num_processo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando processo
        session.add(processo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado processo: %s"% processo)
        return apresenta_processo(processo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Processo de com o mesmo número já salvo na base :/"
        logger.warning(f"Erro ao adicionar processo '{processo.num_processo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo processo :/"
        logger.warning(f"Erro ao adicionar Processo '{processo.num_processo}', {error_msg}")
        return {"mesage": error_msg}, 400

    
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
    app.run(host='0.0.0.0', port=5000)