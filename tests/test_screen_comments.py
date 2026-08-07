"""Tests for ephemeral screen commentary."""

from unittest.mock import MagicMock, patch

import pytest

from content import dialogue as dlg
from kinito.features.screen_comments import ScreenCommentsMixin


class ScreenCommentStub(ScreenCommentsMixin):
    pass


@pytest.fixture
def screen_comments():
    stub = ScreenCommentStub()
    stub._running = True
    stub._screen_comments_enabled = True
    stub._last_screen_comment_at = 0.0
    stub.paused = False
    stub.is_dragging = False
    stub._camera_active = False
    stub._browser_active = False
    stub._focus_mode = False
    stub.root = MagicMock()
    stub.root.after = MagicMock()
    stub.speak = MagicMock()
    stub._is_busy_with_speech = MagicMock(return_value=False)
    stub._is_game_active = MagicMock(return_value=False)
    stub._persist_settings = MagicMock()
    return stub


def test_maybe_trigger_respects_disabled(screen_comments):
    screen_comments._screen_comments_enabled = False
    assert screen_comments.maybe_trigger_screen_comment() is False
    screen_comments.root.after.assert_not_called()


def test_maybe_trigger_respects_focus_mode(screen_comments):
    screen_comments._focus_mode = True
    assert screen_comments.maybe_trigger_screen_comment() is False


def test_maybe_trigger_respects_busy(screen_comments):
    screen_comments._is_busy_with_speech.return_value = True
    assert screen_comments.maybe_trigger_screen_comment() is False


def test_maybe_trigger_respects_cooldown(screen_comments):
    import time

    screen_comments._last_screen_comment_at = time.monotonic()
    with patch("kinito.features.screen_comments.random.random", return_value=0.0):
        assert screen_comments.maybe_trigger_screen_comment() is False


def test_maybe_trigger_schedules_on_hit(screen_comments):
    with patch("kinito.features.screen_comments.random.random", return_value=0.0):
        assert screen_comments.maybe_trigger_screen_comment() is True
    screen_comments.root.after.assert_called_once()
    assert screen_comments.root.after.call_args.args[1] == screen_comments._start_screen_comment


def test_worker_speaks_fallback_line(screen_comments):
    screen_comments._screen_comment_worker()
    screen_comments.root.after.assert_called()
    spoken = screen_comments.root.after.call_args.args[1]
    spoken()
    screen_comments.speak.assert_called_once()
    assert screen_comments.speak.call_args.kwargs.get("skip_ai") is True
    assert isinstance(screen_comments.speak.call_args.args[0], str)


def test_toggle_screen_comments_disables(screen_comments):
    screen_comments.toggle_screen_comments()
    assert screen_comments._screen_comments_enabled is False
    screen_comments._persist_settings.assert_called_once()
    screen_comments.speak.assert_called_once()
    spoken = screen_comments.speak.call_args.args[0]
    assert spoken in dlg.SCREEN_COMMENTS_OFF_LINES
