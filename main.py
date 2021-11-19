#!/usr/bin/env python3
from os import system, environ
import keep_alive

keep_alive.keep_alive()
try:
	from discord.ext import commands
	from discord_variables_plugin import GlobalUserVariables
except ModuleNotFoundError:
	print("discord.py is not installed. Installing...")
	check_pip = str(system("python3 -m pip -V"))
	if not "0" in check_pip:
		install_pip = system(
			"curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py ; python3"
			" get-pip.py"
		)
		if not "0" in install_pip:
			print(
				"Error while installing pip, which is required to install discord.py."
			)
	install_discord = str(
		system("python3 -m pip install discord.py discord-variables-plugin")
	)
	if not "0" in install_discord:
		print("Error while installing discord.py.\a")
from discord.ext import commands
from discord import File
from discord_variables_plugin import GlobalUserVariables, ServerVariables

serverVars = ServerVariables()
userVars = GlobalUserVariables()

import logging
import logging.handlers
from math import *

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("./discord.log", "a", maxBytes=32768)
handler.setFormatter(
	logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot = commands.Bot(command_prefix="=", case_insensitive=True)


@bot.event
async def on_ready():
	print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_command(ctx):
	userVars.load("ServerVars")
	serverVars.load("serverVars")


@bot.command(name="primerange", aliases=["pr"])
async def primerange(ctx, num1, num2, file: bool = False):
	await ctx.channel.trigger_typing()
	num1 = int(eval(num1))
	num2 = int(eval(num2))
	try:
		limit = serverVars.get(ctx.message.guild, "MessageLimit")
	except:
		limit = 2000

	def Prime(n):
		if n == 2 or n == 3:
			return True
		if n < 2 or n % 2 == 0:
			return False
		if n < 9:
			return True
		if n % 3 == 0:
			return False
		r = int(n ** 0.5)
		f = 5
		while f <= r:
			if n % f == 0:
				return False
			if n % (f + 2) == 0:
				return False
			f += 6
		return True

	amount = 0
	primes = []
	i = num1
	while i < num2 + 1:
		if Prime(i):
			amount += 1
			primes.append(i)
		i += 1
	if amount == 1:
		await ctx.send(f"There is 1 prime number between {str(num1)} and {str(num2)}:")
	else:
		await ctx.send(
			f"There are {str(amount)} prime numbers between {str(num1)} and"
			f" {str(num2)}:"
		)
	await ctx.channel.trigger_typing()
	Total = str(primes).replace("]", "").replace("[", "")
	if len(Total) > limit or file:
		with open(f"/tmp/{ctx.message.id}.md", "w+") as f:
			f.write(Total)
			print(f.read())
			if file:
				await ctx.send(file=File(f"/tmp/{ctx.message.id}.md"))
			else:
				await ctx.send(
					f"Message would be over {limit} characters, so sending in file"
					" instead",
					file=File(f"/tmp/{ctx.message.id}.md"),
				)
	else:
		await ctx.send(str(Total))


@primerange.error
async def pr_error(ctx, error):
	await ctx.send(
		"Please make sure your command is set out like this:\n=primerange <first"
		f" number> <final number>\nThis was the error encountered:\n {str(error)}"
	)


@bot.command(
	name="powerrange",
	aliases=["pwr"],
	help=(
		"Find the squares or cubes within a range, e.g. `=pr 1 100 2` finds squares"
		" between 1 and 100."
	),
)
async def powerrange(ctx, start, end, *th_power):
	try:
		limit = serverVars.get(ctx.message.guild, "MessageLimit")
	except:
		limit = 2000
	await ctx.channel.trigger_typing()
	start = int(eval(start))
	end = int(eval(end)) + 1

	def super(x: str):
		"""Make a number superscript"""
		normal = "0123456789"
		super_s = "⁰¹²³⁴⁵⁶⁷⁸⁹"
		res = x.maketrans(normal, super_s)
		return x.translate(res)

	message = ""
	file = False
	for p in th_power:
		if "file" in p:
			file = True
	for p in th_power:
		i = start
		try:
			p = int(p)
		except:
			break
		total = 0
		if p == 2:
			message += f"> **Square numbers between {i} and {end}:**\n"
		elif p == 3:
			message += f"> **Cube numbers between {i} and {end}:**\n"
		elif p == 4:
			message += f"> **Tesseractic numbers between {i} and {end}:**\n"
		else:
			message += f"> **{p}th powers between {i} and {end}:**\n"
		while i < end:
			if round(abs(i) ** (1 / p)) ** p == abs(i):
				message += f"{int(i ** (1 / p))}{super(str(p))} = {i}\n"
				total += 1
			i += 1
		message += f"Total: {total}\n"
		if len(message) > limit or file:
			with open(f"/tmp/{ctx.message.id}.md", "w+") as f:
				f.write(message)
			if file:
				await ctx.send(file=File(f"/tmp/{ctx.message.id}.md"))
			else:
				await ctx.send(
					"Message would be over 2000 characters, so sending in file instead",
					file=File(f"/tmp/{ctx.message.id}.md"),
				)
		else:
			await ctx.send(message)


@powerrange.error
async def pwr_error(ctx, error):
	await ctx.send(
		"Please make sure your command is set out like this:\n`=powerrange <first"
		" number> <final number> <nth power>`\n Example:\n`=powerrange 1 100 3` to"
		" find cubes between 1 and 100. \nThis was the error encountered:\n"
		f" {str(error)}"
	)


@bot.command(
	name="eval", aliases=["ev"], help="Do a calculation using Python operators."
)
async def formula(ctx, *formula):
	userVars.load("userVars")
	await ctx.channel.trigger_typing()
	try:
		limit = serverVars.get(ctx.message.guild, "MessageLimit")
	except:
		limit = 2000
	if "system" in formula or "exit" in formula:
		assert 0
	f = ""
	for i in formula:
		f += f" {i}"
	for i in f.split():
		if i[0] == "$":
			var = userVars.get(ctx.message.author, "".join(i[1:]))
			f = f.replace(i, str(var))
	answer = eval(f)
	if len(str(answer)) > limit:
		with open(f"/tmp/{ctx.message.id}.md", "w+") as f:
			f.write(str(answer))
		await ctx.send(
			f"Message would be over {limit} characters, so sending in file instead",
			file=File(f"/tmp/{ctx.message.id}.md"),
		)
	else:
		await ctx.send(answer)


@formula.error
async def formula_error(ctx, error):
	await ctx.send(
		"Error: Please make sure your formula makes sense and uses python operators or"
		" the cmath module. \nThis was the error encountered:\n"
		+ str(error)
	)


@bot.command(name="CuboidVolume", aliases=["CuV"])
async def CuV(ctx, length: int, height: int, width: int):
	await ctx.send(length * height * width)


@CuV.error
async def CuVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=CuV <height> <width> length>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="PyramidVolume", aliases=["PyV"])
async def PV(ctx, base_area: int, height: int):
	await ctx.send((1 / 3) * base_area * height)


@PV.error
async def PVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=PV <base_area> <height>`. 
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="SphereVolume", aliases=["SV"])
async def SV(ctx, radius: int):
	await ctx.send((4 / 3) * pi * radius ** 3)


@SV.error
async def SVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=SV <radius>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="ConeVolume", aliases=["CoV"])
async def CoV(ctx, radius: int, height: int):
	await ctx.send((1 / 3) * pi * radius ** 2 * height)


@CoV.error
async def CoVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=CoV <radius> <height>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="CylinderVolume", aliases=["CyV"])
async def CyV(ctx, radius: int, height: int):
	await ctx.send(pi * radius ** 2 * height)


@CyV.error
async def CyVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=CyV <radius> <height>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="PentagonalPrismVolume", aliases=["PPV"])
async def PPV(ctx, height: int, base_edge_length: int):
	await ctx.send((5 / 4) * height * base_edge_length ** 2 * (1 + 2 / sqrt(5)))


@PPV.error
async def PPVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=PPV <height> <base edge length>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(name="HexagonalPrismVolume", aliases=["HPV"])
async def HPV(ctx, height: int, base_edge_length: int):
	await ctx.send((3 * sqrt(3) / 2) * height * base_edge_length ** 2)


@HPV.error
async def HPVError(ctx, error: str):
	await ctx.send(
		f"""
	Error: Please make sure your command makes sense and is set out as:
	`=HPV <height> <base edge length>`.
	This was the error encountered:
	{error}
	"""
	)


@bot.command(
	name="MessageLimit",
	aliases=["ML"],
	help="Set the character limit for messages sent by the bot.",
)
@commands.has_permissions(administrator=True)
async def ML(ctx, limit: int):
	if limit > 2000:
		await ctx.send("Limit can not be more than 2000.")
		limit = 2000
	serverVars.set(ctx.message.guild, "MessageLimit", limit)
	serverVars.save("serverVars")


@ML.error
async def MLError(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send("Permission denied: You are not an admin of this server.")
	else:
		await ctx.send(
			f"""Error: Please make sure your command makes sense and is set out as:
		`=MessageLimit <limit>`
		This was the error encountered:
		{error}"""
		)


@bot.command(name="var", help="Save a variable for use in =eval, e.g. if you set `e` to `3+2`, `ev $e + 1` returns `6`.")
async def var(ctx, var, val):
	userVars.set(ctx.message.author, var, val)
	userVars.save("userVars")

bot.run(environ["TOKEN"])
