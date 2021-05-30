import settings
from jerry.client.kuna import KunaClient


def get_client(name: str):
    if name == 'kuna':
        return KunaClient(
            api_key=settings.KUNA_API_KEY,
            secret_key=settings.KUNA_SECRET_KEY,
        )
    else:
        ValueError(f'No such client {name}')