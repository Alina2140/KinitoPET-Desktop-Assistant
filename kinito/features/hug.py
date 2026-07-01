"""Love-bubble overlay shown during virtual hugs."""

import random
import tkinter as tk
from tkinter import Toplevel

from content.hug_lines import HUG_LINES


class HugMixin:
    """Small heart bubble beside Kinito during hug interactions."""

    LOVE_BUBBLE_SIZE = 56
    LOVE_BUBBLE_OVERLAP = 32

    def _cancel_love_bubble_timer(self):
        """Cancel the scheduled auto-hide for the love bubble."""
        if self._love_bubble_timer is not None:
            try:
                self.root.after_cancel(self._love_bubble_timer)
            except (tk.TclError, ValueError):
                pass
            self._love_bubble_timer = None

    def _has_love_bubble(self):
        """Return True if the love-bubble window is open."""
        try:
            return self._love_bubble_window is not None and self._love_bubble_window.winfo_exists()
        except tk.TclError:
            return False

    def position_love_bubble(self):
        """Place the love bubble overlapping Kinito's right edge (transparent PNG)."""
        if not self._has_love_bubble():
            return

        self.root.update_idletasks()
        self._love_bubble_window.update_idletasks()

        kinito_x = self.root.winfo_rootx()
        kinito_y = self.root.winfo_rooty()
        kinito_w = max(self.root.winfo_width(), 1)
        bubble_w = self._love_bubble_window.winfo_width()
        bubble_h = self._love_bubble_window.winfo_height()

        bubble_x = kinito_x + kinito_w - self.LOVE_BUBBLE_OVERLAP
        bubble_y = kinito_y - bubble_h // 4

        min_x, min_y, max_x, max_y = self.get_screen_bounds(bubble_w, bubble_h)
        bubble_x = max(min_x, min(bubble_x, max_x))
        bubble_y = max(min_y, min(bubble_y, max_y))

        new_pos = (bubble_x, bubble_y)
        if getattr(self, "_love_bubble_last_pos", None) == new_pos:
            return
        self._love_bubble_last_pos = new_pos

        self._love_bubble_window.geometry(f"+{bubble_x}+{bubble_y}")
        self._love_bubble_window.lift()
        self._love_bubble_window.wm_attributes("-topmost", True)

    def show_love_bubble(self):
        """Open the heart bubble image beside Kinito."""
        self.hide_love_bubble()
        self._love_bubble_window = Toplevel(self.root)
        self._love_bubble_window.overrideredirect(True)
        self._love_bubble_window.attributes("-transparentcolor", "white")
        self._love_bubble_window.wm_attributes("-topmost", True)

        label = tk.Label(self._love_bubble_window, image=self.tk_img_love_bubble, bg="white")
        label.pack()
        self.root.after(0, self.position_love_bubble)

    def hide_love_bubble(self):
        """Destroy the love bubble and cancel its hide timer."""
        self._cancel_love_bubble_timer()
        self._love_bubble_last_pos = None
        if self._has_love_bubble():
            self._love_bubble_window.destroy()
        self._love_bubble_window = None

    def _schedule_love_bubble_hide(self, delay_ms=8000):
        """Hide the love bubble after *delay_ms* milliseconds."""
        self._cancel_love_bubble_timer()
        self._love_bubble_timer = self.root.after(delay_ms, self.hide_love_bubble)

    def give_hug(self):
        """Show the love bubble and speak a hug line."""
        self.show_love_bubble()
        self._schedule_love_bubble_hide(8000)
        self._hug_mode = True
        self.speak(random.choice(HUG_LINES))
