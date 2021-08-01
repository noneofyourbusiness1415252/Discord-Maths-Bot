#!/usr/bin/env python3
from os import system, name, environ
try:
	from discord.ext import commands
except ModuleNotFoundError:
	print('discord.py is not installed. Installing...')
	check_pip=str(system('python3 -m pip -V'))
	if not '0' in check_pip:
		system('curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py ; python3 get-pip.py')
	install_discord = str(system("python3 -m pip install 'discord.py'"))
	if not '0' in install_discord:
		print('Error while installing discord.py.\a')
		exit()
	from discord.ext import commands
import logging
from cmath import *  # @UnusedWildImport
import random
from time import sleep
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix='=')


@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))


@bot.command(name='primerange')
async def primerange(ctx, num1: int, num2: int):
	await ctx.channel.trigger_typing()

	def PrimeOrComposite(n):
		if n == 2 or n == 3:
			return('is a prime number.')
		if n < 2 or n % 2 == 0:
			return('is a composite number.')
		if n < 9:
			return('is a prime number.')
		if n % 3 == 0:
			return('is a composite number.')
		r = int(n ** 0.5)
		f = 5
		while f <= r:
			if n % f == 0:
				return('is a composite number.')
			if n % (f + 2) == 0:
				return('is a composite number.')
			f += 6
		return('is a prime number.')

	async def PrimeRange(num1, num2):
		amount = 0
		primes = ('These are the prime numbers between' + str(num1) + ' and ' + str(num2) + ': ')
		for l in range(num1, num2 + 1):
			if PrimeOrComposite(l) == 'is a prime number.':
				amount = amount + 1
				primes = primes + str(l) + ', '
		if amount == 1:
			await ctx.send('There is 1 prime number between ' + str(num1) + ' and ' + str(num2) + '.')
		else:
			await ctx.send('There are ' + str(amount) + ' prime numbers between ' + str(num1) + ' and ' + str(num2) + '.')
		await ctx.channel.trigger_typing()
		global Total
		Total = ''.join(primes)

	await PrimeRange(num1, num2)
	if len(Total) > 2000:
		await ctx.send('There are too many numbers to print, so it can not be fit into one message.')
		j = 0
		for i in range(1, int(len(Total) / 2000) + 1):
			await ctx.send(str(Total)[j:i * 2000])
			j = i * 2000
	else:
		await ctx.send(str(Total))


@primerange.error
async def pr_error(ctx, error):
	await ctx.send('Please make sure your command is set out like this:\n=primerange <first number> <final number>\nThis was the error encountered:\n' + str(error))


@bot.command(name='pr')
async def pr(ctx, num1:int, num2:int):
	await primerange(ctx, num1, num2)


@pr.error
async def PR_Error(ctx, error):
	await pr_error(ctx, error)


@bot.command(name='powerrange')
async def powerrange(ctx, num1:int, num2:int):
	await ctx.channel.trigger_typing()

	def SquareOrCube(n):
		if abs(n ** (1 / 6)) == int(abs(n ** (1 / 6))):
			return('is a power of 6, so it is both a square number and a cube number.')
		elif abs(n ** 0.5) == int(abs(n ** 0.5)):
			return('is a square number.')
		elif abs(n ** (1 / 3)) == int(abs(n ** (1 / 3))):
			return('is a cube number.')
		else:
			return('is not a square or cube number.')

	async def PowerRange(num1, num2):
		global totallist
		cubes = 0
		squares = 0
		CubeNumbers = 'The cube numbers between ' + str(num1) + ' and ' + str(num2) + ' are: '
		SquareNumbers = 'The square numbers between ' + str(num1) + ' and ' + str(num2) + ' are: '
		for l in range(num1, num2 + 1):
			if SquareOrCube(l) == 'is a power of 6, so it is both a square number and a cube number.':
				squares = squares + 1
				cubes = cubes + 1
				SquareNumbers = SquareNumbers + str(l) + ', '
				CubeNumbers = CubeNumbers + str(l) + ', '
		for l in range(num1, num2 + 1):
			if SquareOrCube(l) == 'is a cube number.':
				cubes = cubes + 1
				CubeNumbers = CubeNumbers + str(l) + ', '
		for l in range(num1, num2 + 1):
			if SquareOrCube(l) == 'is a square number.':
				squares = squares + 1
				SquareNumbers = SquareNumbers + str(l) + ', '
		total = ('There are ' + str(cubes) + ' cube numbers, and ' + str(squares) + ' square numbers between ' + str(num1) + ' and ' + str(num2) + '.')
		await ctx.send(''.join(total))
		await ctx.channel.trigger_typing()
		totallist = CubeNumbers + '\n' + SquareNumbers

	await PowerRange(num1, num2)
	if len(totallist) > 2000:
		await ctx.send('There are too many numbers to print, so it can not be fit into one message.')
		j = 0
		for i in range(1, int(len(totallist) / 2000) + 1):
			await ctx.send(str(totallist)[j:i * 2000])
			j = i * 2000
	else:
		await ctx.send(totallist)


@powerrange.error
async def powerrange_error(ctx, error):
	await ctx.send('Please make sure your command is set out like this:\n=powerrange <first number> <final number>\nThis was the error encountered:\n' + str(error))


@bot.command(name='pwr')
async def pwr(ctx, num1:int, num2:int):
	await powerrange(ctx, num1, num2)


@pwr.error
async def pwr_error(ctx, error):
	await powerrange_error(ctx, error)


@bot.command(name='eval')
async def formula(ctx, formula):
	while formula.__contains__('system'):
		await ctx.send('U TRYING TO BREAK MY COMPUTER?? WELL THEN YOU HAVE BEEN CAUGHT RED-HANDED. I KNEW WHEN I PUT THE "EVAL" FORMULA, I WAS ALLOWING YOU TO BREAK MY COMPUTER, SO I STOPPED YOU BY BLOCKING THE WORD "os". HOW DARE YOU TRY AND BREAK MY COMPUTER!')
		sleep(random.uniform(10, sqrt(99)))
	if formula.__contains__('exit()'):
		await ctx.send('Nope, not exiting! (I stopped you from doing this as it would make the bot go offline)')
	await ctx.send(eval(formula))


@formula.error
async def formula_error(ctx, error):
	await ctx.send('Error: Please make sure your formula makes sense and uses python operators or the cmath module. \nThis was the error encountered:\n' + str(error))


@bot.command(name='ev')
async def fml(ctx, fml):
	await formula(ctx, fml)


@fml.error
async def fml_error(ctx, error):
	await formula_error(ctx, error)


@bot.command(name='CuboidVolume')
async def CuV(ctx, length:int, height:int, width:int):
	await ctx.send(length * height * width)


@CuV.error
async def CuVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=CuV <height> <width> length>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='CuV')
async def CuboidVolume(ctx, length:int, height:int, width:int):
	await CuV(ctx, length, height, width)


@CuboidVolume.error
async def CUV_Error(ctx, error:str):
	await CuVError(ctx, error)


@bot.command(name='PyramidVolume')
async def PV(ctx, base_area:int, height:int):
	await ctx.send((1 / 3) * base_area * height)


@PV.error
async def PVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=PV <base_area> <height>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='PV')
async def PyramidVolume(ctx, base_area:int, height:int):
	await PV(ctx, base_area, height)


@PyramidVolume.error
async def PV_Error(ctx, error:str):
	await PVError(ctx, error)


@bot.command(name='SphereVolume')
async def SV(ctx, radius:int):
	await ctx.send((4 / 3) * pi * radius ** 3)


@SV.error
async def SVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=SV <radius>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='SV')
async def SphereVolume(ctx, radius:int):
	await SV(ctx, radius)


@SphereVolume.error
async def SV_Error(ctx, error:str):
	await SVError(ctx, error)


@bot.command(name='ConeVolume')
async def CoV(ctx, radius:int, height:int):
	await ctx.send((1 / 3) * pi * radius ** 2 * height)


@CoV.error
async def CoVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=CoV <radius> <height>`.
	This was the error encountered:
	{error}
	''')


@bot.command(name='CoV')
async def ConeVolume(ctx, radius:int, height:int):
	await CoV(ctx, radius, height)


@ConeVolume.error
async def CoV_Error(ctx, error:str):
	await CoVError(ctx, error)


@bot.command(name='CylinderVolume')
async def CyV(ctx, radius:int, height:int):
	await ctx.send(pi * radius ** 2 * height)


@CyV.error
async def CyVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=CyV <radius> <height>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='CyV')
async def CylinderVolume(ctx, radius:int, height:int):
	await CyV(ctx, radius, height)


@CylinderVolume.error
async def CyV_Error(ctx, error:str):
	await CyVError(ctx, error)


@bot.command(name='PentagonalPrismVolume')
async def PPV(ctx, height:int, base_edge_length:int):
	await ctx.send((5 / 4) * height * base_edge_length ** 2 * (1 + 2 / sqrt(5)))


@PPV.error
async def PPVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=PPV <height> <base edge length>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='PPV')
async def PentagonalPrismVolume(ctx, height:int, base_edge_length:int):
	await PPV(ctx, height, base_edge_length)


@PentagonalPrismVolume.error
async def PPV_Error(ctx, error:str):
	await PPVError(ctx, error)


@bot.command(name='HexagonalPrismVolume')
async def HPV(ctx, height:int, base_edge_length:int):
	await ctx.send((3 * sqrt(3) / 2) * height * base_edge_length ** 2)


@HPV.error
async def HPVError(ctx, error:str):
	await ctx.send(f'''
	Error: Please make sure your command makes sense and is set out as:
	`=HPV <height> <base edge length>`. 
	This was the error encountered:
	{error}
	''')


@bot.command(name='HPV')
async def HexagonalPrismVolume(ctx, height:int, base_edge_length:int):
	await HPV(ctx, height, base_edge_length)


@HexagonalPrismVolume.error
async def HPV_Error(ctx, error:str):
	await HPVError(ctx, error)


@bot.command(name='commands')
async def start(ctx, specify='all'):
	welcome = """
	**Welcome to my maths bot!**
	These are the commands (more to be added soon!):
	"""
	PrimeHelp = '''
	**=primerange,=pr**
	`=pr <first number of range> <final number of range>`
	Find how many primes are between 2 numbers
	Example: `=primerange 1 10000` returns the prime numbers between 1 and 10000
	'''
	PowerHelp = '''
	**=powerrange,=pwr**
	`=pwr <first number of range> <final number of range>`
	Find how many squares + cubes are between 2 numbers
	Example: `=powerrange 2 20000` returns the squares and cubes between 2 and 20000
	'''
	EvalHelp = ''' 
	**=eval,=ev**
	`=ev <calculation>`
	Calculate any maths problem. This uses python operators, including the math module. Go to:

	https://www.w3schools.com/python/python_operators.asp
	https://www.w3schools.com/python/module_cmath.asp
	for more information about python operators.
	
	NOTE: ***DO NOT*** add `cmath.` before your functions in the cmath module.
	**Examples:**
	Area of circle with radius 3: `=ev 3**2*pi` returns `28.274333882308138`, while `=ev 3**2*cmath.pi` **returns an error**.
	True/False:
	`=ev 3**2*pi==28.274333882308138` returns `True`
	`=ev 3**2*pi>29` returns `False`
	Area of cone: `pi*3*(3+sqrt(9**2+3**2))` returns `117.68562827447305`
	'''
	CommandHelp = '''
	View list of commands. Examples:
	`=commands` returns full list of commands.
	`=commands pwr` returns description of `pwr` command.
	'''
	CuVHelp = '''
	**=CuV,=CuboidVolume**
	Find volume of cuboid/cube:
	`=CuV <height> <length> <width>`
	Example:
	`=CuV 150 300 600` returns `27000000`
	'''
	PVHelp = '''
	**=PV,=PyramidVolume**
	Find volume of pyramid:
	`=PyV <base area> <height>`
	Example:
	`=PyV 5 7` returns `11.6666667`
	'''
	SVHelp = '''
	**=SV,=SphereVolume**
	Find volume of sphere:
	`=SV <radius>`
	Example:
	`=SV 1` returns `4.1887902`
	'''
	CyVHelp = '''
	**=CyV,=CylinderVolume**
	Find volume of cylinder:
	`=CyV <radius> <height>`
	Example:
	`=CyV 6 8` returns `904.778684`
	'''
	PPVHelp = '''
	**=PPV,=PentagonalPrismVolume**
	Find volume of pentagonal prism:
	`=PPV <height> <base edge length>`
	Example:
	`=PPV 2 3` returns `42.6246118`
	'''
	HPVHelp = '''
	**=HPV,=HexagonalPrismVolume**
	Find volume of hexagonal prism:
	`=HPV <height> <base edge length>`
	Example:
	`=HPV 7 15` returns `4091.97003`
	'''
	if specify == 'pr' or specify == 'primerange':
		await ctx.send(PrimeHelp)
	elif specify == 'pwr' or specify == 'powerrange':
		await ctx.send(PowerHelp)
	elif specify == 'ev' or specify == 'eval':
		await ctx.send(EvalHelp)
	elif specify == 'start' or specify == 'commands' or specify == 'cm':
		await ctx.send(CommandHelp)
	elif specify == 'PyV' or specify == 'PyramidVolume':
		await ctx.send(PVHelp)
	elif specify == 'CuV' or specify == 'CuboidVolume':
		await ctx.send(CuVHelp)
	elif specify == 'SV' or specify == 'SphereVolume':
		await ctx.send(SVHelp)
	elif specify == 'CyV' or specify == 'CylinderVolume':
		await ctx.send(CyVHelp)
	elif specify == 'PPV' or specify == 'PentagonalPrismVolume':
		await ctx.send(PPVHelp)
	elif specify == 'HPV' or specify == 'HexagonalPrismVolume':
		await ctx.send(HPVHelp)
	else:
		await ctx.send(welcome + PrimeHelp + PowerHelp + CommandHelp + CuVHelp + PVHelp + CyVHelp + PPVHelp + HPVHelp)


@bot.command(name='start')
async def _commands_(ctx):
	await start(ctx)


@bot.command(name='cm')
async def __commands__(ctx):
	await start(ctx, specify='all')


if name == 'nt':
	system_path = environ['USERPROFILE'] + '\\TOKEN'
	path = system_path.replace("\\", "/")
else:
	path = environ['HOME'] + '/TOKEN'
	system_path = path
try:
	with open(path, 'r') as t:
		token = str(t.read())
except:
	token = input('Please enter bot token.\n')
	save = input('Do you want to save this token?\n')
	if save.lower() == 'yes' or save.lower() == 'y':	
		try:
			with open(path, 'w+') as t:
				t.write(token)
		except Exception as e:
			print(f'{str(e)}\n\aError while writing file to {system_path}')
		else:
			print(f'TOKEN has been written in file {system_path}')
else:
	if name == 'nt':
		print(f'Using token from {system_path}')
	else:
		print(f'Using token from {system_path}')
bot.run(token)
