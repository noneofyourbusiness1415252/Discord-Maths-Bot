from os import environ, path
from discord.ext import commands
from discord import File, Embed
from discord import Colour
from discord_variables_plugin import GlobalUserVariables, ServerVariables
from matplotlib import pyplot
from math import *
from random import randint
import logging, logging.handlers
from flask import Flask
from threading import Thread
from time import time
from fractions import Fraction
from timeit import timeit
from maths_stuff import *

app = Flask("Discord Maths Bot")


@app.route("/")
def display_logs():
	return open("discord.log").read()


Thread(target=lambda: app.run("0.0.0.0")).start()
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("./discord.log", "a", 32768, 1)
handler.setFormatter(
	logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot = commands.Bot(command_prefix="=", case_insensitive=True)
serverVars = ServerVariables()
userVars = GlobalUserVariables()


def discordround(ctx, num):
	userVars.load("userVars.json")
	try:
		roundto = userVars.get(ctx.message.author, "RoundTo")
	except:
		return num if type(num) in {complex, float} else int(num)
	digits = int(roundto[:-2])
	if roundto.endswith("sf"):
		format = f"%.{digits}g"
		if type(num) == complex:
			return float(format % num.real) + float(format % num.imag) * 1j
		asfloat = float(format % num)
		return asfloat if asfloat % 1 else int(asfloat)
	if type(num) == complex:
		return round(num.real, digits) + round(num.imag, digits) * 1j
	asfloat = round(num, digits)
	return asfloat if asfloat % 1 else int(asfloat)


def discordnum(ctx, *calc):
	userVars.load("userVars.json")
	answers = []
	for i in calc:
		while True:
			try:
				ans = eval(str(i))
			except NameError as e:
				for j in str(e).split():
					if "'" in j:
						var = j.replace("'", "")
						break
				i = i.replace(var, userVars.get(ctx.message.author, var))
			else:
				answers.append(ans)
				break
	if len(answers) == 1:
		return answers[0]
	return answers


async def send(ctx, file="", footer="", **embed):
	await ctx.channel.trigger_typing()
	author = ctx.message.author
	userVars.load("userVars.json")
	try:
		embed = Embed(**embed, colour=userVars.get(author, "colour"))
	except KeyError:
		colour = Colour.random()
		embed = Embed(**embed, colour=colour)
		userVars.set(author, "colour", colour)
		userVars.save("userVars.json")
	embed.set_footer(text=footer)
	try:
		limit = serverVars.get(ctx.message.guild, "MessageLimit")
	except KeyError:
		limit = 4000
	if len(embed) > limit or file == "file":
		open(f"/tmp/{ctx.message.id}.md", "w+").write(
			f"**{embed.title if embed.title!=Embed.Empty else''}**\n{embed.description}\n{footer}"
		)
		if file:
			return await ctx.reply(file=File(f"/tmp/{ctx.message.id}.md"))
		return await ctx.reply(
			f"Message would be over {limit} characters, so sending in file"
			" instead",
			file=File(f"/tmp/{ctx.message.id}.md"),
		)
	return await ctx.reply(embed=embed)


@bot.event
async def on_ready():
	print(f"We have logged in as", bot.user)


@bot.command(
	name="Primes",
	help=(
		"Find primes up to, **but not including**, a number. Example:\n`=primes"
		" 1000` for primes up to `1000`, `=primes 10000 file` to put the primes"
		" up to `10000` in a file."
	),
)
async def primes(
	ctx,
	limit,
	file="",
	help="Find primes up to a number, e.g. `primes 1000` for t",
):
	limit = int(discordnum(ctx, limit))
	start_time = time()
	primes = primesupto(limit + 1)
	await send(
		ctx,
		file,
		f"Time taken: {discordround(ctx,time()-start_time)}",
		title=f"{len(primes)} primes up to {limit}:",
		description=str(primes)[1:-1],
	)


@primes.error
async def pr_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your command is set out like this:\n=`primes"
			" <limit>`, e.g. `=primes 1000` returns the primes up to"
			f" 1000.\nThis was the error encountered:\n ```diff\n-{error}```"
		),
	)


@bot.command(
	name="nthPowerRange",
	aliases=["npwr"],
	help=(
		"Find the squares, cubes etc. between 2 numbers, e.g. `=npwr 1 1000`"
		" for the squares, cubes, etc. between 1 and 1000."
	),
)
async def powerrange(ctx, start, end, file=""):
	await send(
		ctx,
		file,
		title=f"nth powers between {start} and {end}:",
		description=nthpowers(*discordnum(ctx, start, end)),
	)


@powerrange.error
async def pwr_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=f"""Please make sure your command is set out like this:
`=nthPowerRange <first number> <final number>`
 Example:
`=npwr 1 1000` to find squares, cubes etc. between 1 and 100. 
This was the error encountered:
  {str(error)}""",
	)


@bot.command(
	name="Evaluate",
	aliases=["ev", "calc", "eval"],
	help=(
		"Do a calculation using Python operators, your own saved variables, and"
		" python modules."
	),
)
async def calculation(ctx, *calculation):
	file = calculation[-1]
	calc = " ".join((*calculation[:-1], file.replace("file", "")))
	unrounded = discordnum(ctx, calc)
	footer = ""
	ans = discordround(ctx, unrounded)
	if unrounded != ans:
		footer = f"Rounding to {userVars.get(ctx.message.author,'RoundTo')}"
	if type(ans) == float:
		frac = Fraction(str(ans))
		if log10(frac.denominator) % 1:
			if ans < 1:
				description = f"{frac.numerator}⁄{frac.denominator}\n{ans}"
			else:
				description = (
					f"{frac.numerator//frac.denominator} {frac.numerator%frac.denominator}⁄{frac.denominator}\n{ans}"
				)
		else:
			description = ans
	else:
		description = ans
	await send(ctx, file, footer, description=description)


@calculation.error
async def calculation_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your calculation makes sense and uses python"
			" operators, the math module and/or your own defined variables."
			f" \nThis was the error encountered:\n```diff\n-{error}```"
		),
	)


@bot.command(name="CuboidVolume", aliases=["CuV"])
async def CuV(ctx, length, height, width, file=""):
	length, height, width = discordnum(ctx, length, height, width)
	await send(
		ctx,
		file,
		description=(
			f"{length} × {height} × {width} ="
			f" {discordround(ctx,length*height*width)}"
		),
		title=(
			f"Length of cuboid with length {length}, height {height}, width"
			f" {width}:"
		),
	)


@CuV.error
async def CuVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:`=CuV"
			" <height> <width> length>`.\nThis was the error"
			f" encountered:\n{error}"
		),
		title="Error",
	)


@bot.command(name="PyramidVolume", aliases=["PyV"])
async def PV(ctx, base_area, height, file=""):
	base_area, height = discordnum(ctx, base_area, height)
	await send(
		ctx,
		file,
		description=(
			f"{base_area} × {height} ÷ 3 ="
			f" {discordround(ctx,base_area*height/3)}"
		),
		title=f"Volume of pyramid with base area {base_area}, height {height}:",
	)


@PV.error
async def PVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as:\n`=PV"
			" <base_area> <height>`.\nThis was the error"
			" encountered:\n```diff\n-{error}```"
		),
		title="Error",
	)


@bot.command(name="SphereVolume", aliases=["SV"])
async def SV(ctx, radius, file=""):
	radius = discordnum(ctx, radius)
	await send(
		ctx,
		file,
		description=(
			f"4 ÷ 3 × π × {radius}³ = {discordround(ctx,4/3*pi*radius**3)}"
		),
		title=f"Volume of sphere with radius {radius}:",
	)


@SV.error
async def SVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out as: `=SV`"
			" <radius>`.\nThis was the error encountered:\n```diff\n-{error}```"
		),
		title="Error",
	)


@bot.command(name="ConeVolume", aliases=["CoV"])
async def CoV(ctx, radius, height, file=""):
	radius, height = discordnum(ctx, radius, height)
	await send(
		ctx,
		file,
		description=(
			f"π × {radius}² × {height} ÷ 3 ="
			f" {discordround(ctx,pi*radius**2*height/3)}"
		),
		title=f"Volume of cone with radius {radius}, height {height}:",
	)


@CoV.error
async def CoVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out"
			" as:\n`=CoV <radius> <height>`.\nThis was the error"
			f" encountered:\n```diff\n-{error}```"
		),
		title=f"Error",
	)


@bot.command(name="CylinderVolume", aliases=["CyV"])
async def CyV(ctx, radius, height, file=""):
	radius, height = discordnum(ctx, radius, height)
	await send(
		ctx,
		file,
		description=(
			f"π × {radius}² × {height} ="
			f" {discordround(ctx,pi*radius**2*height)}"
		),
		title=f"Volume of cylinder with radius {radius}, height {height}:",
	)


@CyV.error
async def CyVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out"
			" as:\n`=CyV <radius> <height>`.\nThis was the error"
			f" encountered:\n```diff\n-{error}```"
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
			f" {discordround(ctx,5/4*height*base_edge_length**2*(1+2/sqrt(5)))}"
		),
		title=(
			f"Volume of pentagonal prism with height {height}, base edge length"
			" {base_edge_length}:"
		),
	)


@PPV.error
async def PPVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out"
			" as:\n`=PPV <height> <base edge length>`.\nThis was the error"
			f" encountered:\n```diff\n-{error}```"
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
			f" {discordround(ctx,3*sqrt(3)/2*height*base_edge_length**2)}"
		),
		title=(
			f"Volume of hexagon with height {height}, base edge length"
			f" {base_edge_length}"
		),
	)


@HPV.error
async def HPVError(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is set out"
			" as:\n`=HPV <height> <base edge length>`.\nThis was the error"
			f" encountered:\n```diff\n-{error}```"
		),
		title="Error",
	)


@bot.command(
	name="MessageLimit",
	aliases=["ML"],
	help="Set the character limit for messages sent by the bot.",
)
@commands.has_permissions(administrator=True)
async def ML(ctx, limit):
	limit = discordnum(ctx, limit)
	serverVars.load("serverVars.json")
	if limit >= 4000:
		serverVars.removeVar(ctx.message.guild, "MessageLimit")
	else:
		serverVars.set(ctx.message.guild, "MessageLimit", limit)
		serverVars.save("serverVars.json")
		await ctx.send(
			"All messages will now be sent as files instead if they exceed"
			f" {limit} characters."
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
			title=(
				"Error: Please make sure your command makes sense and is set"
				" out as: `=MessageLimit <limit>` This was the error"
				f" encountered:\n```diff\n-{error}```"
			),
		)


@bot.command(
	name="Variable",
	help=(
		"Save a variable for use in any command, e.g. if you type `=var x 2`,"
		" `=ev x * 3` returns `6`, `=primes x` returns the primes up to 6."
	),
	aliases=["var"],
)
async def var(ctx, var, val):
	userVars.load("userVars.json")
	userVars.set(ctx.message.author, var, val)
	userVars.save("userVars.json")


@bot.command(name="RemoveVariable", aliases=["rmvar"])
async def rmvar(ctx, var):
	userVars.load("userVars.json")
	userVars.removeVar(ctx.message.author, var)
	userVars.save("userVars.json")


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
		for (a, b) in zip(n, f):
			pyplot.text(a, b, str(b))
		pyplot.plot(n, f)
		pyplot.autoscale(tight=True)
		pyplot.savefig(filename, transparent=transparent)
	await ctx.send(file=File(filename))


@fibonacci_graph.error
async def fibgraph_error(ctx, error):
	await send(
		ctx,
		description=f"""Please make sure your command makes sense and is in the layout:
=fibgraph <numbers> <n or fibonacci>
Example: `=fibgraph 20` gives you a Fibonacci graph up to fibonacci=20.
`=fibgraph 20 n` gives you a Fibonacci graph up to n=20.
This was the error encountered:
```diff\n{error}```""",
		title="Error",
	)


@bot.command(name="QuadraticEquation", aliases=["QE", "QuadEq"])
async def QuadEq(ctx, a, b, c):
	a, b, c = discordnum(ctx, a, b, c)
	d, dbla = (b**2 - 4 * a * c) ** 0.5, 2 * a
	ans1, ans2 = discordround(ctx, (d - b) / dbla), discordround(
		ctx, (-b - d) / dbla
	)
	if ans1 == ans2:
		await send(
			ctx,
			title=f"{a}x² + {b}x + {c} = 0: x = {ans1}",
			description=(
				f"({-b} ± √({b}² - 4 × {a} × {c})) ÷ 2 × {a} = **{ans1}**"
			),
		)
	else:
		await send(
			ctx,
			title=f"{a}x² + {b}x + {c} = 0: x = {ans1}, {ans2}",
			description=(
				f"{-b} + √({b}² + 4 × {a} × {c}) ÷ 2 × {a} ="
				f" **{ans1}**\n(√({b}² - 4 × {a} × {c}) - {b}) ÷ 2 × {a} ="
				f" **{ans2}**"
			),
		)


@QuadEq.error
async def QE_error(ctx, error):
	await send(
		ctx,
		description=(
			"Please make sure your command makes sense and is in the layout:\n"
			" `=quadeq <a> <b> <c>`.\nExample: `=quadeq 2 4 2` returns `-4.0`,"
			" the answer to the equation 2x² + 4x + 2.\nThis was the error"
			f" encountered:\n```diff\n-{error}```"
		),
		title="Error",
	)


@bot.command(
	name="RoundTo",
	help=(
		"Select a number of decimal places or significant figures to round all"
		" calculations to, e.g. `=roundto 3sf` for 3 significant figures, or"
		" `=roundto 5dp` for 5 decimal places."
	),
	aliases=["RT"],
)
async def round_to(ctx, amount):
	assert amount[-2:] in ["sf", "dp"]
	userVars.load("userVars.json")
	userVars.set(ctx.message.author, "RoundTo", amount)
	userVars.save("userVars.json")


@round_to.error
async def roundto_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your command makes sense and is in the format:"
			" `=roundto <integer><sf or dp>, e.g. `=roundto 3sf`or 3"
			" significant figures, or `=roundto 5dp` for 5 decimal"
			f" places.\nThis was the error encountered: ```diff\n-{error}```"
		),
	)


@bot.command(
	name="EmbedColour",
	aliases=["EmbedColor", "EC"],
	help=(
		"Set the embed colour to an rgb colour, e.g. `=ec 185 242 255` for a"
		" diamond colour."
	),
)
async def embed_colour(ctx, red, green, blue):
	colour = Colour.from_rgb(*discordnum(ctx, red, green, blue))
	userVars.load("userVars.json")
	userVars.set(ctx.message.author, "colour", colour)
	userVars.save("userVars.json")


@bot.command(
	name="TimeMeOn",
	help=(
		"Times you on how long you take to find the correct answer to a random"
		" calculation. The first arguments are the calculation, with '?'"
		" expanding to a random number, and the last argument is the range for"
		" the random number, in the format `start..end`. For example `=timemeon"
		" ? * ? 2..12` tests you on your 2-12 times tables."
	),
)
async def test_on(ctx, *calculation):
	serverVars.load("serverVars.json")
	calc = " ".join(calculation[:-1])
	limit = calculation[-1].split("..")
	i = 0
	vars = {}
	while i < len(calc):
		if calc[i] == "?":
			letter = calc[i + 1]
			if not letter in vars:
				vars[letter] = str(randint(*discordnum(ctx, *limit)))
			calc = calc[:i] + vars[letter] + calc[i + 2 :]
			print(calc, vars)
		else:
			i += 1
	bot_time = time()
	answer = discordround(ctx, discordnum(ctx, calc))
	bot_time = discordround(ctx, time() - bot_time)
	await send(ctx, title=f"What is {calc}?")
	attempts = 1
	player_time = time()
	while answer != discordround(
		ctx,
		complex(
			(
				await bot.wait_for(
					"message",
					check=lambda m: m.channel.id == ctx.channel.id
					and m.author == ctx.message.author,
				)
			).content.replace(" ", "")
		),
	):
		await send(
			ctx,
			title="Incorrect! :negative_squared_cross_mark:",
			description="Try again!",
		)
		attempts += 1
	await send(
		ctx,
		title="Correct! :white_check_mark:",
		description=(
			f"That took you **{attempts}** attempt(s), and"
			f" **{discordround(ctx,time()-player_time)}** seconds.\nI took"
			f" **{bot_time}** seconds."
		),
	)


@test_on.error
async def test_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your command makes sense and is in the format:"
			" `=testmeon <calculation> <limit of randoms>`\nExample: `=timemeon"
			" ?*? 2..12` tests you on 2-12 times tables.\n This was the error"
			f" encountered:\n```diff\n-{error}```"
		),
	)


@bot.command(name="LanguageSpeedComparison", aliases=["LSC"])
async def lsc(ctx, limit, *langs):
	message, limit = "", int(discordnum(ctx, limit))
	if len(langs) == 0 or langs[0] == "all":
		langs = [
			"C",
			"C++",
			"Rust",
			"Go",
			"Nodejs",
			"C#",
			"Ruby",
			"Python",
			"Java",
			"Kotlin",
		]
	else:
		langs = list(langs)
		for i in range(len(langs)):
			langs[i] = langs[i][0].upper() + langs[i][1:].lower()
	times = {}
	for i in langs:
		if i == "Python":
			args = "'python', 'primes.py'"
		elif i in {"Java", "Kotlin"}:
			args = f"'{i.lower()}', '-cp', '{i}', 'primes'"
		elif i == "Nodejs":
			args = "'node', 'primes.js'"
		elif i == "Ruby":
			args = "'ruby', 'primes.rb'"
		elif i == "C#":
			args = "'mono', 'C#/primes.exe'"
		else:
			args = f"'./{i}/primes'"
		try:
			times[i] = timeit(
				f"run([{args}, '{limit}'], stderr=DEVNULL, stdout=DEVNULL,"
				" check=True)",
				setup="from subprocess import DEVNULL, run",
				number=1,
			)
		except Exception as err:
			message += f"{i}:\n> ```diff\n-{str(err)}```\n"
			continue
		fastest = min(times, key=times.get)
	for i in sorted(times, key=times.get):
		message += (
			f"**{i}**: \n> Time taken: {discordround(ctx,times[i])}\n>"
			f" Multiplier: {discordround(ctx,times[i]/times[fastest])}\n"
		)
	await send(
		ctx,
		title=f"Language speed comparison, checking primes up to {limit}",
		description=message,
	)


@lsc.error
async def lsc_error(ctx, error):
	await send(
		ctx,
		title="Error",
		description=(
			"Please make sure your command makes sense and is in the format"
			" `=lsc <limit> <languages...>`.\nExample: `=lsc 100 Rust C++` to"
			" compare Rust and C++ on listing primes up to 100\nThis was the"
			f" error encountered: {error}"
		),
	)


bot.run(environ["TOKEN"])
