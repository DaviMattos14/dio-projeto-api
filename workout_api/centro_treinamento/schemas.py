from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchemas


class CentroTreinamentoIn(BaseSchemas):
    nome: Annotated[str, Field(description="Nome do Centro de Treinamento", exemple="CT Cariri", max_lenght=20)]
    endereco: Annotated[str, Field(description="Endereco do Centro de Treinamento", exemple="Largo do Machado, 89", max_lenght=60)]
    proprietario: Annotated[str, Field(description="Proprietário do Centro de Treinamento", exemple="Roberto Carlos", max_lenght=300)]

class CentroTreinamentoAtleta(BaseSchemas):
    nome: Annotated[str, Field(description="Nome CT", exemple="CT King", max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='identificador de CT')]