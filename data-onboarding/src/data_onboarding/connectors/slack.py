from slack_sdk import WebClient

from data_onboarding.core import get_settings
from data_onboarding.observability import log

settings = get_settings()


class SlackConnection:
    """A singleton class for managing Slack connections."""

    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            if not settings.secrets.slack_token:
                raise ValueError("Slack Bot Token must be provided for initial setup.")

            cls._instance = super().__new__(cls)

            cls._client = WebClient(token=settings.secrets.slack_token)
            log.info("Slack connection initialized successfully.")

        return cls._instance

    @property
    def client(self):
        """Returns the active Slack WebClient instance."""
        return self._client
