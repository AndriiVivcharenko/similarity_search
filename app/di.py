from dependency_injector import containers, providers

from app.services.qdrant_service import QDrantService
from app.services.transformer_service import TransformerService


class Container(containers.DeclarativeContainer):
    vectordb_service = providers.Singleton(QDrantService)
    # vectordb_service = providers.Singleton(PineconeService)
    transformer_service = providers.Singleton(TransformerService)
