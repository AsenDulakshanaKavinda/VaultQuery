from office365.sharepoint.client_context import ClientContext

from data_onboarding.core import get_settings
from data_onboarding.observability import log

secrets = get_settings().secrets


class SharePointConnection:
    """A singleton class for managing SharePoint connections."""

    _instance = None
    _ctx = None

    def __new__(cls):
        if cls._instance is None:
            if not all(
                [
                    secrets.sharepoint_site_url,
                    secrets.sharepoint_tenant_name,
                    secrets.sharepoint_client_id,
                    secrets.sharepoint_client_secret,
                ]
            ):
                raise ValueError(
                    "SharePoint credentials and site URL must be provided for initial setup."
                )

            cls._instance = super().__new__(cls)

            cls._ctx = ClientContext(secrets.sharepoint_site_url).with_client_secret(
                secrets.sharepoint_tenant_name,
                secrets.sharepoint_client_id,
                secrets.sharepoint_client_secret,
            )

            log.info("sharePoint connection initialized successfully.")

        return cls._instance


@property
def ctx(self):
    """Returns the active SharePoint ClientContext."""
    return self._ctx
