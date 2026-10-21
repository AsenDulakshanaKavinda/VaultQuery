from jira import JIRA
from data_onboarding.core import get_settings
from data_onboarding.observability import log

settings = get_settings()

class JiraConnection:
    '''  A singleton class for managing Jira connections. '''
    _instance = None
    _jira = None

    def __new__(cls):
        server = settings.secrets.jira_server
        basic_auth = settings.secrets.jira_basic_auth
        token_auth = settings.secrets.jira_basic_auth

        if cls._instance is None:
            if not server or not (basic_auth or token_auth):
                raise ValueError("Jira server URL and authentication credentials must be provided for initial setup.")

            cls._instance = super(JiraConnection, cls).__new__(cls)

            if basic_auth:
                cls._jira = JIRA(server=server, basic_auth=basic_auth)
            elif token_auth:
                cls._jira = JIRA(server=server, token_auth=token_auth)

            log.info("Jira connection initialized successfully.")

        return cls._instance


    @property
    def client(self):
        ''' returns the active JIRA client instance.'''
        return self._jira
            









