"""Regression: ambient trigger methods must resolve to feature mixins, not Movement stubs."""

from kinito.app import FloatingAssistant
from kinito.features.ads import AdsMixin
from kinito.features.glitch import GlitchMixin
from kinito.features.nudges import NudgesMixin
from kinito.features.window_grab import WindowGrabMixin
from kinito.movement import MovementMixin


def test_ambient_triggers_are_not_movement_stubs():
    assert FloatingAssistant.maybe_trigger_screen_glitch is GlitchMixin.maybe_trigger_screen_glitch
    assert FloatingAssistant.maybe_trigger_blue_screen is GlitchMixin.maybe_trigger_blue_screen
    assert FloatingAssistant.maybe_trigger_random_ad is AdsMixin.maybe_trigger_random_ad
    assert (
        FloatingAssistant.maybe_trigger_ambient_reminder
        is NudgesMixin.maybe_trigger_ambient_reminder
    )
    assert FloatingAssistant.maybe_trigger_window_grab is WindowGrabMixin.maybe_trigger_window_grab
    assert FloatingAssistant.maybe_trigger_screen_glitch is not (
        MovementMixin.maybe_trigger_screen_glitch
    )
    assert FloatingAssistant.maybe_trigger_window_grab is not (
        MovementMixin.maybe_trigger_window_grab
    )
