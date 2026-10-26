from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from data_onboarding.acl import (
    HINT_CHANNEL,
    HINT_PATH,
    HINT_PROJECT,
    AclRule,
    ChannelNameMatch,
    PathPrefixMatch,
    ProjectKeyMatch,
)
from data_onboarding.acl.paths import (
    normalize_channel,
    normalize_path,
    normalize_project_key,
    path_has_prefix,
)


@dataclass(frozen=True)
class AclDecision:
    """immutable result of an ACL mapping operation."""

    allowed_groups: tuple[str, ...]
    rule_id: str | None

    @property
    def quarantined(self) -> bool:
        return self.rule_id is None


class AclMapper:
    """Maps ACL hints to allowed groups based on defined rules."""

    def __init__(self, rules: list[AclRule], quarantine_group: str = "grp_quarantine"):
        self.rules = rules
        self.quarantine_group = quarantine_group
        self._compiled_rules = [self._compiled_rules(r) for r in rules]

    def _compiled_rules(self, rule: AclRule) -> dict[str, Any]:
        """Compiles an AclRule into a dict for efficient matching."""
        compiled: dict[str, Any] = {
            "rule": rule,
            "id": rule.id,
            "source_system": rule.source_system,
            "allowed_groups": tuple(rule.allowed_groups),
        }

        match = rule.match
        if isinstance(match, PathPrefixMatch):
            compiled["hint_key"] = HINT_PATH
            compiled["norm_prefix"] = normalize_path(match.value)
        elif isinstance(match, ChannelNameMatch):
            compiled["hint_key"] = HINT_CHANNEL
            compiled["norm_channels"] = {normalize_channel(c) for c in match.values}
        elif isinstance(match, ProjectKeyMatch):
            compiled["hint_key"] = HINT_PROJECT
            compiled["norm_projects"] = {normalize_project_key(p) for p in match.values}

        return compiled

    def map(self, source_system: str, acl_hints: Mapping[str, Any]) -> AclDecision:
        """Maps ACL hints to allowed groups based on defined rules."""
        
        for c_rule in self._compiled_rules:
            # 1. Skip if source system differs
            if c_rule["source_system"] != source_system:
                continue

            # 2. Skip if hint key missing or non-string
            raw_hint = acl_hints.get(c_rule["hint_key"])
            if not isinstance(raw_hint, str):
                continue

            # 3. Normalize hint & 4. Evaluate match test
            rule_match = c_rule["rule"].match
            if isinstance(rule_match, PathPrefixMatch):
                try:
                    norm_path = normalize_path(raw_hint)
                except ValueError:
                    continue  # Invalid path/traversal attempt
                if path_has_prefix(norm_path, c_rule["norm_prefix"]):
                    return AclDecision(c_rule["allowed_groups"], c_rule["id"])

            elif isinstance(rule_match, ChannelNameMatch):
                norm_chan = normalize_channel(raw_hint)
                if norm_chan in c_rule["norm_channels"]:
                    return AclDecision(c_rule["allowed_groups"], c_rule["id"])

            elif isinstance(rule_match, ProjectKeyMatch):
                norm_proj = normalize_project_key(raw_hint)
                if norm_proj in c_rule["norm_projects"]:
                    return AclDecision(c_rule["allowed_groups"], c_rule["id"])

        # Default fallback: Quarantine
        return AclDecision((self.quarantine_group,), None)

    @classmethod
    def from_yaml(cls, path: str | Path, quarantine_group: str = "grp_quarantine") -> "AclMapper":

        path = Path(path)
        raw_data = yaml.safe_load(path.read_text())

        rules_data = raw_data.get("rules", [])

        parsed_rules = []
        for r_dict in rules_data:
            match_data = r_dict.get("match", {})
            match_type = match_data.get("type")

            match_obj = None
            if match_type == "path_prefix":
                match_obj = PathPrefixMatch(value=match_data["value"])
            elif match_type == "channel_name":
                match_obj = ChannelNameMatch(values=match_data["values"])
            elif match_type == "project_key":
                match_obj = ProjectKeyMatch(values=match_data["values"])
            else:
                raise ValueError(f"Unknown match type: {match_type}")

            rule = AclRule(
                id=r_dict["id"],
                source_system=r_dict["source_system"],
                match=match_obj,
                allowed_groups=r_dict["allowed_groups"]
            )
            parsed_rules.append(rule)

        return cls(rules=parsed_rules, quarantine_group=quarantine_group)




    
