from pydantic import BaseModel
from typing import List
from model.processo import Processo


class ProcessoSchema(BaseModel):
    """ Define como o número do processo a ser inserido e como deve ser representado
    """

    num_processo: str = "10050017120238190001"
    prazo: int = 10
    audiencia: str = "Instrução e Julgamento"
    status: str = "Reunião agendada"
    processo_relacionado: str = "0140040-01.2020.8.19.0201"
    patrono: str = "Dr. Hugo Nunes"
    
class ProcessoBuscaSchema(BaseModel):
    """ Define como será a estrutura que representa a busca por processo. Neste caso será feita apenas pelo número do processo"""

    num_processo: str = "10050017120238190001"

class ProcessoViewSchema(BaseModel):
    """ Define como um processo será retornado: processo + cliente.
    """

    num_processo: str = "10050017120238190001"
    prazo: int = 10
    audiencia: str = "Instrução e Julgamento"
    status: str = "Reunião agendada"
    processo_relacionado: str = "0140040-01.2020.8.19.0201"
    patrono: str = "Dr. Hugo Nunes"
    
class ListagemProcessoSchema(BaseModel):
    """ Define como a listagem de processo será retornada"""

    processos:List[ProcessoViewSchema]

def apresenta_processos(processos: List[Processo]):
    """ Retorna uma apresentação do processo seguindo o schema definido em ListagemProcessoSchema"""

    result = []
    for processo in processos:
        result.append({
            "Num_processo": processo.num_processo,
            "prazo": processo.prazo,
            "audiencia": processo.audiencia,
            "status": processo.status,
            "processo_relacionado": processo.processo_relacionado,
            "patrono": processo.patrono,
        })

    return {"processos": result}

class ProcessoDelSchema(BaseModel):
    """ Define como deve ser a extrutura dos dados retornado após uma requisição de remoção"""
    
    num_processo: str

def apresenta_processo (processo: Processo):
    """ Retorna uma representação do processo seguindo o schema definido em
        ProcessoViewSchema."""
    
    return {
        "num_processo": processo.num_processo,
        "prazo": processo.prazo,
        "audiencia": processo.audiencia,
        "status": processo.status,
        "processo_relacionado": processo.processo_relacionado,
        "patrono": processo.patrono
    }

