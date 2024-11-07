import torch
from transformers import AutoTokenizer, AutoModel

from app.config import settings
from app.services.vector_db_service import IVectorDBService


class TransformerService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(settings.transformer_name)
        self.model = AutoModel.from_pretrained(settings.transformer_name)

    def embed_text(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings[0].numpy()

    def store_embeddings(self, chunks, vectordb_service: IVectorDBService):
        try:
            vectordb_service.delete_all()
        except Exception as e:
            pass

        for chunk_id, text in enumerate(chunks):
            embedding = self.embed_text(text)
            vectordb_service.upsert(chunk_id, embedding, text)
