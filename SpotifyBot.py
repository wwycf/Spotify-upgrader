import discord
from discord.ext import commands
import json, aiohttp
import re
import os,time,subprocess
from os import listdir
from os.path import isfile, join
import colorama
from colorama import init
from colorama import Fore,Back,Style
init()


# Getting bot's token and prefix you've set in config.json file
try:
    with open('config.json') as (f):
        data = json.load(f)
except FileNotFoundError:
    print(Fore.RED +
          "Configuration file can't be found, please create new one, or move it to folder where your exe of bot is")

# Variables for Bot
bot = commands.Bot(command_prefix=f'{data["Prefix"]}')
token = data["Token"]
Channel = data["Channel"]
AdministratorRole = data["AdministratorRole"]
Stocks = data["StockChannel"]

# Different variables
Accounts = []
Codes = "codes.txt"
client = discord.Client()

# Happen every time bot is turned on
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f'Coded by matt {data["Prefix"]}help for help'))
    print("  _____             _   _  __         ____        _     _           ")
    print(" / ____|           | | (_)/ _|       |  _ \      | |   | |          ")
    print("| (___  _ __   ___ | |_ _| |_ _   _  | |_) | ___ | |_  | |__  _   _ ")
    print(" \___ \| '_ \ / _ \| __| |  _| | | | |  _ < / _ \| __| | '_ \| | | |")
    print(" ____) | |_) | (_) | |_| | | | |_| | | |_) | (_) | |_  | |_) | |_| |")
    print("|_____/| .__/ \___/ \__|_|_|  \__, | |____/ \___/ \__| |_.__/ \__, |")
    print("       | |                     __/ |                           __/ |")
    print("       |_|                    |___/                           |___/ ")
    print("                 _   _   ")
    print("                | | | |  ")
    print(" _ __ ___   __ _| |_| |_ ")
    print("| '_ ` _ \ / _` | __| __|")
    print("| | | | | | (_| | |_| |_ ")
    print("|_| |_| |_|\__,_|\__|\__|")
    print(Fore.GREEN + f'Bot {bot.user.name} is ready to be used')
    print(Fore.GREEN + f'Bot version : V4.0 - Fixed')
    try:
        with open(Codes, "r") as file:
            bot.codes = [code.strip("\n") for code in file.readlines()]
    except FileNotFoundError:
        print(Fore.RED +
              "Codes file can't be found or does not exist, please create new one or move it to same folder where exe of your bot is")

# Refresh command, can be used to refresh codes file in case you've added new codes.
@bot.command()
@commands.has_role(f'{AdministratorRole}')  # Check if user is allowed to use this command
async def refresh(ctx):
    """ Recheck if new codes are in codes file.
        !refresh - No arguments needed.
    """
    embed = discord.Embed(
        title=f"Codes file refreshed", color=0x00FF00)
    try:
        with open(Codes, "r") as file:
            bot.codes = [code.strip("\n") for code in file.readlines()]
            message = await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(
            title=f"Codes file doesn't exit, please check console for more details", color=0xff5959)
        message = await ctx.send(embed=embed)
        print(Fore.RED +
              "Codes file can't be found or does not exist, please create new one or move it to same folder where exe of your bot is")

# Redeem command can be used to invite user into premium plan
@bot.command()
async def redeem(ctx, country: str, email: str, code: str):
    """ You can use this command to upgrade your account to premium.
        country - Country you live in, and you have spotify account in.
        email - Your email address, where bot will send invitation link.
        code - Code you've bought/got to upgrade your account.
    """
    if '<' in country:  # Checking if command was used with <> or without <>
        embed = discord.Embed(
            title=f"Please use this command without <>, thanks", color=0xff5959)
        message = await ctx.send(embed=embed)
        return
    if '<' in email:  # Checking if command was used with <> or without <>
        embed = discord.Embed(
            title=f"Please use this command without <>, thanks", color=0xff5959)
        message = await ctx.send(embed=embed)
        return
    if '<' in code:  # Checking if command was used with <> or without <>
        embed = discord.Embed(
            title=f"Please use this command without <>, thanks", color=0xff5959)
        message = await ctx.send(embed=embed)
        return
    await ctx.channel.purge(limit=1)  # Deleting reedem message from user, in order to protect his privacy
    if str(ctx.channel) in Channel:
        if '@' in email:  # Checking if user's email is valid or invalid
            if code not in bot.codes:  # Checking if user has valid or invalid redeem code
                embed = discord.Embed(
                    title=f"{ctx.author} That's a bad upgrade key, sorry :/, please try again. It's possible that code wasn't in system so far", color=0xff5959)
                message = await ctx.send(embed=embed)
                try:  # Check if code file does exist
                    with open(Codes, "r") as file:
                        bot.codes = [code.strip("\n") for code in file.readlines()]
                        print(Fore.GREEN + 'Codes file refreshed, new codes can now be used')
                except FileNotFoundError:
                    print(Fore.RED +
                          "Codes file can't be found or does not exist, please create new one or move it to same folder where exe of your bot is")
                print(Fore.RED + f'@{ctx.author} tried to upgrade with invalud upgrade key ({code})')
                return
            else:
                print(Fore.YELLOW + f'@{ctx.author} tried to upgrade with a valid upgrade key ({code})')
                result = 'false'
                embed = discord.Embed(
                    title="Searching for an account...", color=0xffa500)
                message = await ctx.send(embed=embed)
                while result != 'true':  # Repeat until user is invited into familly plan, or country is out of stock
                    try:  # Check if there's stock for country user want to get invite in
                        with open(f"Accounts/{country.upper()}.txt") as filehandle:
                            lines = filehandle.readlines()
                        with open(f"Accounts/{country.upper()}.txt", 'w') as filehandle:
                            lines = filter(lambda x: x.strip(), lines)
                            filehandle.writelines(lines)
                    except FileNotFoundError:
                        embed = discord.Embed(
                            title=f"Sorry, but we currently don't have any stocks for {country.upper()}", color=0xff5959)
                        await message.edit(embed=embed)
                        break
                    LastName = "Snow"
                    FirstName = "John"
                    try:
                        with open('Accounts/'+f'{country.upper()}'+'.txt','r') as (f):
                            for line in f:
                                clean = line.split('\n')
                                Accounts.append(clean[0])
                                lines = f.readlines()
                    except FileNotFoundError:
                        embed = discord.Embed(
                            title=f"Sorry, but We currently don't offer upgrades in this country.", color=0xd3d3d3)
                        await ctx.send(embed=embed)
                    try:
                        account = Accounts.pop()
                        embed = discord.Embed(
                            title="An account has been found.", color=0x00FF00)
                        await message.edit(embed=embed)
                    except IndexError:
                        embed = discord.Embed(
                            title=f"Sorry, but {country.upper()} is currently out of stock.", color=0xff5959)
                        await message.edit(embed=embed)
                        print(Fore.RED + f'{country.upper()} is out of stock')
                        break
                    combo = account.split(':')  # Will split combo into a list, so we can later use only pices of it
                    User = combo[0]
                    Pass = combo[1]
                    Country = country
                    embed = discord.Embed(
                        title=f"Trying to send an invite...", color=0xffa500)
                    await message.edit(embed=embed)
                    # Try to login into account and send invite to user.
                    async with aiohttp.ClientSession() as session:

                        url = 'https://accounts.spotify.com/en/login?continue=https://www.spotify.com/int/account/overview/'
                        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                        response = await session.get(url, headers=headers)
                        CSRF = session.cookie_jar.filter_cookies(url)[
                            'csrf_token'
                        ].value

                        headers = {
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                            'Referer': 'https://accounts.spotify.com/en/login/?continue=https://www.spotify.com/us/googlehome/register/&_locale=en-US'
                        }

                        url = 'https://accounts.spotify.com/api/login'

                        credentials = {
                            'remember': 'true',
                            'username': User,
                            'password': Pass,
                            'csrf_token': CSRF
                        }

                        cookies = dict(
                            __bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')

                        postLogin = await session.post(url, headers=headers, data=credentials, cookies=cookies)

                        postLoginJson = await postLogin.json()

                        # print(postLoginJson)

                        if 'displayName' in postLoginJson:  # If displayName IS in source code, then we're successfully logged into account.

                            url = "https://www.spotify.com/us/account/overview/"

                            secondLogin = await session.get(url,headers=headers)
                            csrf = secondLogin.headers['X-Csrf-Token']

                            url = 'https://www.spotify.com/us/family/api/master-invite-by-email/'

                            headers = {
                                'Accept': '*/*',
                                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                                'x-csrf-token': csrf
                            }

                            postData = {
                                'firstName': FirstName,
                                'lastName': LastName,
                                'email': email
                            }

                            invitePost = await session.post(url,headers=headers,json=postData)
                            inviteJson = await invitePost.json()

                            if inviteJson["success"] is True: # If user was successfully invited to familly plan
                                url = "https://www.spotify.com/us/account/overview/"

                                secondLogin = await session.get(url, headers=headers)
                                csrf = secondLogin.headers['X-Csrf-Token']

                                url = 'https://www.spotify.com/us/family/overview/'

                                headers = {
                                    'Accept': '*/*',
                                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                                    'x-csrf-token': csrf
                                }
                                async with await session.get(url,headers=headers) as resp:
                                    WebsiteResponse = await resp.text()
                                    Replace0 = WebsiteResponse.replace("x7B", "<")
                                    Replace1 = Replace0.replace("x20","")
                                    Replace2 = Replace1.replace("x22",'"')
                                    Replace3 = Replace2.replace("x3A", ':')
                                    Replace4 = Replace3.replace("x2D", '-')
                                    Replace5 = Replace4.replace("x5D", ')')
                                    Replace6 = Replace5.replace("x5B", '(')
                                    Replace7 = Replace6.replace("x7D", '>')
                                    Replace8 = Replace7.replace("\\", '')
                                    PostCodeUnfixed = re.search('postalCode":"(.*)","city"', Replace8)
                                    PostCodeSep = '","'
                                    ZipCode = PostCodeUnfixed.group(1).split(PostCodeSep, 1)[0]
                                    CityUnfixed = re.search(f'"postalCode":"{ZipCode}","city":"(.*)","line1":"', Replace8)
                                    CitySep = '","'
                                    City = CityUnfixed.group(1).split(CitySep, 1)[0]
                                    AddressUnfixed = re.search(f'city":"{City}","line1":"(.*)">,"canInvite":', Replace8)
                                    AddressSep = '":"'
                                    AddressTemps = AddressUnfixed.group(1).split(AddressSep, 1)[0]
                                    AddressTemp = AddressTemps
                                    AddressTempSep = '">,"canInvite"'
                                    Address = AddressTemp.split(AddressTempSep, 1)[0]
                                if not City:
                                    embed = discord.Embed(
                                        title=f"Invitation code was sent, check private messages @{ctx.author}.",color=0x00FF00)
                                    await message.edit(embed=embed)
                                    print(Fore.GREEN + f'@{ctx.author} successfully upgraded his account {email} from {country.upper()} with a key {code}')
                                    await ctx.author.send(f"Please check for an email from Spotify for an invitation link!"
                                                          f"\nFill in these informations in form!"
                                                          f"\n"
                                                          f"\nInvite sent to: {email}"
                                                          f'\n**City**: `You can add random {country.upper()} city`'
                                                          f'\n**Street Name**: `You can add random {country.upper()} street`'
                                                          f'\n**Postal Code**: `You can add random {country.upper()} postal code`'
                                                          f'\n**Country**: `{country.upper()}`'
                                                          f'\n**You can add random {country.upper()} address if these fields are empty.**'
                                                          )
                                    bot.codes.remove(code)  # Remove code from codes list after user got invite code.
                                    with open("codes.txt", "a") as file:
                                        file.truncate(0)
                                        for code in bot.codes:
                                            file.write(f"{code}\n")
                                    break
                                else:
                                    embed = discord.Embed(
                                        title=f"Invitation code was sent, check private messages @{ctx.author}.", color=0x00FF00)
                                    await message.edit(embed=embed)
                                    print(Fore.GREEN + f'@{ctx.author} successfully upgraded his account {email} from {country.upper()} with a key {code}')
                                    await ctx.author.send(f"Please check for an email from Spotify for an invitation link!"
                                                               f"\nFill in these informations in form!"
                                                               f"\n"
                                                               f"\nInvite sent to: {email}"
                                                               f'\n**City**: `{City}`'
                                                               f'\n**Street Name**: `{Address}`'
                                                               f'\n**Postal Code**: `{ZipCode}`'
                                                               f'\n**Country**: `{Country.upper()}`'
                                                               f'\n**You can add random {country.upper()} address if these fields are empty.**'
                                                               )
                                    bot.codes.remove(code)  # Remove code from codes list after user got invite code.
                                    with open("codes.txt", "a") as file:
                                        file.truncate(0)
                                        for code in bot.codes:
                                            file.write(f"{code}\n")
                                    break
                            else:  # If user wasn't invited to familly plan so far
                                embed = discord.Embed(
                                    title=f"There were some issues, retrying.", color=0xd3d3d3)
                                await message.edit(embed=embed)
                                with open(f"Accounts/{country}.txt", "w") as f:
                                    for line in lines:
                                        if line.strip("\n") != f"{User}:{Pass}":
                                            f.write(line)
                                result = 'false'
        else:  # If user's email address isn't correct.
            embed = discord.Embed(
                title=f"Your email address isn't valid", color=0xff5959)
            message = await ctx.send(embed=embed)
    else:  # If user is trying to get invite in wrong channel.
        embed = discord.Embed(
            title=f"You can only use this command in #{Channel}", color=0xd3d3d3)
        message = await ctx.send(embed=embed)

@bot.command()
@commands.has_role(f'{AdministratorRole}')  # Checking if user is allowed to use this command.
async def restock(ctx, country: str):
    """ This command can be used to restock accounts.
        Country = Country you want to restock accounts in.
        In case you want to rest all countries use !restock all
    """
    await ctx.channel.purge(limit=1)  # Deleting the restock message
    print(Fore.GREEN + f'@{ctx.author} restocked stocks')
    embed = discord.Embed(
        title="Restocking....", color=0xffa500)
    message = await ctx.send(embed=embed)
    if 'all' in country:
        onlyfiles = [f for f in listdir('Restocks') if
                     isfile(join('Restocks', f))]
        for e in onlyfiles:
            with open(f"Restocks/{e}") as f:
                lines = f.readlines()
                lines = [l for l in lines if ":" in l]
                with open(f"Accounts/{e}", "a+") as f1:
                    f1.writelines(lines)
                    f.close()
                    os.remove(f"Restocks/{e}")
        embed = discord.Embed(
            title="All countries were was successfully restocked", color=0x00FF00)
        await message.edit(embed=embed)
    else:
        try:
            with open(f"Restocks/{country.upper()}.txt") as f:
                lines = f.readlines()
                lines = [l for l in lines if ":" in l]
                with open(f"Accounts/{country.upper()}.txt", "a+") as f1:
                    f1.writelines(lines)
                    f.close()
                os.remove(f"Restocks/{country.upper()}.txt")
                embed = discord.Embed(
                    title=f"{country.upper()} was successfully restocked", color=0x00FF00)
                await message.edit(embed=embed)
        except FileNotFoundError:
            print(Fore.RED +
                  "You can't restock this country, since you don't have any restock file for this country in Restocks folder")
            embed = discord.Embed(
                title="File for this country doesn't exist in restocks folder.", color=0xff5959)
            await message.edit(embed=embed)

@bot.command()
async def info(ctx):
    """ Just some informations about coder."""
    print(Fore.YELLOW + f'@{ctx.author} used !info')
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(f"```This is opensource spotify upgrade bot made by matt(matoooo),"
                          f"\nI've coded it to practice in Python and to get better in it."
                          f"\nAs said it's opensource, so if you have any problems, just go into code and edit it"
                          f"\nIf you will ever need something from me, just hit me up on Discord matooo#5132"
                           f"\nBillie is best! And you can't change my mind.```"
                          )

@bot.command()
async def stock(ctx, country:str):
    """ This command can be used to check current stocks.
        <country> - Country you want to check stocks in.
        Commands:
        !stock <country> - To check stocks for specific country
        !stock all - To check stocks for all countries
    """
    if '<' in country:  # Checking for <> in country
        embed = discord.Embed(
            title=f"Please use this command without <>, thanks", color=0xff5959)
        message = await ctx.send(embed=embed)
        return
    print(Fore.YELLOW + f'@{ctx.author} checked stocks for {country.upper()}')
    await ctx.channel.purge(limit=1)  # Deleting message.
    if str(ctx.channel) in Stocks:
        if country == 'all':  # If command is !stock all then do this
            embed = discord.Embed(title='Current Stocks',
                                  colour=discord.Colour.blue())
            onlyfiles = [f for f in listdir('Accounts') if
                         isfile(join('Accounts', f))]
            for e in onlyfiles:
                num_lines = sum(1 for line in open(f'Accounts/{e}'))
                x = e.replace(".txt", "")
                embed.add_field(name=str(x), value=int(num_lines), inline=True)
            await ctx.send(embed=embed)
        else:  # If command is with specific country (ex. !stock US) do this
            try:  # Check if file even exist
                with open(f"Accounts/{country.upper()}.txt") as filehandle:
                    lines = filehandle.readlines()
                with open(f"Accounts/{country.upper()}.txt", 'w') as filehandle:
                    lines = filter(lambda x: x.strip(), lines)
                    filehandle.writelines(lines)
                embed = discord.Embed(title='Current Stocks',
                                      colour=discord.Colour.blue())
                num_lines = sum(1 for line in open(f'Accounts/{country}.txt'))
                embed.add_field(name=str(country.upper()), value=int(num_lines), inline=False)
                await ctx.send(embed=embed)
            except FileNotFoundError:
                embed = discord.Embed(
                    title=f"Sorry, but We currently don't offer upgrades in this country.", color=0xd3d3d3)
                await ctx.send(embed=embed)
    else:  # If user is in different channel then he have to be
        embed = discord.Embed(
            title=f"Sorry, but you can't check stock channel, please go to #{Stocks}", color=0xd3d3d3)
        await ctx.send(embed=embed)
bot.run(token)
