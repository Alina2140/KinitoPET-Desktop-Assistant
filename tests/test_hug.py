from unittest.mock import MagicMock, patch

import pytest

from content.hug_lines import HUG_LINES
from kinito.features.hug import HugMixin


class HugStub(HugMixin):
    pass


@pytest.fixture
def hug():
    stub = HugStub()
    stub.root = MagicMock()
    stub.root.after = MagicMock()
    stub.root.after_cancel = MagicMock()
    stub.tk_img_love_bubble = "love"
    stub._love_bubble_window = None
    stub._love_bubble_timer = None
    stub._hug_mode = False
    stub.speak = MagicMock()
    stub.get_screen_bounds = MagicMock(return_value=(0, 0, 1000, 800))
    return stub


def test_give_hug_shows_bubble_and_speaks(hug):
    with patch("kinito.features.hug.random.choice", return_value=HUG_LINES[0]), patch.object(
        hug, "show_love_bubble"
    ) as show, patch.object(hug, "_schedule_love_bubble_hide") as schedule:
        hug.give_hug()
    show.assert_called_once()
    schedule.assert_called_once_with(8000)
    assert hug._hug_mode is True
    hug.speak.assert_called_once_with(HUG_LINES[0])


def test_hide_love_bubble_clears_window(hug):
    window = MagicMock()
    window.winfo_exists.return_value = True
    hug._love_bubble_window = window
    hug.hide_love_bubble()
    window.destroy.assert_called_once()
    assert hug._love_bubble_window is None


def test_has_love_bubble_false_when_destroyed(hug):
    import tkinter as tk

    window = MagicMock()
    window.winfo_exists.side_effect = tk.TclError("destroyed")
    hug._love_bubble_window = window
    assert hug._has_love_bubble() is False
