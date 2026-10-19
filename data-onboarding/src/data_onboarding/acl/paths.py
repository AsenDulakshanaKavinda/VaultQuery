



def path_segments(raw: str) -> list[str]:

    # is raw path is a str? or empty?
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("path must be a non-empty string")

    if "\x00" in raw:
        raise ValueError("path contain a null byte")

    segments: list[str] = []
    for part in raw.strip().replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not segments:
                raise ValueError("path escapes the root")
        else:
            segments.append(part)

    return segments


def normalize_path(raw: str) -> str:
    return "/" + "/".join(path_segments(raw))

def path_has_prefix(path: str, prefix: str) -> bool:
    p, q = path_segments(path), path_segments(prefix)
    return len(p) >= len(q) and p[: len(q)] == q

def normalize_channel(raw: str) -> str:
    if not isinstance(raw, str):
        raise ValueError("channel name must be a string")

    cleaned = raw.strip().lstrip("#").strip().lower()

    if not cleaned:
        raise ValueError("channel name is empty")

    return cleaned

def normalize_project_key(raw: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("project key must be a non-empty string")
    return raw.strip()
    