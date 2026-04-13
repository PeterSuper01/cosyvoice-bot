# cosyvoice-bot

A Discord bot that integrates with [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) to deliver text-to-speech (TTS) audio directly into your voice channels.

---

## Features

- Automatically joins a configured Discord voice channel on startup
- Converts text to speech using a CosyVoice TTS backend
- Modular cog-based architecture (`tts`, `admin`)
- Environment-based configuration via `.env`

## Supported Languages
 
The TTS engine supports the following languages:
 
Chinese, English, Japanese, Korean, German, Spanish, French, Italian, Russian

---

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- A running CosyVoice TTS server (HTTP API)
- A Discord bot token with the following intents enabled:
  - `Message Content`
  - `Voice States`

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/PeterSuper01/cosyvoice-bot.git
cd cosyvoice-bot
```

2. **Install dependencies**

```bash
poetry install
```

3. **Configure environment variables**

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_VOICE_CHANNEL_ID=your_voice_channel_id
BASE_URL=http://your-cosyvoice-server/
```

| Variable | Description |
|---|---|
| `DISCORD_BOT_TOKEN` | Your Discord bot's token |
| `DISCORD_VOICE_CHANNEL_ID` | The voice channel the bot will join on startup |
| `BASE_URL` | Base URL of your CosyVoice TTS API server |
| `TEST_URL` | Test endpoint URL for the TTS server |

---

## Usage

Start the bot with:

```bash
poetry run python bot.py
```

The bot will connect to the configured voice channel automatically when it's ready.

---

## Project Structure

```
cosyvoice-bot/
├── cogs/
│   ├── tts.py        # TTS commands and voice playback logic
│   └── admin.py      # Admin/utility commands
├── utils/
│   └── tts_client.py # HTTP client for the CosyVoice API
├── bot.py            # Bot entry point
├── config.py         # Pydantic settings / env config
├── pyproject.toml    # Project metadata and dependencies
└── .env              # Environment variables (not committed)
```

---
 
## Commands
 
### `!register`
 
Registers your voice profile with the bot. Attach a `.wav` file to the command and the bot will use ASR (Automatic Speech Recognition) to auto-detect and store your voice feature. You can also manually provide your own transcription instead of relying on ASR.

```
!register [text] (attach a .wav file)
```

- If `text` is provided, it will be used as the transcription of the audio.
- If omitted, the bot will automatically transcribe the audio using ASR.
 
**Audio file requirements:**
- Format: `.wav`
- Duration: less than 30 seconds
- Sample rate: 16,000 Hz or higher
 
> You must register before using `!tts`.

---
 
### `!tts <text>`
 
Converts the given text to speech using your registered voice model and plays it in the voice channel.
 
```
!tts Hello, how are you?
```
 
> Requires the user to have run `!register` first.