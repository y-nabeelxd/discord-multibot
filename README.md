<div align="center">

# 🤖 Discord MultiBot

**All-in-one Discord bot with music streaming, economy games, moderation, and multi-game verification.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-2.3%2B-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![License: MIT](https://img.shields.io/github/license/y-nabeelxd/discord-multibot?color=brightgreen)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/y-nabeelxd/discord-multibot?style=social)](https://github.com/y-nabeelxd/discord-multibot)
[![GitHub Forks](https://img.shields.io/github/forks/y-nabeelxd/discord-multibot?style=social)](https://github.com/y-nabeelxd/discord-multibot)
[![Code Style: Prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://prettier.io)

[**Quick Start**](#-setup--installation) • [**Features**](#-features) • [**Commands Reference**](#-hybrid-commands-slash--prefix) • [**Verification Guide**](#-multi-game-verification)

---

</div>

## 🌟 Why Discord MultiBot?

**Discord MultiBot** is a production-ready, modular Discord bot written in **Python 3.10+** using **discord.py 2.3+**. Built with an extensible cog-based architecture, it combines high-performance audio streaming, comprehensive server moderation, interactive economy minigames, support tickets, and game player verification into a single unified bot.

- 🎵 **High-Quality Audio**: Built on `yt-dlp` and `FFmpeg` with automatic SoundCloud fallback and interactive button player.
- 🛡️ **Advanced Moderation**: Full punishment suite (ban, kick, timeout, warn, purge, slowmode, channel clone/nuke).
- 🔒 **Multi-Game Verification**: Automated player verification for **Roblox** (bio code), **FiveM** (server query), and **SA:MP** (MySQL/RCON).
- ⚡ **Full Hybrid Support**: Use commands either as modern Slash commands (`/command`) or traditional text prefixes (`!command`).
- 🪙 **Interactive Economy & Minigames**: Daily rewards, coinflip, slots, blackjack, work, and community leveling.
- 🎫 **Support Tickets & Giveaways**: Button-driven ticket panels with private threads and automated giveaway timers.

---

## ✨ Features Matrix

| Category                 | Highlights                                                                   | Slash Ready |
| :----------------------- | :--------------------------------------------------------------------------- | :---------: |
| 🎵 **Music Streaming**   | Search, queue, skip, pause, resume, lyrics, SoundCloud fallback              |     ✅      |
| 🛡️ **Server Moderation** | Ban, kick, timeout (1s–28d), warn tracking, message purge, lock/unlock       |     ✅      |
| 🔒 **Game Verification** | Roblox (code-in-bio), FiveM (live server status), SA:MP (MySQL/RCON)         |     ✅      |
| 🏆 **Leveling & XP**     | Passive chat XP, customizable user rank cards, server leaderboards           |     ✅      |
| 🎫 **Support Tickets**   | Ephemeral ticket panels, staff roles, transcripts, button closes             |     ✅      |
| 🎉 **Giveaways**         | Timed giveaways with interactive join buttons and auto-roller                |     ✅      |
| 🪙 **Economy & Games**   | Daily coins, coinflip, slots, pay, work, rob                                 |     ✅      |
| 🎮 **Fun & Social**      | Tic-Tac-Toe, RPS, 8-Ball, Trivia, meme generator, ship, slap, hug            |     ✅      |
| 🔧 **Utility & Tools**   | Safe calculator, weather lookup, Google translation, polls, reminders, snipe |     ✅      |

---

## 📂 Project Architecture

```
discord-multibot/
├── bot.py                     # Bot entrypoint & startup lifecycle
├── config.py                  # Typed configuration loaded from .env
├── utils.py                   # Reusable helpers, console formatting & API clients
├── test_load.py               # Automated verification test suite for cogs & evaluator
├── requirements.txt           # Python package dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Protected secrets & clean repository ignore rules
├── .prettierrc.json           # Code style formatting rules
└── plugins/                   # Modular cog extensions
    ├── music/                 # Audio streaming engine (yt-dlp + FFmpeg)
    ├── moderation/            # Server protection & member discipline
    ├── verification/          # Roblox, FiveM, and SA:MP verification
    ├── leveling/              # XP algorithms & leaderboard storage
    ├── ticket/                # Ticket creation panels & channel lifecycle
    ├── giveaway/              # Timed giveaway coordinator
    ├── economy/               # Virtual currency & gambling minigames
    ├── fun/                   # Social commands & button minigames
    ├── utility/               # Weather, calculator, translate, reminder
    └── slash/                 # Dedicated slash management & voice controls
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/y-nabeelxd/discord-multibot.git
cd discord-multibot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> [!NOTE]
> **FFmpeg Requirement**: FFmpeg is bundled automatically on Windows via `static-ffmpeg`. For native Linux hosting, install it with:
>
> ```bash
> sudo apt update && sudo apt install -y ffmpeg
> ```

### 3. Configure environment variables

Copy the example template to create your `.env` file:

```bash
cp .env.example .env
```

Open `.env` in your text editor and fill in your keys:

```env
# Core Bot Settings
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
GAME_PREFIX=owo
BOT_OWNER_ID=your_discord_user_id

# Optional API Integrations
WEATHER_API_KEY=your_openweathermap_api_key
YT_COOKIES=cookies.txt

# Multi-Game Verification Toggles
VERIFICATION_ROBLOX=true
ROBLOX_ROLE_ID=123456789012345678

VERIFICATION_FIVEM=true
FIVEM_SERVER=127.0.0.1:30120
FIVEM_ROLE_ID=123456789012345678

VERIFICATION_SAMP=true
SAMP_ROLE_ID=123456789012345678
```

> [!IMPORTANT]
> **Enable Privileged Gateway Intents**:
> Go to the [Discord Developer Portal](https://discord.com/developers/applications) > **Bot** > Enable all three options under **Privileged Gateway Intents**:
>
> - **Presence Intent**
> - **Server Members Intent**
> - **Message Content Intent**

### 4. Run automated verification tests

Ensure all 10 cogs and security evaluators pass before launching:

```bash
python test_load.py
```

### 5. Launch the bot

```bash
python bot.py
```

---

## ⚡ Hybrid Commands (Slash + Prefix)

Every command supports both traditional text triggers (`!command`) and Discord Slash commands (`/command`).

### 🎵 Music Commands

| Command               | Usage                      | Description                                   |
| :-------------------- | :------------------------- | :-------------------------------------------- |
| `!play` / `/play`     | `!play <song name or URL>` | Search YouTube or play direct audio stream    |
| `!lyrics` / `/lyrics` | `!lyrics [song name]`      | Fetch lyrics for current or specified track   |
| `!queue` / `/queue`   | `!queue`                   | Display current track queue with pagination   |
| `!skip` / `/skip`     | `!skip`                    | Vote or force skip to next queued song        |
| `!pause` / `/pause`   | `!pause`                   | Pause current playback session                |
| `!resume` / `/resume` | `!resume`                  | Resume paused playback session                |
| `!stop` / `/stop`     | `!stop`                    | Clear active queue and leave voice channel    |
| `!vc247` / `/vc247`   | `!vc247`                   | Keep the bot in the voice channel permanently |

### 🛡️ Moderation Commands

| Command                   | Usage                         |   Permissions   | Description                                        |
| :------------------------ | :---------------------------- | :-------------: | :------------------------------------------------- |
| `!ban` / `/ban`           | `!ban @user [reason]`         |   Ban Members   | Permanently bans a member from the server          |
| `!kick` / `/kick`         | `!kick @user [reason]`        |  Kick Members   | Kicks a member from the server                     |
| `!timeout` / `/timeout`   | `!timeout @user 10m [reason]` |    Moderate     | Times out a member (e.g. `30s`, `15m`, `2h`, `7d`) |
| `!warn` / `/warn`         | `!warn @user [reason]`        |    Moderate     | Logs a persistent warning for a member             |
| `!warnings` / `/warnings` | `!warnings [@user]`           |    Moderate     | Lists all recorded warnings for a member           |
| `!purge` / `/purge`       | `!purge <1-100>`              | Manage Messages | Bulk deletes up to 100 recent messages             |
| `!lock` / `/lock`         | `!lock [#channel]`            | Manage Channels | Locks down channel send permissions                |
| `!unlock` / `/unlock`     | `!unlock [#channel]`          | Manage Channels | Restores channel send permissions                  |
| `!nuke` / `/nuke`         | `!nuke [#channel]`            |  Administrator  | Clones channel settings and deletes old one        |

### 🔒 Multi-Game Verification

| Game             | Command                       |     Method     | Details                                                 |
| :--------------- | :---------------------------- | :------------: | :------------------------------------------------------ |
| **Roblox**       | `!verifyroblox <username>`    |    Bio Code    | Generates unique security code to place in profile bio  |
| **FiveM**        | `!verifyfivem <name/id>`      |  Server Query  | Queries live FiveM server player list                   |
| **FiveM Live**   | `!fivemserverlive [#channel]` | Realtime Embed | Auto-updating embed with player count and server status |
| **SA:MP**        | `!verifysamp [code/name]`     |  MySQL / RCON  | Verifies against game database or live RCON status      |
| **SA:MP Status** | `!sampstatus`                 |  Query Socket  | Live server query for player count and ping             |

### 🪙 Economy & Gambling (Prefix: `owo`)

| Command        | Usage                                 | Description                                         |
| :------------- | :------------------------------------ | :-------------------------------------------------- |
| `owo daily`    | `owo daily`                           | Claim your free daily coin reward (300–5,000 coins) |
| `owo balance`  | `owo balance [@user]`                 | View your wallet and bank balance                   |
| `owo coinflip` | `owo coinflip <amount> [heads/tails]` | Wager coins on a coinflip                           |
| `owo slots`    | `owo slots <amount>`                  | Bet coins on the slot machine                       |
| `owo work`     | `owo work`                            | Complete a quick job to earn coins                  |
| `owo pay`      | `owo pay @user <amount>`              | Transfer coins directly to another member           |
| `owo rob`      | `owo rob @user`                       | Attempt to steal coins from another user            |

### 🎫 Tickets & 🎉 Giveaways

| Command         | Usage                              | Description                                                    |
| :-------------- | :--------------------------------- | :------------------------------------------------------------- |
| `!ticket setup` | `!ticket setup [#channel]`         | Deploys an interactive button panel for support tickets        |
| `!ticket close` | `!ticket close`                    | Archives and closes the current ticket thread                  |
| `!gstart`       | `!gstart <time> <winners> <prize>` | Launches a timed giveaway (e.g. `!gstart 2h 1w Discord Nitro`) |
| `!gend`         | `!gend <message_id>`               | Manually concludes an active giveaway                          |
| `!greroll`      | `!greroll <message_id>`            | Rerolls a new winner for a completed giveaway                  |

---

## 🛠️ Security & Safe Design

- **AST-Based Math Evaluator**: Math parsing uses safe Abstract Syntax Tree analysis with exponent thresholds, preventing code execution (`eval`) and memory denial-of-service.
- **Defensive API Calls**: All external HTTP requests enforce strict connection timeouts (10s) with exception fallbacks.
- **Safe Interaction Lifecycle**: Slash command responses and message deletions are cleanly guarded to avoid Discord API 404/400 exceptions.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project: `https://github.com/y-nabeelxd/discord-multibot`
2. Create your Feature Branch: `git checkout -b feat/amazing-feature`
3. Commit your Changes: `git commit -m 'feat: add amazing feature'`
4. Push to the Branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

<div align="center">

**Maintained by [y-nabeelxd](https://github.com/y-nabeelxd)**

_If you found this bot helpful, give it a ⭐ star on GitHub!_

</div>
