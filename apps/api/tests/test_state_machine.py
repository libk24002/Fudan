from apps.api.app.state_machine import can_transition


def test_finished_to_archiving_is_allowed():
    assert can_transition('finished', 'archiving') is True


def test_practicing_to_archived_is_blocked():
    assert can_transition('practicing', 'archived') is False


def test_archiving_to_practicing_is_allowed():
    assert can_transition('archiving', 'practicing') is True
