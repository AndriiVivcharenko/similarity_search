import os.path
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends

from app.config import settings
from app.di import Container
from app.models.query_response import QueryResponseModel, RestoreEmbeddingsResponseModel
from app.services.transformer_service import TransformerService
from app.services.vector_db_service import IVectorDBService
from app.utils.pdf_utils import chunk_text, clean_text, extract_text_from_pdf

router = APIRouter(
    prefix="/query",
    tags=["query"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@inject
async def get_query(
        q: Annotated[str | None, Query(max_length=50, description="Query string")],
        top_k: Annotated[int, Query(description="number of top results to return")] = 3,
        vectordb_service: IVectorDBService = Depends(Provide[Container.vectordb_service]),
        transformer_service: TransformerService = Depends(Provide[Container.transformer_service]),
) -> QueryResponseModel:
    """
    Returns top k results from a query
    """
    if q is None or q == "":
        raise HTTPException(status_code=403, detail="Query cannot be empty")

    try:
        return QueryResponseModel(
            query=q,
            matches=vectordb_service.query_index(
                embedded_text=transformer_service.embed_text(q).tolist(),
                top_k=top_k
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error {0}".format(
            str(e) if settings.is_dev() else ""
        ))


@router.post("/restore_embeddings")
@inject
async def restore_embeddings(
        vectordb_service: IVectorDBService = Depends(Provide[Container.vectordb_service]),
        transformer_service: TransformerService = Depends(Provide[Container.transformer_service]),
) -> RestoreEmbeddingsResponseModel:
    """
    Removes all embeddings from the database
    and adds new ones after reading the pdf file
    """

    if (not os.path.exists(settings.input_pdf_file) or
            not os.path.isfile(settings.input_pdf_file)):
        raise HTTPException(
            status_code=404,
            detail="Input pdf file does not exist"
        )

    try:
        pdf_text = extract_text_from_pdf(
            settings.input_pdf_file
        )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Error while extracting text from pdf file: {0}".format(
                                str(e) if settings.is_dev() else ""))

    try:
        processed_text = clean_text(pdf_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while cleaning text from pdf file: {0}".format(
            str(e) if settings.is_dev() else ""))

    try:
        chunks = chunk_text(processed_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while chunking text from pdf file: {0}".format(
            str(e) if settings.is_dev() else ""
        ))

    try:
        transformer_service.store_embeddings(
            chunks=chunks,
            vectordb_service=vectordb_service
        )

        return RestoreEmbeddingsResponseModel(
            number_of_embeddings=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Internal Server Error: {0}".format(
                                str(e) if settings.is_dev() else ""
                            ))
