"""Occasional spoken screen commentary (scripted lines; no vision)."""

from __future__ import annotations

import random
import threading
import time

from content import dialogue as dlg
from content.screen_comment_lines import pick_screen_comment_fallback


class ScreenCommentsMixin:
    """Speak occasional scripted desktop commentary."""

    SCREEN_COMMENT_CHANCE = 1 / 300
    SCREEN_COMMENT_COOLDOWN_SECONDS = 300

    def maybe_trigger_screen_comment(self) -> bool:
        """Roll for a silent screen glance; schedule work if it hits."""
        if not getattr(self, "_screen_comments_enabled", True):
            return False
        if getattr(self, "_focus_mode", False):
            return False
        if getattr(self, "_is_game_active", lambda: False)():
            return False
        if (
            self.paused
            or getattr(self, "_is_position_locked_by_user", lambda: self.is_dragging)()
            or getattr(self, "_camera_active", False)
            or getattr(self, "_browser_active", False)
        ):
            return False
        if getattr(self, "_is_busy_with_speech", lambda: False)():
            return False
        last_at = getattr(self, "_last_screen_comment_at", 0.0)
        if time.monotonic() - last_at < self.SCREEN_COMMENT_COOLDOWN_SECONDS:
            return False
        if random.random() >= self.SCREEN_COMMENT_CHANCE:
            return False
        self._last_screen_comment_at = time.monotonic()
        self.root.after(0, self._start_screen_comment)
        return True

    def toggle_screen_comments(self):
        """Enable or disable spontaneous screen commentary."""
        self._screen_comments_enabled = not getattr(self, "_screen_comments_enabled", True)
        if hasattr(self, "_persist_settings"):
            self._persist_settings()
        lines = (
            dlg.SCREEN_COMMENTS_ON_LINES
            if self._screen_comments_enabled
            else dlg.SCREEN_COMMENTS_OFF_LINES
        )
        self.speak(dlg.pick_line(lines), skip_ai=True)

    def _start_screen_comment(self):
        """Kick off commentary work off the UI thread."""
        if not getattr(self, "_running", True):
            return
        if not getattr(self, "_screen_comments_enabled", True):
            return
        threading.Thread(target=self._screen_comment_worker, daemon=True).start()

    def _screen_comment_worker(self):
        """Pick a fallback line and speak it on the UI thread."""
        line = pick_screen_comment_fallback()
        if not getattr(self, "_running", True):
            return
        if not getattr(self, "_screen_comments_enabled", True):
            return
        self.root.after(0, lambda spoken=line: self._speak_screen_comment(spoken))

    def _speak_screen_comment(self, line: str):
        """Deliver the comment with the normal speech bubble."""
        if getattr(self, "_is_busy_with_speech", lambda: False)():
            return
        self.speak(line, skip_ai=True)
