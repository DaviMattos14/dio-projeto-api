from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchemas


class CategoriaIn(BaseSchemas):
    nome: Annotated[str, Field(description="Nome da categoria", exemple="Scale", max_lenght=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]