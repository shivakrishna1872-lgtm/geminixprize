import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Google/GCP
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "mock-api-key")
    firebase_project_id: str = os.getenv("FIREBASE_PROJECT_ID", "antigravity-dev")
    
    # Pub/Sub
    pubsub_project_id: str = os.getenv("PUBSUB_PROJECT_ID", "antigravity-dev")
    pubsub_topic_id: str = os.getenv("PUBSUB_TOPIC_ID", "agy-events")
    
    # External APIs
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "mock")
    printify_api_key: str = os.getenv("PRINTIFY_API_KEY", "mock")
    duda_api_key: str = os.getenv("DUDA_API_KEY", "mock")
    commerce_layer_client_id: str = os.getenv("COMMERCE_LAYER_CLIENT_ID", "mock")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
