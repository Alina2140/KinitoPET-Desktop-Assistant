"""Unit tests for mini-game logic."""

import random

import pytest

from content import dialogue as dlg
from kinito.features.games.memory import DEFAULT_PAIRS, build_deck, is_match
from kinito.features.games.number_guess import (
    compare_guess,
    is_valid_guess,
    parse_guess,
)
from kinito.features.games.rock_paper_scissors import MOVES, rps_winner
from kinito.features.games.tic_tac_toe import (
    EMPTY,
    KINITO,
    PLAYER,
    check_winner,
    choose_ai_move,
    winning_move,
)


def test_rps_rock_beats_scissors():
    assert rps_winner(dlg.BUTTON_ROCK, dlg.BUTTON_SCISSORS) == "player"


def test_rps_scissors_beats_paper():
    assert rps_winner(dlg.BUTTON_SCISSORS, dlg.BUTTON_PAPER) == "player"


def test_rps_paper_beats_rock():
    assert rps_winner(dlg.BUTTON_PAPER, dlg.BUTTON_ROCK) == "player"


def test_rps_draw():
    for move in MOVES:
        assert rps_winner(move, move) is None


def test_rps_kinito_wins():
    assert rps_winner(dlg.BUTTON_ROCK, dlg.BUTTON_PAPER) == "kinito"


def test_parse_guess_valid():
    assert parse_guess(" 42 ") == 42


def test_parse_guess_invalid():
    assert parse_guess("abc") is None


@pytest.mark.parametrize("value", [0, 101, -5])
def test_is_valid_guess_out_of_range(value):
    assert is_valid_guess(value) is False


def test_compare_guess():
    assert compare_guess(50, 50) == "correct"
    assert compare_guess(10, 50) == "higher"
    assert compare_guess(90, 50) == "lower"


def test_ttt_player_row_win():
    board = [PLAYER, PLAYER, PLAYER] + [EMPTY] * 6
    assert check_winner(board) == PLAYER


def test_ttt_draw():
    board = [
        PLAYER,
        KINITO,
        PLAYER,
        KINITO,
        PLAYER,
        KINITO,
        KINITO,
        PLAYER,
        KINITO,
    ]
    assert check_winner(board) == "draw"


def test_ttt_winning_move_finds_block():
    board = [PLAYER, PLAYER, EMPTY] + [EMPTY] * 6
    assert winning_move(board, PLAYER) == 2


def test_ttt_ai_blocks_player_win():
    board = [PLAYER, PLAYER, EMPTY, EMPTY, KINITO, EMPTY, EMPTY, EMPTY, EMPTY]
    assert choose_ai_move(board) == 2


def test_memory_deck_has_pairs():
    random.seed(0)
    deck = build_deck()
    assert len(deck) == 16
    for symbol in DEFAULT_PAIRS:
        assert deck.count(symbol) == 2


def test_memory_is_match():
    assert is_match("🦊", "🦊") is True
    assert is_match("🦊", "🐸") is False
