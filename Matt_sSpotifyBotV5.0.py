#Importing all needed modules.
import discord
import json, aiohttp
import re, os , time , subprocess , colorama
from os import listdir
from os.path import isfile, join
from colorama import init, Fore, Back, Style
from discord.ext import commands
init()

#Reading config in order to get bot's token.
try:
    with open('config.json') as (f):
        data = json.load(f)
except FileNotFoundError:
    print(Fore.RED +
          "Configuration file can't be found, please create new one, or move it to folder where your exe of bot is")

#Setting important variables.
Accounts = []
Codes = "codes.txt"
client = discord.Client()
token = data["Token"]
bot = commands.Bot(command_prefix=f'{data["Prefix"]}')
Name = "Jon"
Surname = "Snow"


@bot.event #Happening every time bot is turned of for first time. And Getting important informations from Administrator of bot.
async def on_ready():
    os.system('cls')
    print(Fore.GREEN + """
     __             _   _  __         _           _   
    / _\_ __   ___ | |_(_)/ _|_   _  | |__   ___ | |_ 
    \ \| '_ \ / _ \| __| | |_| | | | | '_ \ / _ \| __|
    _\ \ |_) | (_) | |_| |  _| |_| | | |_) | (_) | |_ 
    \__/ .__/ \___/ \__|_|_|  \__, | |_.__/ \___/ \__|
       |_|                    |___/                   
     _                             _   _              
    | |__  _   _   _ __ ___   __ _| |_| |_            
    | '_ \| | | | | '_ ` _ \ / _` | __| __|           
    | |_) | |_| | | | | | | | (_| | |_| |_            
    |_.__/ \__, | |_| |_| |_|\__,_|\__|\__|           
           |___/                                      
    """)
    print(Fore.RESET)
    try:
        with open(Codes, "r") as file:
            bot.codes = [code.strip("\n") for code in file.readlines()]
    except FileNotFoundError:
        print(Fore.RED +
              "Codes file can't be found or does not exist, please create new one or move it to same folder where exe of your bot is")
    print(Fore.RESET)


print(Fore.LIGHTGREEN_EX + "Welcome in set-up mode, please fill these details in order to make your bot fully functional")
print(Fore.YELLOW + "WARNING:")
print(Fore.YELLOW + "Not filling some of these details or not filling them correctly, can end up in your bot not working properly")
print(Fore.RESET)
while 1==1:
    Mode = input(f"Please select mode you want to use (Type Free/Paid)\n")
    if Mode == "Paid":
        break
    elif Mode == "Free":
        break
Channel = input(f"Please enter name of channel where users will be able to upgrade their keys\n")
if not Channel:
    Channel = "spotify"
Role = input(f"Please enter name of role that will have access to all commands, in other words administrator role\n")
if not Role:
    Role = "owner"
Stocks = input(f"Please enter channel where users will be able to change current stocks\n")
if not Stocks:
    Stocks = "stock"
while 1==1:
    Debug = input("Please select mode you want console in, to understand mods better check github (Degub/Normal)\n")
    if Debug == "Debug":
        break
    elif Debug == "Normal":
        break


if Mode == "Free": #Upgrading user in free mode = user doesn't need to use upgrade key
    @bot.command()
    async def redeem(ctx, country: str,email: str):
        """ You can use this command to upgrade your account to premium.
            country - Country you live in, and you have spotify account in.
            email - Your email address, where bot will send invitation link.
        """
        await ctx.channel.purge(limit=1)
        if str(ctx.channel) in Channel:
            if '@' in email:
                print(Fore.YELLOW + f"@{ctx.author} upgrading his account {email} from {country.upper()} in free mode")
                print(Fore.RESET)
                result = 'false'
                tries = 0
                embed = discord.Embed(
                    title="Searching for an account...", color=0xffa500)
                message = await ctx.send(embed=embed)
                while result != "true":
                    while tries <= 5:
                        try:
                            with open(f"Accounts/{country.upper()}.txt") as filehandle:
                                lines = filehandle.readlines()
                            with open(f"Accounts/{country.upper()}.txt", 'w') as filehandle:
                                lines = filter(lambda x: x.strip(), lines)
                                filehandle.writelines(lines)
                        except FileNotFoundError:
                            embed = discord.Embed(
                                title=f"Sorry, but we currently don't have any stocks for {country.upper()}", color=0xff5959)
                            await message.edit(embed=embed)
                            print (Fore.RED + f"User @{ctx.author} tried to upgrade his account, but {country.upper()} is already out of stock or never had any stocks")
                            print (Fore.RESET)
                            result = "true"
                            break
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
                            result = "true"
                            break
                        try:
                            account = Accounts.pop()
                            embed = discord.Embed(
                                title="An account has been found.", color = 0x00FF00
                                )
                            await message.edit(embed=embed)
                        except IndexError:
                            embed = discord.Embed(
                                title=f"Sorry, but {country.upper()} is currently out of stock.", color = 0xff5959
                                )
                            await message.edit(embed=embed)
                            print (Fore.RED + f"User @{ctx.author} tried to upgrade his account, but {country.upper()} is already out of stock or never had any stocks")
                            print (Fore.RESET)
                            result = "true"
                            break
                        combo = account.split(':')
                        user = combo[0]
                        password = combo[1]
                        embed = discord.Embed(
                            title=f"Trying to send an invite...", color=0xffa500)
                        await message.edit(embed=embed)
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
                                'username': user,
                                'password': password,
                                'csrf_token': CSRF
                            }

                            cookies = dict(
                                __bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')

                            postLogin = await session.post(url, headers=headers, data=credentials, cookies=cookies)

                            postLoginJson = await postLogin.json()
                            if Debug == "Debug":
                                print(postLoginJson)
                                print(postLoginJson.get('error'))
                            errorMessage = postLoginJson.get('error')
                            if errorMessage == "errorInvalidCredentials":
                                with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != f"{user}:{password}":
                                                f.write(line)
                                        result = 'false'
                                        tries += 1
                                        if Debug == "Debug":
                                            print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                            print(Fore.RESET)
                                        if tries >= 5:
                                            embed = discord.Embed(
                                                title=f"There were some issues, retrying.", color=0xd3d3d3)
                                            await message.edit(embed=embed)
                            elif 'displayName' in postLoginJson:
                                if 1 == 1:
                                    url = "https://www.spotify.com/us/account/overview/"

                                    secondLogin = await session.get(url, headers=headers)
                                    csrf = secondLogin.headers['X-Csrf-Token']

                                    url = 'https://www.spotify.com/us/home-hub/api/v1/family/home/'

                                    headers = {
                                        'Accept': '*/*',
                                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                                        'x-csrf-token': csrf
                                    }
                                    async with await session.get(url,headers=headers) as resp:
                                        WebsiteResponse = await resp.json()
                                        if Debug == "Debug":
                                            print(Fore.RESET + f"{WebsiteResponse}")
                                        accessControl = WebsiteResponse["accessControl"]
                                        Slots = accessControl["planHasFreeSlots"]
                                        if Slots is True:
                                            Address = WebsiteResponse["address"]
                                            inviteToken = WebsiteResponse["inviteToken"]
                                            embed = discord.Embed(
                                                title=f"Invitation code was sent, check private messages @{ctx.author}.", color=0x00FF00)
                                            await message.edit(embed=embed)
                                            print(Fore.GREEN + f'@{ctx.author} successfully upgraded his account {email} from {country.upper()} in free mode')
                                            await ctx.author.send(f"In order to upgrade your account please click on lin below, and enter prov"
                                                                       f"\nFill in these informations in form!"
                                                                       f"\n"
                                                                       f'\n**Address**: `{Address}`'
                                                                       f'\n**Invite Link**: https://www.spotify.com/{country.lower()}/family/join/invite/{inviteToken}'
                                                                       f'\n**You can add random {country.upper()} address if these fields are empty.**'
                                                                       )
                                            result = "true"
                                            break
                                        elif Slots is False:
                                            tries += 1
                                            if Debug == "Debug":
                                                print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                                print(Fore.RESET)
                                            embed = discord.Embed(
                                            title=f"There were some issues, retrying.", color=0xd3d3d3)
                                            await message.edit(embed=embed)
                                            with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                                for line in lines:
                                                    if line.strip("\n") != f"{user}:{password}":
                                                        f.write(line)
                                            result = 'false'
                                else:
                                    tries += 1
                                    if Debug == "Debug":
                                        print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                        print(Fore.RESET)
                                    embed = discord.Embed(
                                    title=f"There were some issues, retrying.", color=0xd3d3d3)
                                    await message.edit(embed=embed)
                                    with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != f"{user}:{password}":
                                                f.write(line)
                                        result = 'false'
                    if result == "true":
                        break
                    if tries >= 6:
                        if Debug == "Debug":
                                        print(Fore.RED + f"Failed to upgrade user bacuse of too many fails")
                                        print(Fore.RESET)
                        embed = discord.Embed(
                                    title=f"Oops, we're not able to upgrade your account at the moment, please try again later.", color=0xff5959)
                        await message.edit(embed=embed)
                        print(Fore.RED + f"Seems like there are some issues with {country.upper()} please check your stock if there isn't something weird happening.")
                        print(Fore.RESET)
                        break
            else:
                if Debug == "Debug":
                    print(Fore.RED + f"User {ctx.author} tried to upgrade with invalid email address {email}")
                    print(Fore.RESET)
                embed = discord.Embed(
                    title=f"Please use valid email address in order to upgrade your account.", color=0xff5959)
                await ctx.send(embed=embed)
        else: 
            embed = discord.Embed(
                title=f"You can only use this command in #{Channel}", color=0xd3d3d3)
            message = await ctx.send(embed=embed)


if Mode == "Paid": #Upgrading user in free mode = user doesn't need to use upgrade key
    @bot.command()
    async def redeem(ctx, country: str,email: str, code: str):
        """ You can use this command to upgrade your account to premium.
            country - Country you live in, and you have spotify account in.
            email - Your email address, where bot will send invitation link.
            code - code you bought in order to upgrade your account.
        """
        await ctx.channel.purge(limit=1)
        if str(ctx.channel) in Channel:
            if '@' in email:
                if code not in bot.codes:
                    embed = discord.Embed(
                    title=f"{ctx.author} That's a bad upgrade key, sorry :/, please try again. It's possible that code wasn't in system so far", color=0xff5959)
                    with open(Codes, "r") as file:
                        bot.codes = [code.strip("\n") for code in file.readlines()]
                        print(Fore.GREEN + 'Codes file refreshed, new codes can be used now')
                    message = await ctx.send(embed=embed)
                    print(Fore.RED + f'@{ctx.author} tried to upgrade with an invalid upgrade key ({code})')
                    print(Fore.RESET)
                    return
                try:  # Check if code file does exist
                    with open(Codes, "r") as file:
                        bot.codes = [code.strip("\n") for code in file.readlines()]
                        print(Fore.GREEN + 'Codes file refreshed, new codes can be used now')
                except FileNotFoundError:
                    print(Fore.RED +
                          "Codes file can't be found or does not exist, please create new one or move it to same folder where exe of your bot is")
                    print(Fore.RED + f'@{ctx.author} tried to upgrade with an invalid upgrade key ({code})')
                    print(Fore.RESET)
                    return
                else:
                    print(Fore.YELLOW + f"@{ctx.author} upgrading his account {email} from {country.upper()} in paid mode with code {code}")
                    print(Fore.RESET)
                    result = 'false'
                    tries = 0
                    embed = discord.Embed(
                        title="Searching for an account...", color=0xffa500)
                    message = await ctx.send(embed=embed)
                    while result != "true":
                        while tries <= 5:
                            try:
                                with open(f"Accounts/{country.upper()}.txt") as filehandle:
                                    lines = filehandle.readlines()
                                with open(f"Accounts/{country.upper()}.txt", 'w') as filehandle:
                                    lines = filter(lambda x: x.strip(), lines)
                                    filehandle.writelines(lines)
                            except FileNotFoundError:
                                embed = discord.Embed(
                                    title=f"Sorry, but we currently don't have any stocks for {country.upper()}", color=0xff5959)
                                await message.edit(embed=embed)
                                print (Fore.RED + f"User @{ctx.author} tried to upgrade his account, but {country.upper()} is already out of stock or never had any stocks")
                                print (Fore.RESET)
                                result = "true"
                                break
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
                                result = "true"
                                break
                            try:
                                account = Accounts.pop()
                                embed = discord.Embed(
                                    title="An account has been found.", color = 0x00FF00
                                    )
                                await message.edit(embed=embed)
                            except IndexError:
                                embed = discord.Embed(
                                    title=f"Sorry, but {country.upper()} is currently out of stock.", color = 0xff5959
                                    )
                                await message.edit(embed=embed)
                                print (Fore.RED + f"User @{ctx.author} tried to upgrade his account, but {country.upper()} is already out of stock or never had any stocks")
                                print (Fore.RESET)
                                result = "true"
                                break
                            combo = account.split(':')
                            user = combo[0]
                            password = combo[1]
                            embed = discord.Embed(
                                title=f"Trying to send an invite...", color=0xffa500)
                            await message.edit(embed=embed)
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
                                    'username': user,
                                    'password': password,
                                    'csrf_token': CSRF
                                }

                                cookies = dict(
                                    __bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')

                                postLogin = await session.post(url, headers=headers, data=credentials, cookies=cookies)

                                postLoginJson = await postLogin.json()
                                if Debug == "Debug":
                                    print(postLoginJson)
                                    print(postLoginJson.get('error'))
                                errorMessage = postLoginJson.get('error')
                                if errorMessage == "errorInvalidCredentials":
                                    with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                            for line in lines:
                                                if line.strip("\n") != f"{user}:{password}":
                                                    f.write(line)
                                            result = 'false'
                                            tries += 1
                                            if Debug == "Debug":
                                                print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                                print(Fore.RESET)
                                            if tries >= 5:
                                                embed = discord.Embed(
                                                    title=f"There were some issues, retrying.", color=0xd3d3d3)
                                                await message.edit(embed=embed)
                                elif 'displayName' in postLoginJson:
                                    if 1 == 1:
                                        url = "https://www.spotify.com/us/account/overview/"

                                        secondLogin = await session.get(url, headers=headers)
                                        csrf = secondLogin.headers['X-Csrf-Token']

                                        url = 'https://www.spotify.com/us/home-hub/api/v1/family/home/'

                                        headers = {
                                            'Accept': '*/*',
                                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                                            'x-csrf-token': csrf
                                        }
                                        async with await session.get(url,headers=headers) as resp:
                                            WebsiteResponse = await resp.json()
                                            if Debug == "Debug":
                                                print(Fore.RESET + f"{WebsiteResponse}")
                                            accessControl = WebsiteResponse["accessControl"]
                                            Slots = accessControl["planHasFreeSlots"]
                                            if Slots is True:
                                                Address = WebsiteResponse["address"]
                                                inviteToken = WebsiteResponse["inviteToken"]
                                                embed = discord.Embed(
                                                    title=f"Invitation code was sent, check private messages @{ctx.author}.", color=0x00FF00)
                                                await message.edit(embed=embed)
                                                print(Fore.GREEN + f'@{ctx.author} successfully upgraded his account {email} from {country.upper()} in free mode')
                                                await ctx.author.send(f"In order to upgrade your account please click on lin below, and enter prov"
                                                                           f"\nFill in these informations in form!"
                                                                           f"\n"
                                                                           f'\n**Address**: `{Address}`'
                                                                           f'\n**Invite Link**: https://www.spotify.com/{country.lower()}/family/join/invite/{inviteToken}'
                                                                           f'\n**You can add random {country.upper()} address if these fields are empty.**'
                                                                           )
                                                bot.codes.remove(code)  # Remove code from codes list after user got invite code.
                                                with open("codes.txt", "a") as file:
                                                    file.truncate(0)
                                                    for code in bot.codes:
                                                        file.write(f"{code}\n")
                                                result = "true"
                                                break
                                            elif Slots is False:
                                                tries += 1
                                                if Debug == "Debug":
                                                    print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                                    print(Fore.RESET)
                                                embed = discord.Embed(
                                                title=f"There were some issues, retrying.", color=0xd3d3d3)
                                                await message.edit(embed=embed)
                                                with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                                    for line in lines:
                                                        if line.strip("\n") != f"{user}:{password}":
                                                            f.write(line)
                                                result = 'false'
                                    else:
                                        tries += 1
                                        if Debug == "Debug":
                                            print(Fore.RED + f"Failed to upgrade {ctx.author} retrying...({tries})")
                                            print(Fore.RESET)
                                        embed = discord.Embed(
                                        title=f"There were some issues, retrying.", color=0xd3d3d3)
                                        await message.edit(embed=embed)
                                        with open(f"Accounts/{country.upper()}.txt", "w") as f:
                                            for line in lines:
                                                if line.strip("\n") != f"{user}:{password}":
                                                    f.write(line)
                                        result = 'false'
                        if result == "true":
                            break
                        if tries >= 6:
                            if Debug == "Debug":
                                            print(Fore.RED + f"Failed to upgrade user bacuse of too many fails")
                                            print(Fore.RESET)
                            embed = discord.Embed(
                                        title=f"Oops, we're not able to upgrade your account at the moment, please try again later.", color=0xff5959)
                            await message.edit(embed=embed)
                            print(Fore.RED + f"Seems like there are some issues with {country.upper()} please check your stock if there isn't something weird happening.")
                            print(Fore.RESET)
                            return
            else:
                if Debug == "Debug":
                    print(Fore.RED + f"User {ctx.author} tried to upgrade with invalid email address {email}")
                    print(Fore.RESET)
                embed = discord.Embed(
                    title=f"Please use valid email address in order to upgrade your account.", color=0xff5959)
                await ctx.send(embed=embed)
        else: 
            embed = discord.Embed(
                title=f"You can only use this command in #{Channel}", color=0xd3d3d3)
            message = await ctx.send(embed=embed)
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
    print(Fore.RESET)
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


@bot.command()
@commands.has_role(f'{Role}')  # Checking if user is allowed to use this command.
async def restock(ctx, country: str):
    """ This command can be used to restock accounts.
        Country = Country you want to restock accounts in.
        In case you want to rest all countries use !restock all
    """
    await ctx.channel.purge(limit=1)  # Deleting the restock message
    print(Fore.GREEN + f'@{ctx.author} restocked stocks')
    print(Fore.RESET)
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
async def credits(ctx):
    """ Credits to who coded this bot"""
    print(Fore.YELLOW + f'@{ctx.author} used !credits')
    print(Fore.RESET)
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(f"```Open source spotify bot full developed by matt"
                          f"\nhttps://www.nulled.to/user/2158082-matoooo"
                          f"\nDesign made using a guide from Billie"
                          f"\nhttps://www.nulled.to/user/1236023-billieeilish"
                          f"\nhttps://www.nulled.to/topic/835795-free-source-code-how-to-make-your-python-tools-look-cooler-colors-and-ascii-art/```"
                          )
    print(f"Open source spotify bot full developed by matt"
                          f"\nhttps://www.nulled.to/user/2158082-matoooo"
                          f"\nDesign made using a guide from Billie"
                          f"\nhttps://www.nulled.to/user/1236023-billieeilish"
                          f"\nhttps://www.nulled.to/topic/835795-free-source-code-how-to-make-your-python-tools-look-cooler-colors-and-ascii-art/"
                          )


@bot.command()
async def cls(ctx):
    """You can use this command to clean console."""
    print(Fore.YELLOW + f'@{ctx.author} used !cls')
    print(Fore.RESET)
    os.system('cls')
    print(Fore.GREEN + """
     __             _   _  __         _           _   
    / _\_ __   ___ | |_(_)/ _|_   _  | |__   ___ | |_ 
    \ \| '_ \ / _ \| __| | |_| | | | | '_ \ / _ \| __|
    _\ \ |_) | (_) | |_| |  _| |_| | | |_) | (_) | |_ 
    \__/ .__/ \___/ \__|_|_|  \__, | |_.__/ \___/ \__|
       |_|                    |___/                   
     _                             _   _              
    | |__  _   _   _ __ ___   __ _| |_| |_            
    | '_ \| | | | | '_ ` _ \ / _` | __| __|           
    | |_) | |_| | | | | | | | (_| | |_| |_            
    |_.__/ \__, | |_| |_| |_|\__,_|\__|\__|           
           |___/                                      
    """)
    print(Fore.RESET)
@bot.event
async def on_command_error(ctx,exception):
    if Debug == "Debug":
        print(Fore.RESET)
        print(Fore.RED +f"@{ctx.author} tried to upgrade his account but got an exception: {exception}")
        print(Fore.RESET)
    if isinstance(exception, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            title=f'You need to enter redeem code behind your email ({data["Prefix"]}redeem country email code)', color=0xff5959)
        message = await ctx.send(embed=embed)
bot.run(token)
