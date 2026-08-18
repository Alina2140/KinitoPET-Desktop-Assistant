Kinito User Media
=================

Drop image files here to let Kinito show them on your screen.

Supported image formats: PNG, JPG, JPEG, WEBP, GIF, BMP

Videos go in the "videos" subfolder (MP4, WEBM, MOV, MKV, AVI).
Online videos are controlled by content/allowed_videos.py (whitelist).

Only files in these folders can be opened — Kinito will not load images
or videos from anywhere else on your PC.

Memory
------
Kinito can remember things about you across sessions.

- memory.json  — structured facts and follow-up notes (auto-managed)
- notes.txt    — human-readable mirror of notes (optional to edit)

Settings
--------
Toggle preferences from the in-app Settings menu are saved here:

- settings.json — screen effects, ambient reminders, app awareness, mood system, TTS volume, music folder, …

Game scores
-----------
Highscores for selected mini-games (Snake, Memory, True or False, Number Guess, Battleships):

- game_scores.json — snake highscore, memory best moves, trivia best/streak,
  number-guess best attempts, battleships best shots

These files are not in Git (personal data). You do not need to create them
yourself — Kinito writes them on first save. The folder is created at startup.

Right-click Kinito → "What do you remember?" to hear a summary.
Right-click Kinito → "Forget everything" to clear saved memory.
