from pydantic import BaseModel, Field
from typing import List, Optional
from model.processo import Processo

class ProcessoSchema(BaseModel):
    num_processo: str = Field(..., json_schema_extra={"example": "10050017120238190001"})
    prazo: Optional[int] = Field(None, json_schema_extra={"example": 10})
    audiencia: Optional[str] = Field(None, json_schema_extra={"example": "Instrução e Julgamento"})
    status: Optional[str] = Field(None, json_schema_extra={"example": "Reunião agendada"})
    processo_relacionado: Optional[str] = Field(None, json_schema_extra={"example": "0140040-01.2020.8.19.0201"})
    patrono: Optional[str] = Field(None, json_schema_extra={"example": "Dr. Hugo Nunes"})

class ProcessoBuscaSchema(BaseModel):
    num_processo: str = Field(..., json_schema_extra={"example": "10050017120238190001"})

class ProcessoViewSchema(BaseModel):
    num_processo: str = Field(..., json_schema_extra={"example": "10050017120238190001"})
    prazo: Optional[int] = Field(None, json_schema_extra={"example": 10})
    audiencia: Optional[str] = Field(None, json_schema_extra={"example": "Instrução e Julgamento"})
    status: Optional[str] = Field(None, json_schema_extra={"example": "Reunião agendada"})
    processo_relacionado: Optional[str] = Field(None, json_schema_extra={"example": "0140040-01.2020.8.19.0201"})
    patrono: Optional[str] = Field(None, json_schema_extra={"example": "Dr. Hugo Nunes"})


class ListagemProcessoSchema(BaseModel):
    processos: List[ProcessoViewSchema] = Field(default=[], json_schema_extra={"example": [{
        "num_processo": "10050017120238190001",
        "prazo": 10,
        "audiencia": "Instrução e Julgamento",
        "status": "Reunião agendada",
        "processo_relacionado": "0140040-01.2020.8.19.0201",
        "patrono": "Dr. Hugo Nunes"
    }]})

def apresenta_processos(processos: List[Processo]):
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
    num_processo: str = Field(..., json_schema_extra={"example": "10050017120238190001"})

def apresenta_processo(processo: Processo):
    return {
        "num_processo": processo.num_processo,
        "prazo": processo.prazo,
        "audiencia": processo.audiencia,
        "status": processo.status,
        "processo_relacionado": processo.processo_relacionado,
        "patrono": processo.patrono
    }

