




from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from data_onboarding.acl.errors import UnmappedContentError
from data_onboarding.acl.paths import normalize_channel, normalize_path, normalize_project_key, path_has_prefix
from data_onboarding.core.settings import AclRule
from data_onboarding.domain.acl import HINT_CHANNEL, HINT_PATH, HINT_PROJECT, ChannelNameMatch, PathPrefixMatch, ProjectKeyMatch

@dataclass(frozen=True)
class AclDecision:
    # A decision made by the ACL mapper, indicating which groups are allowed and which rule (if any) was matched.
    allowed_groups: tuple[str, ...]
    rule_id: str | None

    @property
    def quarantined(self) -> bool:
        return self.rule_id is None

@dataclass(frozen=True)
class _Compiled:
    # A compiled ACL rule with its associated hint key, normalization function, and test function.
    rule: AclRule
    hint_key: str
    normalize: Callable[[str], str]
    test: Callable[[str], bool]

def _compile(rule: AclRule) -> _Compiled:
    '''
    This function compiles an AclRule into a _Compiled object, which includes the rule itself,
    the hint key, a normalization function, and a test function.
    '''
    m = rule.match
    if isinstance(m, PathPrefixMatch):
        prefix = normalize_path(m.value)
        return _Compiled(rule, HINT_PATH, normalize_path, lambda v: path_has_prefix(v, prefix))
    if isinstance(m, ChannelNameMatch):
        channels = frozenset(normalize_channel(v) for v in m.values)
        return _Compiled(rule, HINT_CHANNEL, normalize_channel, channels.__contains__)
    if isinstance(m, ProjectKeyMatch):
        keys = frozenset(normalize_project_key(v) for v in m.values)
        return _Compiled(rule, HINT_PROJECT, normalize_project_key, keys.__contains__)
    raise TypeError(f"unsupported match type: {type(m).__name__}")


class AclMapper:
    '''
    This class is responsible for mapping source systems and ACL hints to AclDecisions based on a set of compiled ACL rules.
    It takes a sequence of AclRule objects, a quarantine group, and an optional flag to fail on unmapped content as input, and provides a method to perform the mapping.
    '''
    def __init__(
            self,
            rules: Sequence[AclRule],
            quarantine_group: str,
            fail_on_unmapped: bool = False
    ) -> None:
        self._compiled = [_compile(r) for r in rules]
        self._quarantine = quarantine_group
        self._fail_on_unmapped = fail_on_unmapped

    def map(self, source_system: str, acl_hints: Mapping[str, Any]) -> AclDecision:
        '''
        This method maps a given source system and ACL hints to an AclDecision.
        It iterates through the compiled ACL rules, normalizes the hints, and tests for matches.
        If a match is found, it returns an AclDecision with the allowed groups and rule ID.
        If no match is found and fail_on_unmapped is True, it raises an UnmappedContentError. 
        Otherwise, it returns an AclDecision with the quarantine group.   
        '''
        for c in self._compiled:
            if c.rule.source_system != source_system:
                continue
            raw = acl_hints.get(c.hint_key)
            if not isinstance(raw, str):
                continue
            try:
                value = c.normalize(raw)
            except ValueError:
                continue
            if c.test(value):
                return AclDecision(tuple(c.rule.allowed_groups), c.rule.id)

        if self._fail_on_unmapped:
            raise UnmappedContentError(
                f"no ACL rule matched: source_system={source_system!r}, "
                f"hint_keys={sorted(acl_hints)}"
            )
        return AclDecision((self._quarantine,), None)
