from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente

from schemas import ProcessoSchema


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido e como deve ser representado
    """
    cpf: float = 10010010050
    nome: str = "Jack Sparrow"
    telefone: Optional[int] = 999991111
    nome_social: str = "Captain Jack Sparrow"
    rg: str = "020.200.200-2"
    orgao_expeditor: str = "Royal Navy"
    uf_doc: str = "Ld"
    nacionalidade: str = "Inglês"
    estado_civil: str = "solteiro"
    data_de_nascimento: str = "29/02/1983"
    profissao: str = "Oficial de Marinha"
    email: str = "CaptainJackSaprrow@Nassau.io"
    sexo: str = "Masculino"
    rua: str = "rua da Acre"
    numero: str = "21"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf_endereco: str = "RJ"
    cep: str = "20081-000"
    complemento: str = "Porto Maravilha"
    

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas pelo CPF do cliente.
    """
    cpf: float = 10010010050

class ClienteBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita, neste caso, pelo noke do cliente."""
    
    termo: str = "Jack Sparrow"

class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + processos.
    """
    # Por hora apenas cliente no front end.
    cpf: float = 10010010050
    nome: str = "Jack Sparrow"
    telefone: Optional[int] = 999991111
    nome_social: str = "Xuxa"
    rg: str = "020.200.200-2"
    orgao_expeditor: str = "Royal Navy"
    uf_doc: str = "Ld"
    nacionalidade: str = "Inglês"
    estado_civil: str = "solteiro"
    data_de_nascimento: str = "29/02/1983"
    profissao: str = "Oficial de Marinha"
    email: str = "CaptainJackSaprrow@Nassau.io"
    sexo: str = "Masculino"
    rua: str = "rua da Acre"
    numero: str = "21"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf_endereco: str = "RJ"
    cep: str = "20081-000"
    complemento: str = "Porto Maravilha"
    processo: int = 10050017120238190001
    processos:List[ProcessoSchema]

class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteViewSchema]

def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "telefone": cliente.telefone,
            "nome_social": cliente.nome_social,
            "rg": cliente.rg,
            "orgao_expeditor": cliente.orgao_expeditor,
            "uf_doc": cliente.uf_doc,
            "nacionalidade": cliente.nacionalidade,
            "estado_civil": cliente.estado_civil,
            "data_de_nascimento": cliente.data_de_nascimento,
            "profissao": cliente.profissao,
            "email": cliente.email,
            "sexo": cliente.sexo,
            "rua": cliente.rua,
            "numero": cliente.numero,
            "bairro": cliente.bairro,
            "cidade": cliente.cidade,
            "uf_endereco": cliente.uf_endereco,
            "cep": cliente.cep,
            "complemento": cliente.complemento,
        })

    return {"clientes": result}

class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    cpf: float

def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """

    return {
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "nome_social": cliente.nome_social,
        "rg": cliente.rg,
        "orgao_expeditor": cliente.orgao_expeditor,
        "uf_doc": cliente.uf_doc,
        "nacionalidade": cliente.nacionalidade,
        "estado_civil": cliente.estado_civil,
        "data_de_nascimento": cliente.data_de_nascimento,
        "profissao": cliente.profissao,
        "email": cliente.email,
        "sexo": cliente.sexo,
        "rua": cliente.rua,
        "numero": cliente.numero,
        "bairro": cliente.bairro,
        "cidade": cliente.cidade,
        "uf_endereco": cliente.uf_endereco,
        "cep": cliente.cep,
        "complemento": cliente.complemento,
        "total_processos": len(cliente.processos),
        "processos": [{"texto": c.texto} for c in cliente.processos]
    }
