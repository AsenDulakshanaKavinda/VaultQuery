from data_onboarding.acl.acl import (
    AclMapping,
    ChannelNameMatch,
    GroupHierarchy,
    PathPrefixMatch,
    ProjectKeyMatch,
)
from data_onboarding.acl.paths import (
    normalize_channel,
    normalize_path,
    normalize_project_key,
    path_has_prefix,
)


class PolicyValidationError(Exception):
    pass


def validate_policy(
    mapping: AclMapping,
    hierarchy: GroupHierarchy,
    quarantine_group: str = "grp_quarantine",
) -> None:
    """Validates the ACL policy against the group hierarchy and quarantine constraints."""

    # Validate quarantine group constraints
    if quarantine_group not in hierarchy.groups:
        raise PolicyValidationError(
            f"Quarantine group '{quarantine_group}' missing from hierarchy"
        )
    if quarantine_group in hierarchy.always_granted:
        raise PolicyValidationError("Quarantine group cannot be always_granted")
    if quarantine_group in hierarchy.role_claim_to_group.values():
        raise PolicyValidationError("Quarantine group cannot be mapped from a role")

    for g_name, g in hierarchy.groups.items():
        if quarantine_group in g.inherits:
            raise PolicyValidationError(f"Group '{g_name}' inherits from quarantine")

    # Validate that all always_granted groups are defined in the hierarchy
    defined_groups = set(hierarchy.groups.keys())
    for g_name in hierarchy.always_granted:
        if g_name not in defined_groups:
            raise PolicyValidationError(
                f"always_granted group '{g_name}' not defined in hierarchy"
            )

    # Validate that all role_claim_to_group mappings point to defined groups
    def detect_cycle(current: str, visited: set[str], path: list[str]):
        visited.add(current)
        path.append(current)
        grp = hierarchy.groups.get(current)
        if grp:
            for parent in grp.inherits:
                if parent not in defined_groups:
                    raise PolicyValidationError(
                        f"Group '{current}' inherits from undefined '{parent}'"
                    )
                if parent in path:
                    raise PolicyValidationError(
                        f"Inheritance cycle detected: {' -> '.join(path + [parent])}"
                    )
                if parent not in visited:
                    detect_cycle(parent, visited, path)
        path.pop()

    visited_nodes: set[str] = set()
    for grp_name in hierarchy.groups:
        if grp_name not in visited_nodes:
            detect_cycle(grp_name, visited_nodes, [])

    # Validate that all rule IDs are unique and that the source types are valid
    rule_ids = set()
    valid_sources = {
        "s3": PathPrefixMatch,
        "sharepoint": PathPrefixMatch,
        "slack": ChannelNameMatch,
        "jira": ProjectKeyMatch,
    }

    for rule in mapping.rules:
        if rule.id in rule_ids:
            raise PolicyValidationError(f"Duplicate rule ID: '{rule.id}'")
        rule_ids.add(rule.id)

        # Validate that the quarantine group is not granted
        if quarantine_group in rule.allowed_groups:
            raise PolicyValidationError(f"Rule '{rule.id}' grants quarantine group")

        # Validate that all allowed groups are defined
        for grp in rule.allowed_groups:
            if grp not in defined_groups:
                raise PolicyValidationError(
                    f"Rule '{rule.id}' references undefined group '{grp}'"
                )

        # Validate that the rule's match type is compatible with its source system
        expected_type = valid_sources.get(rule.source_system)
        if not expected_type or not isinstance(rule.match, expected_type):
            raise PolicyValidationError(
                f"Rule '{rule.id}' match type {type(rule.match).__name__} incompatible with source '{rule.source_system}'"
            )

        # Validate path prefixes
        if isinstance(rule.match, PathPrefixMatch):
            norm_p = normalize_path(rule.match.value)
            if norm_p == "/":
                raise PolicyValidationError(
                    f"Rule '{rule.id}' path prefix cannot be root '/'"
                )

    # Validate rule shadowing
    for i, rule_a in enumerate(mapping.rules):
        for rule_b in mapping.rules[:i]:
            if rule_a.source_system != rule_b.source_system:
                continue

            match_a, match_b = rule_a.match, rule_b.match
            if isinstance(match_a, PathPrefixMatch) and isinstance(
                match_b, PathPrefixMatch
            ):
                if path_has_prefix(
                    normalize_path(match_a.value), normalize_path(match_b.value)
                ):
                    raise PolicyValidationError(
                        f"Rule '{rule_a.id}' is shadowed by prior rule '{rule_b.id}'"
                    )

            elif isinstance(match_a, ChannelNameMatch) and isinstance(
                match_b, ChannelNameMatch
            ):
                set_a = {normalize_channel(c) for c in match_a.values}
                set_b = {normalize_channel(c) for c in match_b.values}
                if set_a.issubset(set_b):
                    raise PolicyValidationError(
                        f"Rule '{rule_a.id}' is shadowed by prior rule '{rule_b.id}'"
                    )

            elif isinstance(match_a, ProjectKeyMatch) and isinstance(
                match_b, ProjectKeyMatch
            ):
                set_a = {normalize_project_key(p) for p in match_a.values}
                set_b = {normalize_project_key(p) for p in match_b.values}
                if set_a.issubset(set_b):
                    raise PolicyValidationError(
                        f"Rule '{rule_a.id}' is shadowed by prior rule '{rule_b.id}'"
                    )
