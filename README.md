# Konoha Engine

Konoha is a premium, modern Discord bot designed to completely replace your moderation, logging, and utility stack with surgical precision. 

## Features
- **Next-Gen Automod:** Zero-configuration defense system intercepting unauthorized links and scams.
- **Surgical Moderation:** Slash commands (`/ban`, `/tempban`, `/purge`) with ephemeral logging to keep chat clean.
- **Advanced Audit Logging:** Tracks deleted and edited messages into a hidden `#konoha-logs` channel.
- **Modern Self-Roles:** Create interactive UI Buttons (`/setup_roles`) for users to assign roles without outdated reactions.
- **Leveling & XP:** Dynamic XP tracking per message with rank cards (`/rank`) and level-up announcements.
- **Smart Welcomer:** Generates beautiful arrival telemetry embeds.

## Commands Reference
*All commands are deeply integrated with Discord Slash Commands (`/`).*

- **Moderation:** `/ban`, `/kick`, `/tempban`, `/unban`, `/bans`, `/purge`
- **Utility:** `/ping`, `/hello`
- **Leveling:** `/rank`
- **Configuration:** `/setup_roles`, `/testwelcome`

## Setup & Hosting
Konoha is built with `discord.py` and features a built-in Flask `keep_alive` server specifically optimized for 24/7 free hosting on Render + UptimeRobot.
