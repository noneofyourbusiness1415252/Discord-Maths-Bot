from http import server
from threading import Thread

Thread(
	target=server.HTTPServer(
		("", 0), server.SimpleHTTPRequestHandler
	).serve_forever
).start()
from os import environ, path
from discord.commands import permissions
from discord import File, Embed, Colour, Bot, Intents
from discord.commands import Option
from discord_variables_plugin import GlobalUserVariables, ServerVariables
from matplotlib import pyplot
from math import *
from random import randint
from logging import handlers, DEBUG, getLogger, Formatter
from time import time
from fractions import Fraction
from timeit import timeit
from maths_stuff import *
from ast import literal_eval
from logging import handlers, DEBUG, getLogger, Formatter

logger = getLogger("discord")
logger.setLevel(DEBUG)
handler = handlers.RotatingFileHandler("./discord.log", "a", 32768, 1)
handler.setFormatter(
	Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot = Bot(intents=Intents(message_content=True, messages=True))
file_option = Option(
	bool,
	"Whether or not you want the result to be sent in a file.",
	default=False,
)
serverVars = ServerVariables()
userVars = GlobalUserVariables()


def discordround(ctx, num):
	userVars.load("userVars.json")
	try:
		roundto = userVars.get(ctx.author, "RoundTo")
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
				answers.append(eval(str(i)))
				break
			except NameError as e:
				for j in str(e).split():
					if "'" in j:
						var = j.replace("'", "")
						break
				i = i.replace(var, userVars.get(ctx.author, var))
	return answers[0] if len(answers) == 1 else answers


async def send(ctx, file=False, footer="", **embed):
	userVars.load("userVars.json")
	try:
		embed = Embed(**embed, colour=userVars.get(ctx.author, "colour"))
	except KeyError:
		colour = Colour.random()
		embed = Embed(**embed, colour=colour)
		userVars.set(ctx.author, "colour", colour)
		userVars.save("userVars.json")
	embed.set_footer(text=footer)
	try:
		limit = serverVars.get(ctx.guild, "MessageLimit")
	except KeyError:
		limit = 4096
	if len(embed) > limit or file:
		open(f"/tmp/{ctx.interaction.id}.md", "w+").write(
			f"**{embed.title or ''}**\n{embed.description}\n{footer}"
		)
		try:
			return await ctx.respond(file=File(f"/tmp/{ctx.interaction.id}.md"))
		except:
			return await ctx.send(file=File(f"/tmp/{ctx.interaction.id}.md"))
	try:
		return await ctx.respond(embed=embed)
	except:
		return await ctx.send(embed=embed)


@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")


@bot.event
async def on_application_command_error(ctx, error):
	await send(
		ctx,
		title="Error :negative_squared_cross_mark:",
		description=(
			f"```diff\n-{' '.join(str(error).split()[5:])}```\nIf you're sure"
			" your"
			" command makes"
			" sense, kindly report a bug"
			" [here](https://github.com/noneofyourbusiness1415252/Discord-Maths-Bot/issues/new?assignees=noneofyourbusiness1415252&labels=bug&template=bug_report.md)."
		),
	)


@bot.command()
async def primes(
	ctx, mode: Option(str, choices=["first", "until"]), end, file: file_option
):
	"Find the first n primes, or the primes up to n"
	start_time = time()
	end = int(discordnum(ctx, end))
	primelist = (
		primesupto(end + 1)
		if mode == "until"
		else primesupto(int(end * log(end) + end * log(log(end))))[:end]
	)
	await send(
		ctx,
		file,
		f"Time taken: {discordround(ctx,time()-start_time)}",
		title=f"{len(primelist)} primes:",
		description=str(primelist)[1:-1],
	)


@bot.command()
async def nthpowersbetween(
	ctx,
	start: Option(str, "The start of the range to find nth powers"),
	end: Option(str, "The end of the range"),
	file: file_option,
):
	"Find the squares, cubes etc. between 2 numbers"
	start, end = int(discordnum(ctx, start)), int(discordnum(ctx, end))
	await send(
		ctx,
		file,
		title=f"nth powers between {start} and {end}:",
		description=nthpowers(start, end),
	)


@bot.command()
async def calculate(ctx, calculation, file: file_option):
	"Evaluate a calculation using your saved variables, Python operators, and Python `math` functions."
	await ctx.defer()
	unrounded = discordnum(ctx, calculation)
	footer = ""
	ans = discordround(ctx, unrounded)
	if unrounded != ans:
		footer = f"Rounding to {userVars.get(ctx.author,'RoundTo')}"
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


volume = bot.create_group("volume")


@volume.command()
async def cuboid(ctx, length, height, width, file: file_option):
	length, height, width = discordnum(ctx, length, height, width)
	await send(
		ctx,
		file,
		description=(
			f"{length} × {height} × {width} ="
			f" {discordround(ctx,length*height*width)}"
		),
	)


@volume.command()
async def pyramid(
	ctx, height, vertices_count, base_edge_length, file: file_option
):
	height, vertices_count, base_edge_length = discordnum(
		ctx, height, vertices_count, base_edge_length
	)
	await send(
		ctx,
		file,
		description=(
			f"{height} × {vertices_count} × {base_edge_length}² × 1 ÷ tan(π ÷"
			f" {vertices_count} rad) ÷"
			" 12 ="
			f" {discordround(ctx,height*vertices_count*base_edge_length**2*1/tan(pi/vertices_count)/12)}"
		),
	)


@volume.command()
async def sphere(ctx, radius, file: file_option):
	radius = discordnum(ctx, radius)
	await send(
		ctx,
		file,
		description=(
			f"4 ÷ 3 × π × {radius}³ = {discordround(ctx,4/3*pi*radius**3)}"
		),
		title=f"Volume of sphere with radius {radius}:",
	)


@volume.command()
async def cone(ctx, radius, height, file: file_option):
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


@volume.command()
async def cylinder(ctx, radius, height, file: file_option):
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


@volume.command()
async def pentagonalprism(ctx, height, base_edge_length, file: file_option):
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
			f" {base_edge_length}:"
		),
	)


@volume.command()
async def hexagonalprism(ctx, height, base_edge_length, file=""):
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


@bot.command()
@permissions.is_owner()
async def messagecharacterlimit(ctx, limit):
	"Set the character limit for messages sent by the bot before reverting to sending a file"
	limit = discordnum(ctx, limit)
	serverVars.load("serverVars.json")
	if limit > 4095:
		limit = 4096
		serverVars.removeVar(ctx.guild, "MessageLimit")
	else:
		serverVars.set(ctx.guild, "MessageLimit", limit)
		serverVars.save("serverVars.json")
	await send(
		ctx,
		description=(
			"All messages will now be sent as files instead if they exceed"
			f" {limit} characters."
		),
	)


variable = bot.create_group("variable")


@variable.command()
async def add(ctx, name, value):
	"Save a variable for use in any command"
	userVars.load("userVars.json")
	userVars.set(ctx.author, name, value)
	userVars.save("userVars.json")


@variable.command()
async def remove(ctx, name):
	userVars.load("userVars.json")
	userVars.removeVar(ctx.author, name)
	userVars.save("userVars.json")


@bot.command()
async def fibonaccigraph(
	ctx,
	mode: Option(
		str,
		"'until' for fibonacci numbers up to 'end', 'first' for first 'end'"
		" fibonacci numbers.",
		choices=["until", "first"],
	),
	end,
	transparent: Option(bool, default=True),
):
	"Generate a graph of the first n fibonacci numbers, OR the fibonacci numbers up to n."
	end = discordnum(ctx, end)
	filename = f"/tmp/fibgraph{mode}{end}{transparent}.png"
	if not path.exists(filename):
		pyplot.figure(end)
		n1, n2 = 0, 1
		sequence = {}
		if mode == "first":
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
		pyplot.title(
			f"First {end} fibonacci numbers"
			if mode == "first"
			else f"Fibonacci numbers up to {end}"
		)
		n, f = zip(*sequence.items())
		for a, b in zip(n, f):
			pyplot.text(a, b, str(b))
		pyplot.plot(n, f)
		pyplot.autoscale(tight=True)
		pyplot.savefig(filename, transparent=transparent)
	await ctx.send(file=File(filename))


@bot.command()
async def quadraticequation(ctx, a, b, c):
	"Solve a quadratic equation of the form ax² + bx + c = 0"
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
				f"(-{b} ± √({b}² - 4 × {a} × {c})) ÷ 2 × {a} = **{ans1}**"
			),
		)
	else:
		await send(
			ctx,
			title=f"{a}x² + {b}x + {c} = 0: x = {ans1}, {ans2}",
			description=(
				f"-{b} + √({b}² + 4 × {a} × {c}) ÷ 2 × {a} ="
				f" **{ans1}**\n(√({b}² - 4 × {a} × {c}) - {b}) ÷ 2 × {a} ="
				f" **{ans2}**"
			),
		)


@bot.command()
async def roundto(
	ctx,
	amount,
	mode: Option(str, choices=["significant figures", "decimal places"]),
):
	"Set how to round all calculations made by this bot for you."
	userVars.load("userVars.json")
	userVars.set(
		ctx.author,
		"RoundTo",
		amount + ("dp" if mode == "decimal places" else "sf"),
	)
	userVars.save("userVars.json")


@bot.command()
async def embedcolour(ctx, red, green, blue):
	"Set the embed colour to an rgb colour. Use prefix '0x' for hex values."
	colour = Colour.from_rgb(*discordnum(ctx, red, green, blue))
	userVars.load("userVars.json")
	userVars.set(ctx.author, "colour", colour)
	userVars.save("userVars.json")


@bot.command()
async def timemeon(
	ctx,
	calculation: Option(
		str,
		"The calculation. Example: ?a * ?b * ?c for a multiplication of 3"
		" random numbers.",
	),
	start: Option(str, "Lowest value for randoms"),
	end: Option(str, "Highest value for randoms"),
):
	"Times you on finding the correct answer to a random calculation."
	serverVars.load("serverVars.json")
	i = 0
	vars = {}
	while i < len(calculation):
		if calculation[i] == "?":
			letter = calculation[i + 1]
			if not letter in vars:
				vars[letter] = str(randint(*discordnum(ctx, start, end)))
			calculation = calculation[:i] + vars[letter] + calculation[i + 2 :]
		else:
			i += 1
	bot_time = time()
	answer = discordround(ctx, discordnum(ctx, calculation))
	bot_time = discordround(ctx, time() - bot_time)
	await send(ctx, title=f"What is {calculation}?")
	attempts = 1
	player_time = time()
	while answer != discordround(
		ctx,
		literal_eval(
			(
				await bot.wait_for(
					"message",
					check=lambda m: m.author == ctx.author
					and m.channel == ctx.channel,
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


@bot.command()
async def languagespeedcomparison(
	ctx,
	limit,
	langs: Option(str, "Separate language names with spaces", default="all"),
):
	"Benchmark 14 programming languages using primes calculator"
	message, limit = "", int(discordnum(ctx, limit))
	if langs == "all":
		langs = [
			"C",
			"C++",
			"Rust",
			"Go",
			"Swift",
			"Java",
			"C♯",
			"PHP",
			"Kotlin",
			"Dart",
			"Node.js",
			"Python",
			"Ruby",
			"R",
		]
	else:
		langs = langs.split()
		for i in range(len(langs)):
			langs[i] = langs[i][0].upper() + langs[i][1:].lower()
	times = {}
	for i in langs:
		if i == "Python":
			args = "python primes.py"
		elif i in {"Java", "Kotlin"}:
			args = f"{i.lower()} -cp {i} primes"
		elif i == "Node.js":
			args = "node primes.js"
		elif i == "Ruby":
			args = "ruby primes.rb"
		elif i == "Dart":
			args = "dart Dart/primes"
		elif i == "PHP":
			args = "php primes.php"
		elif i == "R":
			args = "Rscript primes.r"
		else:
			args = f"{i}/primes"
		try:
			times[i] = timeit(
				f"run({args.split() + [str(limit)]}, stderr=DEVNULL,"
				" stdout=DEVNULL, check=True)",
				setup="from subprocess import DEVNULL, run",
				number=1,
			)
		except Exception as err:
			message += f"{i}:\n> ```{err}```\n"
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


try:
	bot.run(environ["TOKEN"])
except:
	print("Rate-limit detected. Restarting repl")
	from os import kill

	kill(1, 15)
