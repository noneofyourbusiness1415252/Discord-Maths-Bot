#!/usr/bin/env python3
from os import environ, path
from discord.ext import commands
from discord import File, Embed
from discord import Colour
from discord_variables_plugin import GlobalUserVariables, ServerVariables
from matplotlib import pyplot

serverVars = ServerVariables()
userVars = GlobalUserVariables()

import logging
import logging.handlers
from math import *
from flask import Flask
from threading import Thread
from time import time
from fractions import Fraction

app = Flask("Umar's Maths Bot")


@app.route("/")
def display_logs():
	return open("discord.log").read()


def run():
	app.run("0.0.0.0")


Thread(target=run).start()
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("./discord.log", "a", 32768, 1)
handler.setFormatter(
	logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot = commands.Bot(command_prefix="=", case_insensitive=True)


def discordround(ctx, *number: float):
	userVars.load("userVars")
	rounded = []
	try:
		roundto = userVars.get(ctx.message.author, "RoundTo")
	except:
		if len(number) == 1:
			return number[0]
		return number
	digits = int(roundto[:-2])
	for i in number:
		if roundto.endswith("sf"):
			format = f"%.{digits}g"
			if type(i) == complex:
				rounded.append(float(format % i.real) + float(format % i.imag))
			elif (asfloat := float(format % i)) % 1:
				rounded.append(asfloat)
			else:
				rounded.append(int(asfloat))
		else:
			if type(i) == complex:
				rounded.append(round(i.real, digits) + round(i.imag, digits) * 1j)
			else:
				rounded.append(round(i, digits))
	if len(rounded) == 1:
		return rounded[0]
	return rounded


def discordnum(ctx: commands.context.Context, *calc: str):
	userVars.load("userVars")
	answers = []
	for i in calc:
		while True:
			try:
				ans = eval(str(i))
				if type(ans) in [complex, int, float]:
					ans = discordround(ctx, ans)
			except NameError as e:
				for j in str(e).split():
					if "'" in j:
						var = j.replace("'", "")
						break
				try:
					i = i.replace(var, userVars.get(ctx.message.author, var))
				except:
					locals()[var] = __import__(var)
				else:
				answers.append(ans)
				break
	if len(answers) == 1:
		return answers[0]
	return answers


async def send(ctx: commands.context.Context, file: str = "", footer="", **embed):
	author = ctx.message.author
	guild = ctx.message.guild
	userVars.load("userVars")
	try:
		embed = Embed(**embed, colour=userVars.get(author, "colour"))
	except KeyError:
		embed = Embed(**embed, colour=Colour.random())
		userVars.save("userVars")
	if footer:
		embed.set_footer(text=footer)
	try:
		limit = serverVars.get(ctx.message.guild, "MessageLimit")
	except KeyError:
		limit = 4000
	if len(embed) > limit or file == "file":
		open(f"/tmp/{ctx.message.id}.md", "w+").write(
			f"**{embed.title}**\n{embed.description}\n{footer}"
		)
		if file:
			return await ctx.send(file=File(f"/tmp/{ctx.message.id}.md"))
		else:
			return await ctx.send(
				f"Message would be over {limit} characters, so sending in file instead",
				file=File(f"/tmp/{ctx.message.id}.md"),
			)
	return await ctx.send(embed=embed)


@bot.event
async def on_ready():
	print(f"We have logged in as", bot.user)


@bot.event
async def on_command(ctx):
	await ctx.channel.trigger_typing()


@bot.command(name="Primes", help="Find primes up to a number")
async def primes(ctx, limit, file=""):
	start_time = time()
	limit = discordnum(ctx, limit)
	sieve = [False] * (limit + 1)
	sqrt = int(limit ** 0.5)
	uptosqrt = range(1, sqrt + 1)
	for i in uptosqrt:
		isquare = i ** 2
		tsquare = isquare * 3
		for j in uptosqrt:
			jsquare = j ** 2
			if (n := 4 * isquare + jsquare) <= limit and n % 12 in [1, 5]:
				sieve[n] = not sieve[n]
			if (n := tsquare + jsquare) <= limit and n % 12 == 7:
				sieve[n] = not sieve[n]
			if i > j and (n := tsquare - jsquare) <= limit and n % 12 == 11:
				sieve[n] = not sieve[n]
	for i in range(5, sqrt):
		if sieve[i]:
			isquare = i ** 2
			for j in range(isquare, limit + 1, isquare):
				sieve[j] = False
	primes = [2, 3] + [x for x in range(5, limit) if sieve[x]]
	await send(
		ctx,
		file,
		f"Time taken: {discordround(ctx, time() - start_time)}",
		title=f"{len(primes)} primes up to {limit}:",
		description=str(primes)[1:-1],
	)


@primes.error
async def pr_error(ctx, error):
	await send(
		ctx,
		"Please make sure your command is set out like this:\n=`primes <limit>`, e.g."
		" `=primes 1000` returns the primes up to 1000.\nThis was the error"
		" encountered:\n ```{error}```",
	)


@bot.command(
	name="nthPowerRange",
	aliases=["npwr"],
	help=(
		"Find the squares, cubes etc. between 2 numbers, e.g. `=npwr 1 1000` for the"
		" squares, cubes, etc. between 1 and 1000."
	),
)
async def powerrange(ctx, start, end, file=""):
	start, end = discordnum(ctx, start, end)
	start_time = time()
	message = ""

	def super(x: str) -> str:
		"""Make a number superscript"""
		return x.translate(x.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))

	for i in range(start, end + 1):
		if i == 1:
			message += "1ⁿ = 1\n"
		for j in range(2, int(i ** 0.5) + 1):
			base = round(abs(i) ** (1 / j))
			if base ** j == abs(i):
				if j % 2 == 0:
					message += f"±{base}{super(str(j))} = {i}\n"
				else:
					message += f"{base}{super(str(j))} = {i}\n"
	await send(
		ctx,
		file,
		f"Time taken: {discordround(ctx, time() - start_time)} seconds",
		title=f"nth powers between {start} and {end}:",
		description=message,
	)


@powerrange.error
async def pwr_error(ctx, error):
	await ctx.send(
		"Please make sure your command is set out like this:\n`=nthPowerRange <first"
		" number> <final number>`\n Example:\n`=npwr 1 1000` to find"
		" squares, cubes etc. between 1 and 100. \nThis was the error encountered:\n"
		f" {str(error)}"
	)


@bot.command(
	name="Evaluate",
	aliases=["ev", "calc", "eval"],
	help=(
		"Do a calculation using Python operators, your own saved variables, and/or the"
		" python `math` module."
	),
)
async def calculation(ctx, *calculation):
	file = calculation[-1]
	calc = " ".join((*calculation[:-1], file.replace("file", "")))
	print(calc)
	ans = discordnum(ctx, calc)
	if type(ans) == float:
		frac = Fraction(str(ans))
		if log10(frac.denominator) % 1:
			if ans < 1:
				await send(
					ctx,
					file,
					title=calc,
					description=f"{frac.numerator}⁄{frac.denominator}\n{ans}",
				)
			else:
				await send(
					ctx,
					file,
					title=calc,
					description=(
						f"{frac.numerator // frac.denominator}"
						f" {frac.numerator % frac.denominator}⁄{frac.denominator}\n{ans}"
					),
				)
		else:
			await send(ctx, file, title=calc, description=ans)
	else:
		await send(ctx, file, title=calc, description=ans)


@calculation.error
async def calculation_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your calculation makes sense and uses python operators,"
			" the math module and/or your own defined variables. \nThis was the error"
			f" encountered:\n```{error}```"
		),
	)


@bot.command(name="CuboidVolume", aliases=["CuV"])
async def CuV(ctx, length, height, width, file=""):
	length, height, width = discordnum(ctx, length, height, width)
	await send(
		ctx,
		file,
		description=f"{length} × {height} × {width} = {length * height * width}",
		title=f"Length of cuboid with length {length}, height {height}, width {width}:",
	)


@CuV.error
async def CuVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:`=CuV <height>"
			f" <width> length>`.\nThis was the error encountered:\n{error}"
		),
		title="Error",
	)


@bot.command(name="PyramidVolume", aliases=["PyV"])
async def PV(ctx, base_area, height, file=""):
	base_area, height = discordnum(ctx, base_area, height)
	await send(
		ctx,
		file,
		description=f"{base_area} × {height} ÷ 3 = {base_area * height / 3}",
		title=f"Volume of pyramid with base area {base_area}, height {height}:",
	)


@PV.error
async def PVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=PV"
			f" <base_area> <height>`.\nThis was the error encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(name="SphereVolume", aliases=["SV"])
async def SV(ctx, radius, file=""):
	radius = discordnum(ctx, radius)
	await send(
		ctx,
		file,
		description=f"4 ÷ 3 × π × {radius}³ = {(4 / 3) * pi * radius ** 3}",
		title=f"Volume of sphere with radius {radius}:",
	)


@SV.error
async def SVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as: `=SV"
			f" <radius>`.\nThis was the error encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(name="ConeVolume", aliases=["CoV"])
async def CoV(ctx, radius, height, file=""):
	radius, height = discordnum(ctx, radius, height)
	await send(
		ctx,
		file,
		description=f"π × {radius}² × {height} ÷ 3 = {pi * radius ** 2 * height / 3}",
		title=f"Volume of cone with radius {radius}, height {height}:",
	)


@CoV.error
async def CoVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=CoV"
			f" <radius> <height>`.\nThis was the error encountered:\n```{error}```"
		),
		title=f"Error",
	)


@bot.command(name="CylinderVolume", aliases=["CyV"])
async def CyV(ctx, radius, height, file=""):
	radius, height = discordnum(ctx, radius, height)
	await send(
		ctx,
		file,
		description=f"π × {radius}² × {height} = {pi * radius ** 2 * height}",
		title=f"Volume of cylinder with radius {radius}, height {height}:",
	)


@CyV.error
async def CyVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=CyV"
			f" <radius> <height>`.\nThis was the error encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(name="PentagonalPrismVolume", aliases=["PPV"])
async def PPV(ctx, height, base_edge_length, file=""):
	height, base_edge_length = discordnum(ctx, height, base_edge_length)
	await send(
		ctx,
		file,
		description=(
			f"5 ÷ 4 × {height} × {base_edge_length}² × (1 + 2 ÷ √5) ="
			f" {(5 / 4) * height * base_edge_length ** 2 * (1 + 2 / sqrt(5))}"
		),
		title=(
			f"Volume of pentagonal prism with height {height}, base edge length"
			" {base_edge_length}:"
		),
	)


@PPV.error
async def PPVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=PPV"
			" <height> <base edge length>`.\nThis was the error"
			f" encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(name="HexagonalPrismVolume", aliases=["HPV"])
async def HPV(ctx, height, base_edge_length, file=""):
	height, base_edge_length = discordnum(ctx, height, base_edge_length)
	await send(
		ctx,
		file,
		description=(
			f"3√3 ÷ 2 × {height} × {base_edge_length}² ="
			f" {(3 * sqrt(3) / 2) * height * base_edge_length ** 2}"
		),
		title=(
			f"Volume of hexagon with height {height}, base edge length"
			f" {base_edge_length}"
		),
	)


@HPV.error
async def HPVError(ctx, error: str):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=HPV"
			" <height> <base edge length>`.\nThis was the error"
			f" encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(
	name="MessageLimit",
	aliases=["ML"],
	help="Set the character limit for messages sent by the bot.",
)
@commands.has_permissions(administrator=True)
async def ML(ctx, limit: int):
	limit = discordnum(ctx, limit)
	serverVars.load("serverVars")
	if limit >= 4000:
		serverVars.removeVar(ctx.message.guild, "MessageLimit")
	else:
		serverVars.set(ctx.message.guild, "MessageLimit", limit)
		serverVars.save("serverVars")
		await ctx.send(
			f"All messages will now be sent as files instead if they exceed {limit}"
			" characters."
		)


@ML.error
async def MLError(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await send(
			ctx,
			title="Permission denied:",
			description=" You are not an admin of this server.",
		)
	else:
		await send(
			ctx,
			title="Error"
			f"""Error: Please make sure your command makes sense and is set out as:`=MessageLimit <limit>`This was the error encountered:\n```{error}```""",
		)


@bot.command(
	name="Variable",
	help=(
		"Save a variable for use in any command, e.g. if you type `=var x 2`, `=ev x *"
		" 3` returns `6`, `=primes x` returns the primes up to 6."
	),
	aliases=["var"],
)
async def var(ctx, var, val):
	userVars.load("userVars")
	userVars.set(ctx.message.author, var, val)
	userVars.save("userVars")


@bot.command(name="RemoveVariable", aliases=["rmvar"])
async def rmvar(ctx, var):
	userVars.load("userVars")
	userVars.removeVar(ctx.message.author, var)
	userVars.save("userVars")


@rmvar.error
async def rmvar_error(ctx, error):
	await ctx.send("Error: variable does not exist.")


@bot.command(
	name="FibonacciGraph",
	aliases=["FibGraph", "FG"],
	help="Generate a graph of the Fibonacci sequence",
)
async def fibonacci_graph(ctx, end, mode="fibonacci", transparent=""):
	end = discordnum(ctx, end)
	filename = f"/tmp/fibgraph {end}{mode[0]} {transparent}.png"
	if not path.exists(filename):
		pyplot.figure(end)
		n1, n2 = 0, 1
		sequence = {}
		if mode == "n":
			for i in range(1, end + 1):
				sequence[i] = n1
				nth = n1 + n2
				n1 = n2
				n2 = nth
		else:
			i = 1
			while n1 < end:
				sequence[i] = n1
				nth = n1 + n2
				n1 = n2
				n2 = nth
				i += 1
			end = n1
		pyplot.ylabel("Fibonacci")
		pyplot.xlabel("n")
		pyplot.title(f"Fibonacci graph up to {end}")
		n = sequence.keys()
		f = sequence.values()
		for a, b in zip(n, f):
			pyplot.text(a, b, str(b))
		pyplot.plot(n, f)
		pyplot.autoscale(tight=True)
		pyplot.savefig(filename, transparent=transparent)
	await ctx.send(file=File(filename))


@fibonacci_graph.error
async def fibgraph_error(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is in the layout:\n"
			" =fibgraph <numbers> <n or fibonacci\nExample: `=fibgraph 20` gives you a"
			" Fibonacci graph up to fibonacci=20.\n`=fibgraph 20 n` gives you a"
			" Fibonacci graph up to n=20. This was the error"
			f" encountered:\n```py\n{error}``"
		),
		title="Error",
	)


@bot.command(name="QuadraticEquation", aliases=["QE", "QuadEq"])
async def QuadEq(ctx, a, b, c):
	a, b, c = discordnum(ctx, a, b, c)
	print(type(a), type(b), type(c))
	d = (b ** 2 - 4 * a * c) ** 0.5
	ans1, ans2 = (d - b) / 2 * a, (-b - d) / 2 * a
	if ans1 == ans2:
		await send(
			ctx,
			title=f"{a}x² + {b}x + {c} = 0: x = {ans1}",
			description=f"({-b} ± √({b}² - 4 × {a} × {c})) ÷ 2 × {a} = **{ans1}**",
		)
	else:
		await send(
			ctx,
			title=f"{a}x² + {b}x + {c} = 0: x = {ans1}, {ans2}",
			description=(
				f"{-b} + √({b}² + 4 × {a} × {c}) ÷ 2 × {a} = **{ans1}**\n"
				f"(√({b}² - 4 × {a} × {c}) - {b}) ÷ 2 × {a} = **{ans2}**"
			),
		)


@QuadEq.error
async def QE_error(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is in the layout:\n"
			" `=quadeq <a> <b> <c>`.\nExample: `=quadeq 2 4 2` returns `-4.0`, the"
			" answer to the equation 2x² + 4x + 2.\nThis was the error"
			f" encountered:\n```{error}```"
		),
		title="Error",
	)


@bot.command(
	name="RoundTo",
	help=(
		"Select a number of decimal places or significant figures to round all"
		" calculations to, e.g. `=roundto 3sf` for 3 significant figures, or `=roundto"
		" 5dp` for 5 decimal places."
	),
	aliases=["RT"],
)
async def round_to(ctx, amount):
	assert amount[-2:] in ["sf", "dp"]
	userVars.load("userVars")
	userVars.set(ctx.message.author, "RoundTo", amount)
	userVars.save("userVars")


@round_to.error
async def roundto_error(ctx, error: str):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your command makes sense and is in the format: `=roundto"
			" <integer><sf or dp>, e.g. `=roundto 3sf` for 3 significant figures, or"
			" `=roundto 5dp` for 5 decimal places.\nThis was the error encountered:"
			f" ```{error}```"
		),
	)


@bot.command(
	name="EmbedColour",
	aliases=["EmbedColor", "EC"],
	help=(
		"Set the embed colour to an rgb colour, e.g. `=ec 185 242 255` for a diamond"
		" colour."
	),
)
async def embed_colour(ctx, red, green, blue):
	colour = Colour.from_rgb(*discordnum(ctx, red, green, blue))
	userVars.load("userVars")
	userVars.set(ctx.message.author, "colour", colour)
	userVars.save("userVars")
	serverVars.set(ctx.message.guild, "colours", colours + [colour])


bot.run(environ["TOKEN"])
