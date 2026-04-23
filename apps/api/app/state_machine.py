"""Simple state transition rules for practice lifecycle."""

TRANSITIONS = {
    "created": {"practicing"},
    "practicing": {"finished"},
    "finished": {"practicing", "archiving"},
    "archiving": {"archived", "practicing"},
    "archived": set(),
}


def can_transition(src: str, dst: str) -> bool:
    """Return whether a transition from src to dst is allowed."""
    return dst in TRANSITIONS.get(src, set())
