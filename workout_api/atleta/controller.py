from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
        '/',
        summary="Criar novo atleta",
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
)
async def post(
        db_session: DatabaseDependency, 
        atleta_in: AtletaIn = Body(...)
):
        categoria_name = atleta_in.categoria.nome
        centro_treinamento_name = atleta_in.centro_treinamento.nome
        categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()

        if not categoria:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail=f"Categoria não encontrada: {categoria_name}"
                )

        centro_treinamento = (
                await db_session.execute(
                        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name)
                        )
                ).scalars().first()
        if not centro_treinamento:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail=f"CT não encontrada: {centro_treinamento_name}"
                )
        
        try:
                        
                atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
                atlteta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
                atlteta_model.categoria_id = categoria.pk_id
                atlteta_model.centro_treinamento_id = centro_treinamento.pk_id
        except Exception:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"ERROR"
                )
        db_session.add(atlteta_model)
        await db_session.commit()

        return atleta_out

@router.get(
        '/',
        summary="Consultar todos Atletas",
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
        atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scallars().all()
        return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
        '/{id}',
        summary="Consultar um atleta pelo id",
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scallars().all()
        if not atleta:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"atleta não encontrado no id{id}"
                )
        return atleta

@router.patch(
        '/{id}',
        summary="Editar um atleta pelo id",
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body (...)) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scallars().all()
        if not atleta:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"atleta não encontrado no id{id}"
                )
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update.items():
                setattr(atleta,key,value)

        await db_session.commit()
        await db_session.refresh(atleta)
        return atleta


@router.delete(
        '/{id}',
        summary="Deletar um atleta pelo id",
        status_code=status.HTTP_204_NO_CONTENT
)
async def get(id: UUID4, db_session: DatabaseDependency) -> None:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scallars().all()
        if not atleta:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"atleta não encontrado no id{id}"
                )
        await db_session.delete(atleta)
        await db_session.commit(atleta)
