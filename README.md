# KinitoPET — Python Virtual Assistant

A free, open-source desktop companion inspired by **KinitoPET**. Kinito lives on your screen as a small floating character: he talks, wanders around, asks questions, opens safe websites, plays music, and keeps you company while you work.

> **Platform:** Built and tested on **Windows 10/11**. Some features (TTS via `balcon.exe`, opening programs from the Desktop, window minimize / window grab) are Windows-specific. The core app may run on other OSes with reduced functionality.

---

## Table of contents

1. [Features](#features)
2. [Quick start (5 minutes)](#quick-start-5-minutes)
3. [How to use Kinito](#how-to-use-kinito)
4. [Project structure](#project-structure)
5. [Optional features & dependencies](#optional-features--dependencies)
6. [Troubleshooting](#troubleshooting)
7. [For developers](#for-developers)
8. [Documentation](#documentation)
9. [License & attribution](#license--attribution)

---

## Features

| Feature | Description |
|---------|-------------|
| **Floating desktop friend** | Transparent window; drag Kinito anywhere on screen |
| **Text-to-speech** | Speaks lines aloud (Balcon TTS + pyttsx3 fallback) |
| **Speech bubbles** | Interactive buttons and text boxes for replies |
| **Random questions** | 30+ conversation topics while idle |
| **Right-click menu** | Reminders, time, sleep mode, poems, facts, browser, music, hug, goodbye |
| **Safe browser** | Opens whitelisted HTTPS sites in a small window (or your default browser) |
| **Pictures** | Shows images from `GameAssets/UserMedia/` |
| **Camera** | Optional webcam view (requires OpenCV) |
| **Music player** | Play MP3s from your PC |
| **Hug** | Hug sprites + sweet lines |
| **Mini-games** | Tic-tac-toe, memory, battleships, RPS, trivia, and more (right-click → **Play a Game**) |
| **Idle animations** | Blinking, reading, fancy hat mode, sleep sprites |
| **Reminders** | Timer with sound after X minutes |

---

## Quick start (5 minutes)

### What you need

- **Windows 10 or 11**
- **Python 3.11 or 3.12** (recommended) — [python.org/downloads](https://www.python.org/downloads/)
  - During install, check **“Add python.exe to PATH”**
- This repository folder, including the **`GameAssets`** directory (sprites, sounds, `balcon.exe`)

### Steps

```powershell
# 1. Open PowerShell and go to the project folder
cd C:\path\to\KinitoPET-Python-Virtual-Assistant

# 2. Create a virtual environment (keeps dependencies isolated)
python -m venv .venv

# 3. Activate it
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start Kinito
python Kinito.py
```

If PowerShell blocks activation, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**First launch:** Kinito appears at a random position, says a startup line, and begins idle movement after a few seconds.

For a **full beginner walkthrough** (screenshots-level detail), see **[docs/INSTALL.md](docs/INSTALL.md)**.

---

## How to use Kinito

### Mouse controls

| Action | What happens |
|--------|----------------|
| **Left-click + drag** | Move Kinito around the screen |
| **Right-click** | Open the action menu |

### Right-click menu

- **Set Reminder** — type minutes (e.g. `15`); Kinito reminds you with sound + speech
- **Tell the Time** — speaks the current time and today's date (e.g. weekday and calendar date)
- **Sleep** / **Wake up** — nap mode (sleep animations); label switches while sleeping
- **Focus** / **Unfocus** — quiet mode; label switches while active
- **Screen Effects on** / **Screen Effects off** — rare glitch effects; label shows current state
- **Ambient Reminders on** / **Ambient Reminders off** — optional idle nudges
- **App Awareness on** / **App Awareness off** — comments on open/active apps by process name (Windows; unknown apps use FileDescription when available)
- **Screen Comments on** / **Screen Comments off** — occasional scripted desktop commentary (no screenshot or AI vision)
- **Painting Popups on** / **Painting Popups off** — random popups of saved paintings with scripted lines
- **Snoring on** / **Snoring off** — occasional snore sounds while idle
- **Sound Effects on** / **Sound Effects off** — UI and game sounds (speech stays separate)
- **Window Play on** / **Window Play off** — rare hand-sprite window grabs (Windows)
- **Speech on** / **Speech off** — toggle spoken TTS (bubbles still appear)
- **Special Days on** / **Special Days off** — holiday and joke-day comments at startup and idle
- **Menu Buttons** — show or hide individual menu entries
- **Sing** — recites a random poem (some include background music)
- **Fun Fact** — random fact
- **Visit a Website** — pick a category (Animals, Knowledge, Games, Horror, Surprise Me)
- **Play Music** — pick an MP3 or play a random one from your Music/Downloads folders
- **Play a Game** — mini-games (quick games and board games including Snake, Hangman, Minesweeper)
- **Hug** — hug pose sprites + hug line
- **Goodbye** — farewell line, then closes the app

### Spontaneous speech

While idle, Kinito may:

- Ask a random question (answer with buttons or a text field)
- Mention today's **special day** (holidays and joke days, when **Special Days** is on)
- Offer to open the camera, browser, music, or a hug
- Read a short story or wisdom quote
- Do a “fancy” show with a top hat sprite

Click the buttons in the speech bubble to respond. Press **Enter** in text boxes to submit.

Unanswered questions close automatically after about **2 minutes**.

### Easter eggs (intentional behavior)

Some choices trigger **KinitoPET-style surprises** — not bugs:

- **Declining a poem** (**No**) or **declining a secret image** (**Not now**) can cause certain intended things to happen. It needs `pyautogui` installed.
- **Window Play** (on by default): Kinito may rarely reach out with a hand sprite, grab a window edge, and slide it (or sometimes minimize it). Windows stay on the virtual desktop so they remain reachable. While he is dragging, you can take over the window yourself — he lets go and does not keep pulling. Turn **Window Play** off in the menu if you prefer a quieter desktop.

### Browser safety

Kinito only opens URLs from a **manual whitelist** in `content/allowed_sites.py`. Navigation to other HTTPS sites is blocked inside the built-in browser window.

### Paintings

Saved drawings from **Paint** live in `GameAssets/UserMedia/paintings/` (created automatically). With **Painting Popups** enabled, Kinito may occasionally show a saved painting in a popup and speak a short scripted comment.

### Memory (persistent user facts)

Kinito remembers personal facts across sessions — no database required.

- **Storage:** `GameAssets/UserMedia/memory.json` (and optional `notes.txt` mirror)
- These files are local only (listed in `.gitignore`) and are created automatically the first time something is saved (e.g. when you answer a name question or a follow-up).
- Right-click Kinito → **What do you remember?** to hear a summary.
- Right-click Kinito → **Forget everything** to clear saved memory.

Personal questions (name, favorite color, food, hobby, etc.) are asked once; answers are saved and reused in follow-up questions and startup greetings.

**Multi-value answers:** For facts like hobbies or pets, you can answer with comma-separated lists or phrases joined with “and” (e.g. `reading, hiking, and chess`). Kinito stores each item separately for richer follow-ups.

---

## Project structure

```
KinitoPET-Python-Virtual-Assistant/
├── Kinito.py              # Entry point — run this file
├── kinito/                  # Application code
│   ├── app.py               # Main window & lifecycle
│   ├── speech.py            # TTS, speech bubbles, menu
│   ├── bubble_ui.py         # Chamfered bubble chrome & buttons
│   ├── movement.py          # Drag, wander, idle animations
│   ├── assets.py            # Paths to GameAssets files
│   └── features/            # Browser, camera, music, hug, programs, content, games, paint
├── content/                 # All dialogue & data (easy to edit!)
│   ├── dialogue.py          # Questions, buttons, response lines
│   ├── dialog_registry.py   # Links questions → UI → actions
│   ├── questions.py         # Pool of random questions
│   ├── allowed_sites.py     # Browser whitelist
│   ├── facts.py, poems.py, stories.py, ...
│   └── site_validator.py    # URL safety checks
├── GameAssets/              # Sprites, MP3s, balcon.exe (required)
├── tests/                   # Automated tests
├── docs/                    # Detailed guides
├── requirements.txt         # Runtime dependencies
└── requirements-dev.txt     # pytest, ruff (for contributors)
```

---

## Optional features & dependencies

| Package | Purpose | If missing |
|---------|---------|------------|
| `pywebview` | Built-in browser window | Falls back to system default browser |
| `opencv-python` | Webcam feature | Camera questions still appear; opening camera shows a message |
| `pyttsx3` | TTS fallback | Uses `balcon.exe` only |
| `pygame` | Sound effects & MP3 | Required for sounds |
| `pyautogui` | Minimize windows (poem/image easter egg) | That easter egg silently fails |
| `Pillow` | Images / sprites | Required |

On startup, Kinito prints optional dependency status to the console, e.g.:

```
Kinito optional deps: {'pywebview': 'ok', 'opencv': 'missing', 'balcon': 'ok', 'pyttsx3': 'ok'}
```

### GameAssets folder

The app expects a `GameAssets` folder next to `Kinito.py`:

```
GameAssets/
├── Kinito.png, KinitoNormal.png, KinitoHug.png, Thinking.png, ...   # Sprites
├── Timer.mp3, Woosh.mp3, StartTalking.mp3, ...       # Sounds
├── Programs/balcon.exe                               # Windows TTS (optional fallback: pyttsx3)
├── SecretImages/                                     # Optional images for easter egg
└── UserMedia/                                        # Paintings, memory, and settings
```

If a sprite is missing, Kinito falls back to `KinitoNormal.png`.

---

## Troubleshooting

### `python` is not recognized

Python is not on your PATH. Reinstall Python and enable **“Add to PATH”**, or use the full path:

```powershell
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe Kinito.py
```

### `pip install` fails (proxy / 403)

Some corporate networks block PyPI. Try:

```powershell
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

Or install packages one by one. **Minimum to start:** `Pillow`, `pygame`, `pyttsx3`.

### No voice / TTS silent

1. Check that `GameAssets/Programs/balcon.exe` exists
2. Ensure `pyttsx3` is installed: `pip install pyttsx3`
3. Check Windows sound output device and volume
4. Confirm **Speech on** is selected in the right-click menu (TTS can be turned off while keeping speech bubbles)

### Browser opens in Chrome/Firefox instead of a small window

`pywebview` is not installed in your active environment. Install it:

```powershell
pip install pywebview
```

If that fails, the fallback (`webbrowser.open`) still works — just without the small controlled window.

### Camera does not work

```powershell
pip install opencv-python
```

Close other apps using the webcam. Kinito uses camera index `0` (default webcam).

### Kinito closes immediately / error on start

Run from a terminal to see the error:

```powershell
python Kinito.py
```

Common causes: missing `GameAssets`, missing `Pillow`, or no display (won’t run headless).

### Speech bubble buttons do nothing

The spoken line must contain a **marker substring** registered in `content/dialog_registry.py`. If you add new question text, see **[docs/EXTENDING.md](docs/EXTENDING.md)**.

### My windows minimized — is that a bug?

Usually **no**. Declining certain offers (poem **No**, secret image **Not now**) triggers intentional window minimizing on Windows — a KinitoPET-style easter egg. Separately, **Window Play** may occasionally grab and slide open windows with a hand sprite; you can take over mid-drag, and you can disable it via **Window Play off** in the menu. Windows are never closed. See [Easter eggs](#easter-eggs-intentional-behavior) above.

---

## For developers

```powershell
pip install -r requirements-dev.txt
python -m pytest tests/ -q    # Run tests
ruff check .                  # Lint
ruff check --fix .            # Auto-fix lint issues
```

Architecture: one `FloatingAssistant` class in `kinito/app.py` combines **mixins** (speech, movement, browser, camera, …). Dialogue text lives in `content/` and is wired through `dialog_registry.py`.

---

## Documentation

| Document | Audience |
|----------|----------|
| **[docs/INSTALL.md](docs/INSTALL.md)** | Complete install guide for beginners |
| **[docs/EXTENDING.md](docs/EXTENDING.md)** | Add questions, sites, sprites, features |
| **[docs/GITHUB.md](docs/GITHUB.md)** | Publish or clone from GitHub |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Pull requests & community guidelines |

---

## License & attribution

This project is released under the **[MIT License](LICENSE)** — free to use, modify, and share.

### Credits

| What | Who / where |
|------|-------------|
| **Kinito & KinitoPET** | [KinitoPET on Steam](https://store.steampowered.com/app/2075070/KinitoPET/) by **troy_en** |
| **Python template** | [TimTamCoder/KinitoPET-Python-Virtual-Assistant](https://github.com/TimTamCoder/KinitoPET-Python-Virtual-Assistant) by **TimTamCoder** |
| **Sprites** | [The Spriters Resource — KinitoPET](https://www.spriters-resource.com/pc_computer/kinitopet/) |
| **Emoji sheet** | [Pixel Art Emoji by Kuteken](https://kuteken.itch.io/pixel-art-emoji) (CC0) |

This is a **fan-made** desktop assistant. It is not an official KinitoPET product and is not affiliated with the game's developers or publishers.

If you fork this project or build your own desktop friend from it, **please credit this repository**, [TimTamCoder's template](https://github.com/TimTamCoder/KinitoPET-Python-Virtual-Assistant), and mention **KinitoPET** as inspiration.

**In the app:** right-click Kinito → **Settings** → **Credits** to view attributions and open the links above.

### Features (non-AI)

- **Birthday** — Kinito may ask for your birthday once; on that day you get a startup or idle congratulations.
- **Paint** — **Actions** → **Paint** opens a retro drawing window; save PNGs to `GameAssets/UserMedia/paintings/` and browse them in **My Paintings**.
- **Screen Comments** — **Settings** → **Screen Comments** toggles occasional scripted desktop commentary (no AI vision).
- **Painting Popups** — **Settings** → **Painting Popups** toggles random gallery popups with scripted lines.

---

**Enjoy your desktop companion!** If something is unclear, open an Issue on GitHub or improve the docs via Pull Request.
