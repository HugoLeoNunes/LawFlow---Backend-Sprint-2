from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from model import Base

class Processo(Base):
    __tablename__ = 'processo'

    num_processo = Column (String(20), primary_key = True)
    cliente_cpf = Column(Float, ForeignKey('cliente.cpf'))
    prazo = Column (Integer)
    audiencia = Column (String)
    status = Column (String)
    processo_relacionado = Column (String)
    patrono = Column (String)

    # Definição do relacionamento entre o processo e um cliente.
    # Aqui está sendo definido a coluna 'cliente' que vai guardar
    # a referencia ao cpf do cliente, a chave estrangeira que relaciona
    # um cliente ao processo.

    cliente = relationship("Cliente", back_populates="processos")

    def __init__(self, num_processo, prazo, audiencia, status, processo_relacionado, patrono):
        
        """
        Cria um processo inerente a um cliente

        Arguments:
            num_processo: Número do processo
            prazo: prazo judiciaal para atravessar alguma peça ou qualquer outro decidido pela equipe
            audiencia: Data e tipo de audiência, caso exista
            status: status atual do processo
            processo_relacionado: Processos relacionados ao processo principal, normalmente processos de outras instâncias.
            Patrono: Patrono ou pessoa responsável pelo processo 
            Cabe, não olvidar, o relacionamento entre cliente e processo.
        """
        self.num_processo = num_processo
        self.prazo = prazo
        self.audiencia = audiencia
        self.status = status
        self.processo_relacionado = processo_relacionado
        self.patrono = patrono

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Processo.
        """
        return{
            "num_processo": self.num_processo,
            "prazo": self.prazo,
            "audiencia": self.audiencia,
            "status": self.status,
            "processo_relacionado": self.processo_relacionado,
            "patrono": self.patrono,
        }
    
    def __repr__(self):
        """
        Retorna uma representação do Processo em forma de texto.
        """
        return f"Process(num_processo='{self.num_processo}', prazo={self.prazo}, audiencia='{self.audiencia}', status='{self.status}', processo_relaionado='{self.processo_relacionado}', patrono='{self.patrono}')"