"""Tests for persistent settings store."""

import json
import os

import pytest

from kinito.settings_store import SettingsStore


@pytest.fixture
def settings_dir(tmp_path):
    return str(tmp_path / "user_media")


@pytest.fixture
def store(settings_dir):
    return SettingsStore(directory=settings_dir)


def test_defaults_when_missing(store):
    assert store.get("screen_effects_enabled") is True
    assert store.get("ambient_reminders_enabled") is True
    assert store.get("app_awareness_enabled") is True
    assert store.get("screen_comments_enabled") is True
    assert store.get("paint_recall_enabled") is True
    assert store.get("snoring_enabled") is True
    assert store.get("window_grab_enabled") is True
    assert store.get("tts_enabled") is True
    assert store.get("player_focus_enabled") is True
    assert store.get("mood_system_enabled") is True
    assert store.get("color_guess_voice_enabled") is True
    assert store.get_int("tts_volume") == 100
    assert store.get_int("music_volume") == 75
    assert store.get_music_folder() == ""


def test_update_and_reload_roundtrip(store, settings_dir):
    store.update(
        screen_effects_enabled=False,
        ambient_reminders_enabled=False,
        app_awareness_enabled=False,
        screen_comments_enabled=False,
        paint_recall_enabled=False,
        snoring_enabled=False,
        window_grab_enabled=False,
        tts_enabled=False,
        player_focus_enabled=False,
        tts_volume=40,
        music_volume=55,
        music_folder=r"C:\Music",
        mood_system_enabled=False,
        color_guess_voice_enabled=False,
    )
    reloaded = SettingsStore(directory=settings_dir)
    assert reloaded.get("screen_effects_enabled") is False
    assert reloaded.get("ambient_reminders_enabled") is False
    assert reloaded.get("app_awareness_enabled") is False
    assert reloaded.get("screen_comments_enabled") is False
    assert reloaded.get("paint_recall_enabled") is False
    assert reloaded.get("snoring_enabled") is False
    assert reloaded.get("window_grab_enabled") is False
    assert reloaded.get("tts_enabled") is False
    assert reloaded.get("player_focus_enabled") is False
    assert reloaded.get_int("tts_volume") == 40
    assert reloaded.get_int("music_volume") == 55
    assert reloaded.get_music_folder() == r"C:\Music"
    assert reloaded.get("mood_system_enabled") is False
    assert reloaded.get("color_guess_voice_enabled") is False


def test_invalid_file_falls_back_to_defaults(settings_dir):
    os.makedirs(settings_dir, exist_ok=True)
    path = os.path.join(settings_dir, "settings.json")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("{not-json")
    store = SettingsStore(directory=settings_dir)
    assert store.get("screen_effects_enabled") is True


def test_ignores_unknown_keys(store):
    store.update(screen_effects_enabled=False, not_a_real_setting=False)
    with open(store._path, encoding="utf-8") as handle:
        raw = json.load(handle)
    assert "not_a_real_setting" not in raw
    assert raw["screen_effects_enabled"] is False


def test_int_and_music_folder_roundtrip(store, settings_dir):
    from kinito.settings_store import clamp_tts_volume

    store.update(tts_volume=40, music_volume=20, music_folder=r"C:\Music")
    reloaded = SettingsStore(directory=settings_dir)
    assert reloaded.get_int("tts_volume") == 40
    assert reloaded.get_int("music_volume") == 20
    assert reloaded.get_music_folder() == r"C:\Music"
    assert clamp_tts_volume(150) == 100
    assert clamp_tts_volume(-3) == 0
