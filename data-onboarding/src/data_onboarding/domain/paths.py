
def normalize_path(path: str) -> str:
    '''
    normalize canonical path strings
    - Replaces backslashes with slashes
    - Rejects null bytes and traversal above root
    - Collapses repeated slashes, removes '.' and resolves '..'
    - Returns a string starting with '/' and ending with no trailing
    '''

    if "\x00" in path:
        raise ValueError('null byte in path')

    path = path.replace('\\', '/')
    segments = path.split('/')
    stack: list[str] = []

    for seg in segments:
        if not seg or seg == '.':
            continue
        if seg == '..':
            if not stack:
                raise ValueError('path climbs above root')
            stack.pop()
        else:
            stack.append(seg)

    return '/'+ '/'.join(stack)

def normalize_channel(channel: str) -> str:
    ''' Strips whitespace, leading '#', and lowercases.''' 
    cleaned = channel.strip()
    if cleaned.startswith("#"):
        cleaned = cleaned[1:]
    return cleaned.lower()


def normalize_project_key(key: str) -> str:
    ''' Strips whitespace, preserves case.''' 
    return key.strip()



def path_has_prefix(path: str, prefix: str) -> bool:
    ''' Case-sensitive, whole-segment path prefix matching. '''
    norm_path = normalize_path(path)
    norm_prefix = normalize_path(prefix)

    if norm_path == norm_prefix:
        return True

    # Ensure prefix ends with a single slash for segment boundary matching
    prefix_with_slash = norm_prefix if norm_prefix.endswith("/") else norm_prefix + "/"
    return norm_path.startswith(prefix_with_slash)

