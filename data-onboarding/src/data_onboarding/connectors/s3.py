




from minio import Minio


from data_onboarding.core import get_settings
from data_onboarding.observability import log

settings = get_settings()
class MinIOClient:
    ''' A singleton client for interacting with MinIO '''
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MinIOClient, cls).__new__(cls)

        cls._instance.client = Minio(
            endpoint=settings.secrets.minio_endpoint,
            access_key=settings.secrets.minio_access_key,
            secret_key=settings.secrets.minio_secret_key,
            secure=settings.secrets.minio_secure,
        )

        log.info("MinIO Client initialized")


def get_minio_client() -> Minio:
    return MinIOClient().client





