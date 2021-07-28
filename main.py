#!/usr/bin/env python3
from os import system,name,environ
try:
    from discord.ext import commands
except ModuleNotFoundError:
    print('discord.py is not installed. Installing...')
    install_pip=system('python3 -m ensurepip --upgrade')
    install_discord=str(system("python3 -m pip install 'discord.py'"))
    if not '0' in install_discord:
        print('Error while installing discord.py.')
        exit()
import logging
from cmath import * #@UnusedWildImport
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
async def primerange(ctx,num1: int,num2: int):
    await ctx.channel.trigger_typing()
    def PrimeOrComposite(n):
        if n == 2 or n == 3:
            return('is a prime number.')
        if n < 2 or n%2 == 0:
            return('is a composite number.')
        if n < 9:
            return('is a prime number.')
        if n%3 == 0:
            return('is a composite number.')
        r = int(n**0.5)
        f = 5
        while f <= r:
            if n % f == 0:
                return('is a composite number.')
            if n % (f+2) == 0:
                return('is a composite number.')
            f += 6
        return('is a prime number.')
    async def PrimeRange(num1,num2):
        amount = 0
        primes = ('These are the prime numbers between' + str(num1) +' and ' +str(num2) + ': ')
        for l in range(num1, num2 + 1):
            if PrimeOrComposite(l) == 'is a prime number.':
                amount = amount + 1
                primes = primes + str(l) + ', '
        if amount == 1:
            await ctx.send('There is 1 prime number between '+ str(num1)+ ' and '+ str(num2)+'.')
        else:
            await ctx.send('There are '+ str(amount)+ ' prime numbers between '+ str(num1)+ ' and '+ str(num2)+'.')
        await ctx.channel.trigger_typing()
        global Total
        Total = ''.join(primes)
    await PrimeRange(num1,num2)
    if len(Total)>2000:
        await ctx.send('There are too many numbers to print, so it can not be fit into one message.')
        j=0
        for i in range(1,int(len(Total)/2000)+1):
            await ctx.send(str(Total)[j:i*2000])
            j=i*2000
    else:
        await ctx.send(str(Total))
@primerange.error
async def pr_error(ctx,error):
    await ctx.send('Please make sure your command is set out like this:\n=primerange <first number> <final number>\nThis was the error encountered:\n'+str(error))
@bot.command(name='pr')
async def pr(ctx,num1:int,num2:int):
    await primerange(ctx,num1,num2)
@pr.error
async def PR_Error(ctx,error):
    await pr_error(ctx,error)
@bot.command(name='powerrange')
async def powerrange(ctx,num1:int,num2:int):
    await ctx.channel.trigger_typing()
    def SquareOrCube(n):
        if abs(n**(1/6)) == int(abs(n**(1/6))):
            return('is a power of 6, so it is both a square number and a cube number.')
        elif abs(n**0.5) == int(abs(n**0.5)):
            return('is a square number.')
        elif abs(n**(1/3)) ==int(abs(n**(1/3))):
            return('is a cube number.')
        else:
            return('is not a square or cube number.')
    async def PowerRange(num1,num2):
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
        total = ('There are '+ str(cubes)+ ' cube numbers, and '+ str(squares)+' square numbers between '+ str(num1)+ ' and '+ str(num2)+ '.')
        await ctx.send(''.join(total))
        await ctx.channel.trigger_typing()
        totallist = CubeNumbers + '\n' + SquareNumbers
    await PowerRange(num1,num2)
    if len(totallist)>2000:
        await ctx.send('There are too many numbers to print, so it can not be fit into one message.')
        j=0
        for i in range(1,int(len(totallist)/2000)+1):
            await ctx.send(str(totallist)[j:i*2000])
            j=i*2000
    else:
        await ctx.send(totallist)
@powerrange.error
async def powerrange_error(ctx,error):
    await ctx.send('Please make sure your command is set out like this:\n=powerrange <first number> <final number>\nThis was the error encountered:\n'+str(error))
@bot.command(name='pwr')
async def pwr(ctx,num1:int,num2:int):
    await powerrange(ctx,num1,num2)
@pwr.error
async def pwr_error(ctx,error):
    await powerrange_error(ctx,error)
@bot.command(name='eval')
async def formula(ctx,formula):
    while formula.__contains__('system'):
        await ctx.send('U TRYING TO BREAK MY COMPUTER?? WELL THEN YOU HAVE BEEN CAUGHT RED-HANDED. I KNEW WHEN I PUT THE "EVAL" FORMULA, I WAS ALLOWING YOU TO BREAK MY COMPUTER, SO I STOPPED YOU BY BLOCKING THE WORD "os". HOW DARE YOU TRY AND BREAK MY COMPUTER!')
        sleep(random.uniform(10,sqrt(99)))
    if formula.__contains__('exit()'):
        await ctx.send('Nope, not exiting! (I stopped you from doing this as it would make the bot go offline)')
    await ctx.send(eval(formula))
@formula.error
async def formula_error(ctx,error):
    await ctx.send('Error: Please make sure your formula makes sense and uses python operators or the cmath module. \nThis was the error encountered:\n'+str(error))
@bot.command(name='ev')
async def fml(ctx,fml):
    await formula(ctx,fml)
@fml.error
async def fml_error(ctx,error):
    await formula_error(ctx,error)
@bot.command(name='commands')
async def start(ctx,specify='all'):
    welcome="""
    **Welcome to my maths bot!**
    These are the commands (more to be added soon!):

    """
    PrimeHelp='''
    **=primerange,=pr**
    `=pr <first number of range> <final number of range>`
    Find how many primes are between 2 numbers
    Example: `=primerange 1 10000` returns the prime numbers between 1 and 10000

    '''
    PowerHelp='''
    **=powerrange,=pwr**
    `=pwr <first number of range> <final number of range>`
    Find how many squares + cubes are between 2 numbers
    Example: `=powerrange 2 20000` returns the squares and cubes between 2 and 20000

    '''
    EvalHelp=''' 
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
    CommandHelp='''
    View list of commands. Examples:
    `=commands` returns full list of commands.
    `=commands pwr` returns description of `pwr` command.

    '''
    if specify=='pr' or specify=='primerange':
        await ctx.send(welcome+PrimeHelp)
        print(welcome+PrimeHelp)
    elif specify=='pwr' or specify=='powerrange':
        await ctx.send(welcome+PowerHelp)
    elif specify=='ev' or specify=='eval':
        await ctx.send(EvalHelp)
    elif specify=='start' or specify=='commands' or specify=='cm':
        await ctx.send(welcome+CommandHelp)
    else:
        await ctx.send(welcome+PrimeHelp+PowerHelp+CommandHelp)
@bot.command(name='start')
async def _commands_(ctx):
    await start(ctx)
@bot.command(name='cm')
async def __commands__(ctx):
    await start(ctx,specify='all')
try:
    token=environ['TOKEN']
except KeyError:
    token=input('Enter a bot token.')
    save=input('Do you want to use this token every time you run this bot on your computer?') 
    if save.lower()=='yes' or save.lower()=='y':
        if name=='nt':
            system(f'SETX TOKEN {token}')
        else:
            system(f'echo TOKEN={token} >> ~/.profile')
            system(f'echo TOKEN={token} >> ~/.bash_profile')
bot.run(token)
