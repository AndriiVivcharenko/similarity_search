from fastapi import FastAPI
from fastapi.params import Depends

from app.di import Container
from .dependencies import get_token_header
from .routers import queries

app = FastAPI(
    dependencies=[
        Depends(get_token_header)
    ],
)

app.include_router(queries.router)

container = Container()
container.wire(modules=[__name__])
container.wire(modules=["app.routers.queries"])
container.wire(modules=["app.services.pinecone_service"])
container.wire(modules=["app.services.qdrant_service"])
container.wire(modules=["app.services.vector_db_service"])
container.wire(modules=["app.services.transformer_service"])
