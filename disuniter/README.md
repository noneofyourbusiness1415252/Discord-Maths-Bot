This creates a simple website to go with your discord.py bot on https://replit.com so it can be kept alive.
# Usage
Store your bot token in a secret called `DISCORD_TOKEN`. Secrets are accessed through the lock icon on the left on desktop, and commands tab at the bottom > secrets on mobile.
```py
from discord.ext import commands
from disuniter import keepAlive
import discord
# Include members intent here if you want to show your discord tag and profile picture, but that will disable the logging to protect users' privacy
bot = commands.Bot()
# Needed to show DM owner link if you don't have members intent, but can be omitted if you don't want to show your DM link anyways
bot.owner_id = your_discord_user_id_here
# normal bot code here...
keepAlive(bot)
```
Wait, where's the `bot.run`?? The `keepAlive` function does that for you
1) To enforce using a secret to store your token so you don't expose it (NEVER expose it even if you are to remove it instantly, because people can check your repl's history)
2) To restart your bot automatically when there's a rate limit. Rate limits are caused by too many requests from the same IP that is shared across multiple repls, and are responsible for downtimes on replit-hosted bots.

# Why this?
- No dependencies, unlike the typical Flask keep-alive
- No spammy output, unlike Flask and the keep-alive I usually recommended on the replit discord
- It shows:
	- Uptime
	- Number of servers
	- Latency (ping)
	- Logs, unless you have any of the following privacy-violating intents:
		- `message_content`
		- `presences`
		- `members`
- It automatically adds your repl to https://up.repl.link, a pinger, if it isn't already there
- It uses [Solarized](https://ethanschoonover.com/solarized/#features), which is objectively the best colour palette ever.
# Why is it called dis-uniter?
I am keeping Discord bots alive. Discord = disagreement. I am dis-uniting by keeping disagreements alive.