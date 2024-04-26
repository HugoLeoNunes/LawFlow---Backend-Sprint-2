from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from  model import Base, Processo


class Cliente(Base):
    __tablename__ = 'cliente'
    cpf = Column(Float, primary_key=True)
    nome = Column(String(140), unique=True)
    telefone = Column(Integer)
    nome_social = Column (String(140))
    rg = Column (String)
    orgao_expeditor = Column (String)
    uf_doc = Column (String)
    nacionalidade = Column(String)
    estado_civil = Column (String)
    data_de_nascimento = Column (String)
    profissao = Column (String)
    email = Column (String)
    sexo = Column (String)
    rua = Column (String)
    numero = Column (String)
    bairro = Column (String)
    cidade = Column (String)
    uf_endereco = Column (String)
    cep = Column (String)
    complemento = Column (String)

    # Definição do relacionamento entre o cliente e o processo.
    # Essa relação é implicita, não está salva na tabela 'cliente',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    processos = relationship("Processo")

    def __init__(self, cpf:float, nome:str, telefone:int, nome_social, rg, orgao_expeditor, uf_doc, nacionalidade, estado_civil, data_de_nascimento, profissao, email, sexo, rua, numero, bairro, cidade, uf_endereco, cep, complemento):
        """
        Cria um Cliente
        Arguments:
            cpf: cpf do cliente.
            nome: nome do Cliente.
            telefone: número de telefone do cliente
            nome_social: Nome conhecido pela sociedade, caso tenha
            rg: número do RG do cliente
            orgao_expeditor: Órgão Expeditor do RG do cliente
            uf_doc: UF de expedição do RG do cliente
            nacionalidade: Nacionalidade do cliente
            estado_civil: Estado civil do cliente
            data_de_nascimento: Data de nascimento do cliente
            profissão: Profissão do cliente
            email: e-mail do cliente
            sexo: Sexo do cliente
            rua: rua do cliente que poderá ser extraida de uma api externa através da consulta do cep.
            numero: número da casa do cliente (endereçõ)
            bairro: Bairro onde o cliente reside
            cidade: Cidade onde o cliente reside
            uf_endereco: UF do endereço do Cliente
            complemento: complemento do endereço

        """
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.nome_social = nome_social
        self.rg = rg
        self.orgao_expeditor = orgao_expeditor
        self.uf_doc = uf_doc
        self.nacionalidade = nacionalidade
        self.estado_civil = estado_civil
        self.data_de_nascimento = data_de_nascimento
        self.profissao = profissao
        self.email = email
        self.sexo = sexo
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.uf_endereco = uf_endereco
        self.cep = cep
        self.complemento = complemento

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Cliente.
        """
        return{
            "cpf": self.cpf,
            "nome": self.nome,
            "telefone": self.telefone,
            "nome_social": self.nome_social,
            "rg": self.rg,
            "orgao_expeditor": self.orgao_expeditor,
            "uf_doc": self.uf_doc,
            "nacionalidade": self.nacionalidade,
            "estado_civil": self.estado_civil,
            "data_de_nascimento": self.data_de_nascimento,
            "profissao": self.profissao,
            "email": self.email,
            "sexo": self.sexo,
            "rua": self.rua,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf_endereco": self.uf_endereco,
            "cep": self.cep,
            "complemento": self.complemento,
            "processos": [c.to_dict() for c in self.processos]
        }
    
    def __repr__(self):
        """
        Retorna uma representação do Cliente em forma de texto.
        """
        return f"Client(cpf={self.cpf}, nome='{self.nome}', telefone={self.telefone}, nome_social='{self.nome_social}', rg='{self.rg}', orgao_expeditor='{self.orgao_expeditor}', uf_doc='{self.uf_doc}', nacionalidade='{self.nacionalidade}',estado_civil='{self.estado_civil}', data_de_nascimento='{self.data_de_nascimento}', profissao='{self.profissao}', email='{self.email}', sexo='{self.sexo}', rua='{self.rua}', numero='{self.numero}', bairro='{self.bairro}', cidade='{self.cidade}', uf_endereco='{self.uf_endereco}', cep='{self.cep}', complemento='{self.complemento}')"
        
    def adiciona_processo(self, processo:Processo):
        """ Adiciona um novo processo ao cliente
        """
        self.processos.append(processo)
