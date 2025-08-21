import re

_DIALOGUE_RE = re.compile(r"['\"]")

def contains_dialogue(text: str) -> bool:
    """Return True if text contains dialogue indicated by single or double quotes."""
    return bool(_DIALOGUE_RE.search(text))
