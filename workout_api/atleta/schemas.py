from pydantic import Field, PositiveFloat
from typing import Annotated, Optional

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchemas, OutMixin

class Atleta(BaseSchemas):
    nome: Annotated[str, Field(description="Nome do atleta", exemple="Joao", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", exemple="12345678900", max_length=11)] # type: ignore
    idade: Annotated[int, Field(description="Idade do atleta", exemple="36")] # type: ignore
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", exemple=125.5)] # type: ignore
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", exemple=1.93)] # type: ignore
    sexo: Annotated[str, Field(description="Sexo do atleta", exemple="M", max_length=1)] # type: ignore
    categoria: Annotated[CategoriaIn, Field(description='Categoria ')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='CT')]

class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchemas):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", exemple="Joao", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", exemple="36")] 