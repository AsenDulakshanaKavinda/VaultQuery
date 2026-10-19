




from collections.abc import Sequence
from dataclasses import dataclass
import re

from data_onboarding.acl.errors import InvalidAclConfigError
from data_onboarding.acl.paths import normalize_channel, normalize_project_key, path_segments
from data_onboarding.domain.acl import GROUP_PATTERN, AclMapping, AclRule, ChannelNameMatch, GroupHierarchy, PathPrefixMatch, ProjectKeyMatch

_GROUP_RE = re.compile(GROUP_PATTERN)
_MATCH_SOURCES = {
    "path_prefix": {"s3", "sharepoint"},
    "channel_name": {"slack"},
    "project_key": {"jira"},
}


@dataclass(frozen=True)
class ShadowedRule:
    rule_id: str
    shadowed_by: str  # an earlier rule that already covers everything this rule matches


def validate_hierarchy(hierarchy: GroupHierarchy, quarantine_group: str) -> None:
    '''
    This function validates the group hierarchy and ensures that it adheres to the defined rules and constraints.
    It checks for the existence of the quarantine group, validates group names, checks for unknown groups, 
    ensures that the quarantine group is not always granted or inherited, and checks for inheritance cycles.
    '''
    groups = hierarchy.groups
    if quarantine_group not in groups:
        raise InvalidAclConfigError(f"quarantine group {quarantine_group!r} is not defined")
    for name in groups:
        if not _GROUP_RE.match(name):
            raise InvalidAclConfigError(f"group name {name!r} does not match {GROUP_PATTERN}")

    for g in hierarchy.always_granted:
        if g not in groups:
            raise InvalidAclConfigError(f"always_granted group {g!r} is not defined")
        if g == quarantine_group:
            raise InvalidAclConfigError("the quarantine group cannot be always_granted")

    for name, group in groups.items():
        for parent in group.inherits:
            if parent not in groups:
                raise InvalidAclConfigError(f"{name!r} inherits unknown group {parent!r}")
            if parent == quarantine_group:
                raise InvalidAclConfigError(f"{name!r} must not inherit the quarantine group")
            if parent == name:
                raise InvalidAclConfigError(f"{name!r} inherits itself")

    _reject_cycles(hierarchy)

    for role, target in hierarchy.role_claim_to_group.items():
        if target not in groups:
            raise InvalidAclConfigError(f"role {role!r} maps to unknown group {target!r}")
        if target == quarantine_group:
            raise InvalidAclConfigError(f"role {role!r} must not map to the quarantine group")


def _reject_cycles(hierarchy: GroupHierarchy) -> None:
    '''This function checks for inheritance cycles in the group hierarchy.'''
    WHITE, GREY, BLACK = 0, 1, 2
    state = dict.fromkeys(hierarchy.groups, WHITE)

    def visit(node: str, trail: list[str]) -> None:
        state[node] = GREY
        for parent in hierarchy.groups[node].inherits:
            if state[parent] == GREY:
                raise InvalidAclConfigError(
                    "inheritance cycle: " + " -> ".join([*trail, node, parent])
                )
            if state[parent] == WHITE:
                visit(parent, [*trail, node])
        state[node] = BLACK

    for g in hierarchy.groups:
        if state[g] == WHITE:
            visit(g, [])


def validate_rules(
    rules: Sequence[AclRule], known_groups: set[str], quarantine_group: str
) -> None:
    ''' 
    This function validates a sequence of ACL rules, 
    ensuring that each rule adheres to the defined constraints and that there are no duplicate rule IDs. 
    It checks for valid source systems, known groups, and ensures that the quarantine group is not granted by any rule. 
    Additionally, it validates the match values for each rule based on their type.    
    '''
    seen: set[str] = set()
    for r in rules:
        if r.id in seen:
            raise InvalidAclConfigError(f"duplicate rule id {r.id!r}")
        seen.add(r.id)

        if r.source_system not in _MATCH_SOURCES[r.match.type]:
            raise InvalidAclConfigError(
                f"rule {r.id!r}: match type {r.match.type!r} cannot apply to "
                f"source_system {r.source_system!r}"
            )
        unknown = set(r.allowed_groups) - known_groups
        if unknown:
            raise InvalidAclConfigError(f"rule {r.id!r} uses unknown groups: {sorted(unknown)}")
        if quarantine_group in r.allowed_groups:
            raise InvalidAclConfigError(f"rule {r.id!r} must not grant the quarantine group")

        try:
            m = r.match
            if isinstance(m, PathPrefixMatch):
                if not path_segments(m.value):
                    raise ValueError("prefix is the root and would match everything")
            elif isinstance(m, ChannelNameMatch):
                for v in m.values:
                    normalize_channel(v)
            elif isinstance(m, ProjectKeyMatch):
                for v in m.values:
                    normalize_project_key(v)
        except ValueError as exc:
            raise InvalidAclConfigError(f"rule {r.id!r}: {exc}") from exc


def _covers(earlier: AclRule, later: AclRule) -> bool:
    '''
    This function checks if an earlier ACL rule covers a later ACL rule, 
    meaning that the earlier rule matches all the cases that the later rule would match.
    '''
    a, b = earlier.match, later.match
    if earlier.source_system != later.source_system or type(a) is not type(b):
        return False
    if isinstance(a, PathPrefixMatch) and isinstance(b, PathPrefixMatch):
        pa, pb = path_segments(a.value), path_segments(b.value)
        return len(pb) >= len(pa) and pb[: len(pa)] == pa
    if isinstance(a, ChannelNameMatch) and isinstance(b, ChannelNameMatch):
        return {normalize_channel(v) for v in b.values} <= {normalize_channel(v) for v in a.values}
    if isinstance(a, ProjectKeyMatch) and isinstance(b, ProjectKeyMatch):
        return {normalize_project_key(v) for v in b.values} <= {
            normalize_project_key(v) for v in a.values
        }
    return False


def find_shadowed_rules(rules: Sequence[AclRule]) -> list[ShadowedRule]:
    '''Rules that can never fire because an earlier rule already covers them.'''
    out: list[ShadowedRule] = []
    for i, later in enumerate(rules):
        for earlier in rules[:i]:
            if _covers(earlier, later):
                out.append(ShadowedRule(later.id, earlier.id))
                break
    return out


def validate_acl_config(
    mapping: AclMapping, hierarchy: GroupHierarchy, quarantine_group: str
) -> list[ShadowedRule]:
    '''Single entry point. Raises InvalidAclConfigError; returns shadowing warnings.'''
    validate_hierarchy(hierarchy, quarantine_group)
    validate_rules(mapping.rules, set(hierarchy.groups), quarantine_group)
    return find_shadowed_rules(mapping.rules)




















