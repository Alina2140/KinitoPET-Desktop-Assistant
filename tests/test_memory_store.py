"""Tests for the file-backed memory store."""

import json
import os

import pytest

from kinito.memory.store import (
    MAX_NOTES_IN_PROMPT,
    MAX_NOTES_STORED,
    MAX_PROMPT_BLOCK_CHARS,
    MemoryStore,
)


@pytest.fixture
def memory_dir(tmp_path):
    return str(tmp_path / "user_media")


@pytest.fixture
def store(memory_dir):
    return MemoryStore(directory=memory_dir)


def test_empty_store_has_no_prompt_block(store):
    assert store.as_prompt_block() == ""
    assert store.user_display_name() == "You"


def test_set_fact_and_load_roundtrip(store, memory_dir):
    store.set_fact("user_names", "Alex")
    store.mark_answered("What should I call you?")

    reloaded = MemoryStore(directory=memory_dir)
    assert reloaded.get_fact("user_names") == "Alex"
    assert reloaded.is_answered("What should I call you?")


def test_is_question_answered_matches_marker_in_text(store):
    store.mark_answered(dlg_marker := "What's your favorite color?")
    assert store.is_question_answered(f"Hey! {dlg_marker} I love colors.")
    assert not store.is_question_answered("How is your day?")


def test_add_note_deduplicates(store):
    assert store.add_note("Likes jazz music", source="question") is True
    assert store.add_note("Likes jazz music", source="question") is False
    assert len(store.snapshot()["notes"]) == 1


def test_notes_fifo_when_over_limit(store):
    for index in range(MAX_NOTES_STORED + 3):
        store.add_note(f"weekend_plans: plan {index} (follow-up?)", source="question")
    notes = store.snapshot()["notes"]
    assert len(notes) == MAX_NOTES_STORED
    assert notes[0]["text"] == "weekend_plans: plan 3 (follow-up?)"
    assert notes[-1]["text"] == f"weekend_plans: plan {MAX_NOTES_STORED + 2} (follow-up?)"


def test_as_prompt_block_includes_facts_and_recent_notes(store):
    store.set_fact("user_names", "Alex")
    store.add_note("weekend_plans: hiking (Alex, got any plans?)", source="question")
    block = store.as_prompt_block()
    assert "user names: Alex" in block
    assert "hiking" in block


def test_as_prompt_block_limits_note_count(store):
    for index in range(MAX_NOTES_IN_PROMPT + 5):
        store.add_note(f"weekend_plans: note {index} (plans?)", source="question")
    block = store.as_prompt_block()
    assert "note 4" not in block
    assert "note 5" in block
    assert f"note {MAX_NOTES_IN_PROMPT + 4}" in block


def test_as_prompt_block_truncates_long_output(store):
    store.set_fact("user_names", "A" * 200)
    block = store.as_prompt_block()
    assert len(block) <= MAX_PROMPT_BLOCK_CHARS


def test_reset_removes_files(store, memory_dir):
    store.set_fact("user_names", "Alex")
    store.add_note("weekend_plans: test (plans?)", source="question")
    path = os.path.join(memory_dir, "memory.json")
    notes_path = os.path.join(memory_dir, "notes.txt")
    assert os.path.isfile(path)
    assert os.path.isfile(notes_path)

    store.reset()
    assert not os.path.isfile(path)
    assert not os.path.isfile(notes_path)
    assert store.snapshot()["facts"] == {}


def test_load_recovers_from_corrupt_json(memory_dir):
    os.makedirs(memory_dir, exist_ok=True)
    path = os.path.join(memory_dir, "memory.json")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("{not valid json")

    store = MemoryStore(directory=memory_dir)
    assert store.snapshot()["facts"] == {}


def test_save_writes_valid_json(memory_dir, store):
    store.set_fact("user_names", "Sam")
    path = os.path.join(memory_dir, "memory.json")
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    assert data["facts"]["user_names"] == "Sam"


def test_as_facts_prompt_block_omits_notes(store):
    store.set_fact("user_names", "Alex")
    store.add_note("weekend_plans: hiking (plans?)", source="question")
    facts_block = store.as_facts_prompt_block()
    assert "user names: Alex" in facts_block
    assert "hiking" not in facts_block
    full_block = store.as_prompt_block()
    assert "hiking" in full_block


def test_mark_topic_asked_and_fifo(memory_dir, store):
    store.mark_topic_asked("topic_a")
    assert store.is_topic_asked("topic_a")
    reloaded = MemoryStore(directory=memory_dir)
    assert reloaded.is_topic_asked("topic_a")


def test_remove_fact_value_keeps_remaining_items(store):
    store.set_fact("hobbies", "Drawing, Reading, Crochet")
    assert store.remove_fact_value("hobbies", "Drawing") is True
    assert store.get_fact_values("hobbies") == ["Reading", "Crochet"]
    assert store.remove_fact_value("hobbies", "missing") is False


def test_delete_fact_removes_key(store, memory_dir):
    store.set_fact("favorite_drink", "Cherry Coke")
    store.set_fact("hobbies", "Drawing")
    assert store.delete_fact("favorite_drink") is True
    assert store.get_fact("favorite_drink") is None
    assert store.get_fact("hobbies") == "Drawing"
    assert store.delete_fact("favorite_drink") is False
    reloaded = MemoryStore(directory=memory_dir)
    assert reloaded.get_fact("favorite_drink") is None
    assert reloaded.get_fact("hobbies") == "Drawing"


def test_notes_list_and_replace_notes(store, memory_dir):
    store.add_note("Likes jazz nights")
    store.add_note("Works late sometimes")
    notes = store.notes_list()
    assert len(notes) == 2
    assert notes[0]["text"] == "Likes jazz nights"

    store.replace_notes(["Only this note remains", "", "Only this note remains"])
    assert [note["text"] for note in store.notes_list()] == ["Only this note remains"]
    reloaded = MemoryStore(directory=memory_dir)
    assert [note["text"] for note in reloaded.notes_list()] == ["Only this note remains"]


def test_set_fact_rejects_placeholder_for_favorite_drink(store):
    store.set_fact("favorite_drink", "Tea")
    store.set_fact("favorite_drink", "no")
    assert store.get_fact("favorite_drink") == "Tea"


def test_daily_facts_are_dated_and_read_as_plain_value(store):
    from datetime import date

    from kinito.memory.daily_facts import format_daily_fact

    store.set_fact("energy_today", "low")
    assert store.get_fact("energy_today") == "low"
    raw = store.snapshot()["facts"]["energy_today"]
    assert raw == format_daily_fact("low")

    store.set_fact("plans_tonight", "movie night")
    assert store.get_fact("plans_tonight") == "movie night"
    assert store.snapshot()["facts"]["plans_tonight"].startswith(date.today().isoformat())


def test_daily_checkin_facts_accept_neutral(store):
    from kinito.memory.daily_facts import format_daily_fact

    store.set_fact("mood_today", "okay")
    assert store.get_fact("mood_today") == "neutral"
    assert store.snapshot()["facts"]["mood_today"] == format_daily_fact("neutral")

    store.set_fact("energy_today", "medium")
    assert store.get_fact("energy_today") == "neutral"

    store.set_fact("focus_today", "normal")
    assert store.get_fact("focus_today") == "neutral"


def test_stale_daily_facts_are_cleared_on_read(store):
    from datetime import date, timedelta

    from kinito.memory.daily_facts import format_daily_fact

    yesterday = date.today() - timedelta(days=1)
    store._data["facts"]["energy_today"] = format_daily_fact("low", today=yesterday)
    store._data["facts"]["mood_today"] = "bad"
    store.save()

    assert store.get_fact("energy_today") is None
    assert store.get_fact("mood_today") is None
    assert "energy_today" not in store.snapshot()["facts"]
    assert "mood_today" not in store.snapshot()["facts"]


def test_stale_daily_facts_dropped_on_load(memory_dir):
    from datetime import date, timedelta

    from kinito.memory.daily_facts import format_daily_fact
    from kinito.memory.store import memory_file_path

    yesterday = date.today() - timedelta(days=1)
    path = memory_file_path(memory_dir)
    os.makedirs(memory_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "version": 1,
                "facts": {
                    "energy_today": format_daily_fact("low", today=yesterday),
                    "focus_today": format_daily_fact("busy"),
                    "user_names": "Alex",
                },
                "answered_markers": [],
                "notes": [],
                "asked_topics": [],
                "topic_asked_at": {},
            },
            handle,
        )

    store = MemoryStore(directory=memory_dir)
    assert store.get_fact("energy_today") is None
    assert store.get_fact("focus_today") == "busy"
    assert store.get_fact("user_names") == "Alex"
