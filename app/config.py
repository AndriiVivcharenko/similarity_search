from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pinecone
    pinecone_api_key: str = ""
    pinecone_index_name: str = "whitepaper-similarity"
    pinecone_spec_cloud: str = "aws"
    pinecone_spec_region: str = "us-east-1"
    pinecone_dimensions: int = 1024

    # pdf 
    input_pdf_file: str = "ai_adoption_framework_whitepaper.pdf"
    chunk_length: int = 200

    # hugging face 
    transformer_name: str = "intfloat/multilingual-e5-large"

    # qdrant 
    qdrant_host: str = "qdrant_db"
    qdrant_port: int = 6333
    qdrant_index_name: str = "whitepaper_similarity"

    # auth
    x_token: str = "super-secret-token"

    # config
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
