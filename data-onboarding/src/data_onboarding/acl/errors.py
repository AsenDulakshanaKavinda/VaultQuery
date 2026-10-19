

class AclError(Exception):
    '''Base class for ACL-related errors.'''
    pass

class InvalidAclConfigError(AclError, ValueError):
    '''Raised when the ACL policy is invalid.'''
    pass

class UnknownRoleError(AclError):
    '''Raised when an unknown role is encountered in the ACL policy.'''
    pass

class UnknownGroupError(AclError):
    '''Raised when an unknown group is encountered in the ACL policy.'''
    pass

class UnmappedContentError(AclError):
    '''Raised when content is not mapped to any ACL policy.'''
    pass