def normalize_path(path: str, strip_prefix: str | None = None) -> str:
    """
    normalize canonical path strings
    - Remove the prefix from path (bucket name)
    - Replaces backslashes with slashes
    - Rejects null bytes and traversal above root
    - Collapses repeated slashes, removes '.' and resolves '..'
    - Returns a string starting with '/' and ending with no trailing
    """

    if "\x00" in path:
        raise ValueError("null byte in path")

    path = path.replace("\\", "/")

    if strip_prefix:
        strip_prefix = strip_prefix.replace("\\", "/").strip("/")
        parts = [p for p in path.split("/") if p]
        prefix_parts = [p for p in strip_prefix.split("/") if p]

        if parts[: len(prefix_parts)] == prefix_parts:
            parts = parts[len(prefix_parts) :]
        path = "/" + "/".join(parts)

    segments = path.split("/")
    stack: list[str] = []

    for seg in segments:
        if not seg or seg == ".":
            continue
        if seg == "..":
            if not stack:
                raise ValueError("path climbs above root")
            stack.pop()
        else:
            stack.append(seg)

    return "/" + "/".join(stack)


def normalize_channel(channel: str) -> str:
    """Strips whitespace, leading '#', and lowercases."""
    cleaned = channel.strip()
    cleaned = cleaned.removeprefix("#")
    return cleaned.lower()


def normalize_project_key(key: str) -> str:
    """Strips whitespace, preserves case."""
    return key.strip()


def path_has_prefix(path: str, prefix: str) -> bool:
    """Case-sensitive, whole-segment path prefix matching."""
    norm_path = normalize_path(path)
    norm_prefix = normalize_path(prefix)

    if norm_path == norm_prefix:
        return True

    # Ensure prefix ends with a single slash for segment boundary matching
    prefix_with_slash = norm_prefix if norm_prefix.endswith("/") else norm_prefix + "/"
    return norm_path.startswith(prefix_with_slash)


import re
from collections.abc import Iterable


def normalize_group_name(group_name: str) -> str:
    """
    Normalizes a single group name string:
    - Strips leading/trailing whitespace
    - Lowercases the name
    - Ensures it follows the strict ^grp_[a-z0-9_]+$ pattern
    """
    cleaned = group_name.strip().lower()
    if not re.match(r"^grp_[a-z0-9_]+$", cleaned):
        raise ValueError(f"Invalid group name format: '{group_name}'")
    return cleaned


def normalize_groups(groups: Iterable[str]) -> tuple[str, ...]:
    """
    Normalizes a collection of group names:
    - Strips and lowercases each group name
    - Validates format compliance
    - Deduplicates entries
    - Returns a sorted, immutable tuple
    """
    if not groups:
        raise ValueError("Group collection cannot be empty")

    normalized_set = {normalize_group_name(g) for g in groups}
    return tuple(sorted(normalized_set))
