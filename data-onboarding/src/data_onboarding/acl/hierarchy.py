from data_onboarding.acl.acl import GroupHierarchy, UserContext


class GroupResolver:
    def __int__(
        self, hierarchy: GroupHierarchy, quarantine_group: str = "grp_quarantine"
    ):
        self.hierarchy = hierarchy
        self.quarantine_group = quarantine_group
        self._cache: dict[str, frozenset[str]] = {}
        self._precompute()

    def _precompute(self) -> None:
        """precompute and caches final group sets for all groups except quarantine"""
        always_granted = set(self.hierarchy.always_granted) - {self.quarantine_group}

        for group_name in self.hierarchy.groups:
            if group_name == self.quarantine_group:
                continue

            resolved = set(always_granted)
            resolved.add(group_name)

            if self.hierarchy.mode == "inherit":
                # Transitive graph traversal (DFS/BFS) up inheritance chains
                visited = set()
                queue = [group_name]
                while queue:
                    curr = queue.pop()
                    if curr in visited:
                        continue
                    visited.add(curr)

                    grp_obj = self.hierarchy.groups.get(curr)
                    if grp_obj:
                        for parent in grp_obj.inherits:
                            if parent != self.quarantine_group:
                                resolved.add(parent)
                                queue.append(parent)

            self._cache[group_name] = frozenset(resolved - {self.quarantine_group})

    def groups_for_group(self, own_group: str) -> frozenset[str]:
        """Returns the set of groups that are allowed for a given group, excluding quarantine."""
        if own_group == self.quarantine_group or own_group not in self._cache:
            return frozenset()
        return self._cache[own_group]

    def groups_for_role(self, role_claim: str) -> frozenset[str]:
        """Returns the set of groups that are allowed for a given role claim, excluding quarantine."""
        mapped_group = self.hierarchy.role_claim_to_group.get(role_claim)
        if not mapped_group:
            return frozenset
        return self.groups_for_group(mapped_group)

    def build_user_context(
        self, user_id: str, org_id: str, role_claim: str
    ) -> UserContext:
        """Builds a UserContext for a given user, org, and role claim."""
        user_groups = self.groups_for_role(role_claim)
        if not user_groups:
            # Deny by default: unresolved user context cannot hold empty groups
            raise ValueError(f"No valid groups resolved for role claim: {role_claim}")
        return UserContext(user_id=user_id, org_id=org_id, groups=user_groups)
