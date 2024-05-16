import google
import google.auth.transport.requests
import google.oauth2.credentials
from google.auth import compute_engine


def idtoken_from_metadata_server(url: str) -> str:

    request = google.auth.transport.requests.Request()
    credentials = compute_engine.IDTokenCredentials(
        request=request, target_audience=url, use_metadata_identity_endpoint=True
    )

    credentials.refresh(request)
    return credentials.token
