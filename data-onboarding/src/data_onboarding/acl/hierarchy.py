



from data_onboarding.acl.errors import UnknownGroupError, UnknownRoleError
from data_onboarding.acl.validation import validate_hierarchy
from data_onboarding.domain.acl import GroupHierarchy, UserContext


class GroupResolver:
    '''
    This class is responsible for resolving group memberships based on a defined group hierarchy.
    It takes a GroupHierarchy object and a quarantine group as input, validates the hierarchy,
    and provides methods to retrieve the groups associated with a specific group or role claim.
    '''
    def __init__(self, hierarchy: GroupHierarchy, quarantine_group: str) -> None:

        validate_hierarchy(hierarchy, quarantine_group)
        self._h = hierarchy
        # Precomputed once, so lookups on the query path are a dict read.
        self._expanded: dict[str, frozenset[str]] = {
            g: self._expand(g) for g in hierarchy.groups if g != quarantine_group
        }

    def _expand(self, own_group: str) -> frozenset[str]:
        '''
        This method computes the set of groups that a given group "owns" or has access to, 
        based on the hierarchy defined in the GroupHierarchy object. 
        It takes into account the inheritance of groups and any always granted groups defined in the hierarchy.
        '''
        held = {own_group, *self._h.always_granted}
        if self._h.mode == "inherit":
            stack = [own_group]
            while stack:
                for parent in self._h.groups[stack.pop()].inherits:
                    if parent not in held:
                        held.add(parent)
                        stack.append(parent)
        return frozenset(held)

    def groups_for_group(self, own_group: str) -> frozenset[str]:
        '''
        This method retrieves the set of groups that a given group "owns" or has access to, 
        based on the precomputed expanded groups. 
        If the group is not found in the precomputed expanded groups, it raises an UnknownGroupError.
        '''
        try:
            return self._expanded[own_group]
        except KeyError:
            raise UnknownGroupError(f"unknown group: {own_group!r}") from None

    def groups_for_role(self, role_claim: str) -> frozenset[str]:
        '''
        This method retrieves the set of groups that a given role claim has access to, 
        based on the precomputed expanded groups. 
        If the role claim is not found in the precomputed expanded groups, it raises an UnknownRoleError.
        '''
        group = self._h.role_claim_to_group.get(role_claim.strip()) if role_claim else None
        if group is None:
            raise UnknownRoleError(f"unmapped role claim: {role_claim!r}")
        return self.groups_for_group(group)

    def build_user_context(self, user_id: str, org_id: str, role_claim: str) -> UserContext:
        ''' 
        This method builds a UserContext object for a given user, organization, and role claim.
        It retrieves the groups associated with the role claim and constructs a UserContext object. 
        '''
        return UserContext(
            user_id=user_id, org_id=org_id, groups=self.groups_for_role(role_claim)
        )



