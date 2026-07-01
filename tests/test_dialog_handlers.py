"""Integration-style tests for dialog handlers beyond the happy path."""

from content import dialogue as dlg
from content.dialog_registry import find_dialog_spec, handle_dialog_response


def test_handle_story_declined_clears_pending(mock_app):
    mock_app._pending_story = "A tale"
    spec = find_dialog_spec(dlg.STORY_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_NOT_NOW)
    assert mock_app._pending_story is None
    mock_app.speak.assert_called_once()


def test_handle_story_accepted(mock_app):
    spec = find_dialog_spec(dlg.STORY_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_SURE)
    mock_app.say_pending_story.assert_called_once()


def test_handle_browser_yes_opens_category_picker(mock_app):
    spec = find_dialog_spec(dlg.BROWSER_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_YES)
    mock_app.ask_browser_category.assert_called_once()


def test_handle_browser_no_declines(mock_app):
    spec = find_dialog_spec(dlg.BROWSER_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_NO)
    mock_app.speak.assert_called_once()


def test_handle_hug_yes(mock_app):
    spec = find_dialog_spec(dlg.HUG_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_YES)
    mock_app.give_hug.assert_called_once()


def test_handle_music_player_yes(mock_app):
    spec = find_dialog_spec(dlg.MUSIC_PLAYER_QUESTIONS[0])
    handle_dialog_response(mock_app, spec, dlg.BUTTON_YES)
    mock_app.ask_music_player_pick.assert_called_once()


def test_handle_music_pick_declined(mock_app):
    spec = find_dialog_spec(dlg.MUSIC_PLAYER_PICK_QUESTION)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_NOT_NOW)
    mock_app.speak.assert_called_once()


def test_handle_color_text_response(mock_app):
    spec = find_dialog_spec(dlg.COLOR_QUESTION)
    handle_dialog_response(mock_app, spec, "blue")
    mock_app.speak.assert_called_once()
    assert "blue" in mock_app.speak.call_args[0][0]


def test_handle_game_okay_opens_game_picker(mock_app):
    spec = find_dialog_spec(dlg.GAME_QUESTION)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_OKAY)
    mock_app.offer_game_picker.assert_called_once()


def test_handle_menu_play_game(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_PLAY_GAME)
    mock_app.offer_game_picker.assert_called_once()


def test_handle_game_picker_tic_tac_toe(mock_app):
    spec = find_dialog_spec(dlg.GAME_PICKER_QUESTION)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_GAME_TIC_TAC_TOE)
    mock_app.start_tic_tac_toe.assert_called_once()


def test_game_picker_buttons_exclude_not_now():
    spec = find_dialog_spec(dlg.GAME_PICKER_QUESTION)
    assert dlg.BUTTON_NOT_NOW not in spec.ui.buttons


def test_handle_rps_rock(mock_app):
    spec = find_dialog_spec(dlg.RPS_QUESTION)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_ROCK)
    mock_app.speak.assert_called_once()


def test_handle_number_guess_higher_reprompts(mock_app):
    mock_app._number_guess_target = 50
    mock_app._number_guess_attempts = 0
    spec = find_dialog_spec(dlg.NUMBER_GUESS_QUESTION)
    handle_dialog_response(mock_app, spec, "10")
    mock_app.speak.assert_called_once()
    spoken = mock_app.speak.call_args[0][0]
    assert dlg.NUMBER_GUESS_MARKER.lower() in spoken.lower()


def test_handle_number_guess_correct(mock_app):
    mock_app._number_guess_target = 50
    mock_app._number_guess_attempts = 0
    spec = find_dialog_spec(dlg.NUMBER_GUESS_QUESTION)
    handle_dialog_response(mock_app, spec, "50")
    mock_app.speak.assert_called_once()
    assert mock_app._number_guess_target is None


def test_handle_joke_sure(mock_app):
    spec = find_dialog_spec(dlg.JOKE_QUESTION)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_SURE)
    mock_app.say_random_joke.assert_called_once()


def test_handle_menu_tell_time(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_TELL_TIME)
    mock_app.print_current_datetime.assert_called_once()


def test_handle_menu_toggle_screen_effects(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_SCREEN_EFFECTS_OFF)
    mock_app.toggle_screen_effects.assert_called_once()


def test_handle_menu_toggle_focus(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_FOCUS)
    mock_app.toggle_focus.assert_called_once()


def test_handle_menu_wake_up(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_WAKE_UP)
    mock_app.toggle_pause.assert_called_once()


def test_handle_menu_unfocus(mock_app):
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_UNFOCUS)
    mock_app.toggle_focus.assert_called_once()


def test_handle_menu_blocked_during_focus_mode(mock_app):
    mock_app._focus_mode = True
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_FUN_FACT)
    mock_app.say_random_fact.assert_not_called()


def test_handle_menu_unfocus_allowed_during_focus_mode(mock_app):
    mock_app._focus_mode = True
    spec = find_dialog_spec(dlg.MENU_PROMPT)
    handle_dialog_response(mock_app, spec, dlg.BUTTON_UNFOCUS)
    mock_app.toggle_focus.assert_called_once()
