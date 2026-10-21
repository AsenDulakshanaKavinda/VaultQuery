

from data_onboarding.domain.acl import AclMapping, GroupHierarchy


class PolicyValidationError(Exception):
    pass

def validate_policy(mapping: AclMapping, hierarchy: GroupHierarchy, quarantine_group: str = "grp_quarantine") -> None:

    if quarantine_group not in hierarchy.groups:
        raise PolicyValidationError(f"Quarantine group '{quarantine_group}' missing from hierarchy")
    if quarantine_group in hierarchy.always_granted:
        raise PolicyValidationError("Quarantine group cannot be always_granted")
    if quarantine_group in hierarchy.role_claim_to_group.values():
        raise PolicyValidationError("Quarantine group cannot be mapped from a role")


    for g_name, g in hierarchy.groups.items():
        if quarantine_group in g.inherits:
            raise PolicyValidationError(f"Group '{g_name}' inherits from quarantine")
