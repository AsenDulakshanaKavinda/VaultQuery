



from qdrant_client import models

from data_onboarding.acl.acl import UserContext

 
def build_acl_pre_filter(user_context: UserContext) -> models.Filter:
    """Build a pre-filter for Qdrant based on the user's access control list."""
    return models.Filter(
        should = [
            models.FieldCondition(
                key="allowed_groups",
                match=models.MatchAny(any=list(user_context.groups))
            )
        ]
    )

