from pydantic import BaseModel, Field
from typing import Optional, List
from model.cliente import Cliente

class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido e como deve ser representado
    """
    cpf: float = Field(..., json_schema_extra={"example": 10010010050})
    nome: Optional[str] = Field(None, json_schema_extra={"example": "Jack Sparrow"})
    telefone: Optional[int] = Field(None, json_schema_extra={"example": 999991111})
    nome_social: Optional[str] = Field(None, json_schema_extra={"example": "Captain Jack Sparrow"})
    rg: Optional[str] = Field(None, json_schema_extra={"example": "020.200.200-2"})
    orgao_expeditor: Optional[str] = Field(None, json_schema_extra={"example": "Royal Navy"})
    uf_doc: Optional[str] = Field(None, json_schema_extra={"example": "Ld"})
    nacionalidade: Optional[str] = Field(None, json_schema_extra={"example": "Inglês"})
    estado_civil: Optional[str] = Field(None, json_schema_extra={"example": "solteiro"})
    data_de_nascimento: Optional[str] = Field(None, json_schema_extra={"example": "29/02/1983"})
    profissao: Optional[str] = Field(None, json_schema_extra={"example": "Oficial de Marinha"})
    email: Optional[str] = Field(None, json_schema_extra={"example": "CaptainJackSaprrow@Nassau.io"})
    sexo: Optional[str] = Field(None, json_schema_extra={"example": "Masculino"})
    rua: Optional[str] = Field(None, json_schema_extra={"example": "rua da Acre"})
    numero: Optional[str] = Field(None, json_schema_extra={"example": "21"})
    bairro: Optional[str] = Field(None, json_schema_extra={"example": "Centro"})
    cidade: Optional[str] = Field(None, json_schema_extra={"example": "Rio de Janeiro"})
    uf_endereco: Optional[str] = Field(None, json_schema_extra={"example": "RJ"})
    cep: Optional[str] = Field(None, json_schema_extra={"example": "20081-000"})
    complemento: Optional[str] = Field(None, json_schema_extra={"example": "Porto Maravilha"})
    

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas pelo CPF do cliente.
    """
    cpf: float = Field(..., json_schema_extra={"example": 10010010050})

class ClienteBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita, neste caso, pelo noke do cliente."""
    
    termo: str = Field(..., json_schema_extra={"example": "Jack Sparrow"})

class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + processos.
    """
    # Por hora apenas cliente no front end.
    cpf: float = Field(..., json_schema_extra={"example": 10010010050})
    nome: Optional[str] = Field(None, json_schema_extra={"example": "Jack Sparrow"})
    telefone: Optional[int] = Field(None, json_schema_extra={"example": 999991111})
    nome_social: Optional[str] = Field(None, json_schema_extra={"example": "Xuxa"})
    rg: Optional[str] = Field(None, json_schema_extra={"example": "020.200.200-2"})
    orgao_expeditor: Optional[str] = Field(None, json_schema_extra={"example": "Royal Navy"})
    uf_doc: Optional[str] = Field(None, json_schema_extra={"example": "Ld"})
    nacionalidade: Optional[str] = Field(None, json_schema_extra={"example": "Inglês"})
    estado_civil: Optional[str] = Field(None, json_schema_extra={"example": "solteiro"})
    data_de_nascimento: Optional[str] = Field(None, json_schema_extra={"example": "29/02/1983"})
    profissao: Optional[str] = Field(None, json_schema_extra={"example": "Oficial de Marinha"})
    email: Optional[str] = Field(None, json_schema_extra={"example": "CaptainJackSaprrow@Nassau.io"})
    sexo: Optional[str] = Field(None, json_schema_extra={"example": "Masculino"})
    rua: Optional[str] = Field(None, json_schema_extra={"example": "rua da Acre"})
    numero: Optional[str] = Field(None, json_schema_extra={"example": "21"})
    bairro: Optional[str] = Field(None, json_schema_extra={"example": "Centro"})
    cidade: Optional[str] = Field(None, json_schema_extra={"example": "Rio de Janeiro"})
    uf_endereco: Optional[str] = Field(None, json_schema_extra={"example": "RJ"})
    cep: Optional[str] = Field(None, json_schema_extra={"example": "20081-000"})
    complemento: Optional[str] = Field(None, json_schema_extra={"example": "Porto Maravilha"})

class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteViewSchema] = Field(default=[], json_schema_extra={"example": [{
        "cpf": 10010010050,
        "nome": "Jack Sparrow",
        "telefone": 999991111,
        "nome_social": "Xuxa",
        "rg": "020.200.200-2",
        "orgao_expeditor": "Royal Navy",
        "uf_doc": "Ld",
        "nacionalidade": "Inglês",
        "estado_civil": "solteiro",
        "data_de_nascimento": "29/02/1983",
        "profissao": "Oficial de Marinha",
        "email": "CaptainJackSaprrow@Nassau.io",
        "sexo": "Masculino",
        "rua": "rua da Acre",
        "numero": "21",
        "bairro": "Centro",
        "cidade": "Rio de Janeiro",
        "uf_endereco": "RJ",
        "cep": "20081-000",
        "complemento": "Porto Maravilha"
    }]})

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
    cpf: float = Field(..., json_schema_extra={"example": 10010010050})

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
        "total_processos": len(cliente.processos)
    }
