import discord
import os
from discord.ext import commands
import re
import random
import asyncio

# info #
BOT_PREFIX = os.environ['prefix']
TOKEN = os.environ['token']
desc = "Disclaimer: Does not actually give advice"
game = "DM me for advice!"
bot = commands.Bot(command_prefix=BOT_PREFIX)
ID = '506532714279862272'
platform = {'PC' : 4}

# roles #
owner_role = None
mod_role = None
test_role = None
testmrole = None
raider_role = None
member_role = None

# channels #
generalc = None
memec = None
metac = None
consolec = None
mailc = None
testc = None

# servers #
test_server = None
sga_server = None

# colors #
outbox = discord.Colour.orange()
inbox = discord.Colour.blue()
color = discord.Colour(0x3541d4)

# misc #
selected_user = None
last_pm_user = None
pm_user_list = [None] * 10
riddle = None
i = None
num = None
me = None
@bot.event
async def on_ready():
    global owner_role
    global mod_role
    global test_role
    global generalc
    global memec
    global metac
    global testc
    global test_server
    global sga_server
    global selected_user
    global last_pm_user
    global consolec
    global riddle
    global i
    global raider_role
    global mailc
    global testmrole
    global num
    global member_role
    global me
    generalc = bot.get_channel('570609373051748370')
    #memec = bot.get_channel('')
    #metac = bot.get_channel('')
    mailc = bot.get_channel('621707814095552522')
    testc = bot.get_channel('621707829874655317')
    consolec = bot.get_channel('621707842566750219')

    test_server = bot.get_server('570609373051748368')
    #sga_server = bot.get_server('455521454528659485')

    #owner_role = discord.utils.get(sga_server.roles, id='455802683312439297')
    #mod_role = discord.utils.get(sga_server.roles, id='455803368548597781')
    #member_role = discord.utils.get(sga_server.roles, id='455804701292757005')

    test_role = discord.utils.get(test_server.roles, id='570609529553813525')
    testmrole = discord.utils.get(test_server.roles, id='621707401023848464')


    me = test_server.get_member('270265832313978891')
    #me = sga_server.get_member('270265832313978891')
    selected_user = me
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # imgur mirror of avatar https: // imgur.com / a / ydTGylX
    await bot.change_presence(game=discord.Game(name=game))
    embed = discord.Embed(title="SGA has restarted", colour=discord.Colour(0x3541d4), url="https://www.youtube.com/watch?v=HRPwMBAtfTY")
    embed.set_thumbnail(url="https://66.media.tumblr.com/13183110dbf9fbfbfb55fe287d15f05f/tumblr_inline_ns3spgZjVg1sgo7fg_1280.jpg") #add icon
    embed.set_author(name="Super Good Advice", url="https://www.youtube.com/watch?v=HRPwMBAtfTY",
                     icon_url="https://66.media.tumblr.com/13183110dbf9fbfbfb55fe287d15f05f/tumblr_inline_ns3spgZjVg1sgo7fg_1280.jpg") #here too
    embed.set_footer(text="Bot by " + me.display_name, icon_url=me.avatar_url)

    await bot.send_message(testc, embed=embed)

    i = 0
    pm_user_list.clear()
    for c in bot.private_channels:
        if (i >= 10):
            break
        pm_user_list.append(c.user)



async def in_console(ctx):
    console_channels = set([consolec.id, mailc.id, testc.id])
    okay = (ctx.message.channel.id in console_channels) or (ctx.message.server.id == test_server.id)
    if not okay:
        await bot.delete_message(ctx.message)
    return okay

'''async def in_spam_allowed(ctx):
    spam_channels = set([testc.id])
    okay = (not (ctx.message.channel.id in spam_channels)) or (ctx.message.server.id == test_server.id)
    if not okay:
        await bot.delete_message(ctx.message)
    return okay'''
async def select_user(who: discord.User):
    rec = sga_server.get_member(who.id)
    global selected_user
    selected_user = rec
    embed = discord.Embed(title="User selected", colour=rec.colour)

    embed.set_author(name=selected_user.display_name, icon_url=rec.avatar_url)
async def message_embed(chan: discord.Channel, msg: discord.Message):
    pillc = None
    if msg.channel.is_private :
        if msg.author.id == ID:
            return
        else:
            pillc = inbox
    else:
        pillc = msg.author.colour

    em = discord.Embed(title='', description=msg.content, colour=pillc)
    em.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
    ft = "sent via PM"
    em.set_footer(text=ft)
    await bot.send_message(destination=chan, embed=em)

async def sent_embed(who: discord.User, chan: discord.Channel, msg: discord.Message):
    pillc = outbox

    em = discord.Embed(title='', description=msg.content, colour=pillc)
    em.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
    ft = "PM sent to " + who.name
    em.set_footer(text=ft)

    await bot.send_message(destination=chan, embed=em)

async def pm_embed(who: discord.User, chan: discord.Channel, msg: discord.Message):
    if (msg.author.id == bot.user.id):
        await sent_embed(who, chan)
    else:
        await message_embed(chan, msg)

@bot.command(pass_context=True)
async def dice(ctx):
    if await in_console(ctx):
        msg = str(random.randint(1,6))
        await bot.say(msg)

@bot.command(pass_context=True)
async def sga(ctx, branch: int, who: discord.User):
    if await in_console(ctx):
        roles = ["512673489430380546", mod_role.id]
        for y in ctx.message.author.roles:
            if y.id in roles:
                global num
                global member_role
                if branch == 2:
                    num = "[SGA2] "
                else:
                    num = "[SGA] "
                user = who.display_name
                await bot.change_nickname(who, num + user)
                await bot.add_roles(who, member_role)
                await bot.say("Done")
                await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def riddle():
    global riddle
    r = ['I start with M and end with X. I have a never ending amount of letters. What am I?',
         "A man was stabbed in the heart, no one tried to save him but he didn’t die. How is that possible?",
         "The maker doesn’t want it, the buyer doesn’t use it and the user doesn’t know it. What is it?",
         'Most people need it, some ask for it, some give it, but almost nobody takes it. What is it?',
         "I have keys but no locks. I have space but no room. You can enter but can't go outside. What am I?",
         "If you say my name I am no longer there. What am I?"]
    a = ['A mailbox!', 'He was already dead!', 'A coffin!', 'Advice!', 'A keyboard!', 'Silence!']
    riddle = random.randint(0, 5)
    await bot.say(r[riddle])
    await bot.say('You have 20 seconds before the answer is given')
    await asyncio.sleep(20)
    await bot.say(a[riddle])


@bot.command(pass_context=True)
async def say(ctx, chan: discord.Channel, *msg_in: str):
    if await in_console(ctx):
        msg = ' '.join(msg_in)
        await bot.send_message(chan, msg)
        await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def pm(ctx, rec: discord.User, *msg_in: str):
    if rec.id != bot.user.id:
        await select_user(rec)

    if await in_console(ctx):
        msg = ' '.join(msg_in)
        mes = await bot.send_message(selected_user, msg)
        await sent_embed(selected_user, mailc, mes)
        await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def question(ctx, x):
    await bot.say("Let me search that for you")
    await asyncio.sleep(3)
    await bot.say("This is what I found: <https://goo.gl/8DS6ni>")



def word_filter(mes: str):
    s = mes.replace("1", "i").replace("3", "e").replace("4", "a").replace("5", "s").replace("9", "g").replace("0",
                                                                                                              "o").replace(
        "!", "i").lower()
    regex = re.compile('[^a-z]')
    s = regex.sub('', s)
    b = ("nigg" in s) or ("chink" in s) or ("faggot" in s)
    return b



@bot.event
async def on_message(message):
    global last_pm_user
    global mailc
    if message.channel.is_private:
        await message_embed(mailc, message)
        if message.author.id != ID:
            last_pm_user = message.author
            await bot.send_message(mailc, "PM recieved")

    else:
        console_channels = set([consolec.id, mailc.id]) #, adminc.id
        if not message.channel.id in console_channels:
            if word_filter(message.content):
                await bot.delete_message(message)

    try:
        await bot.process_commands(message)
    except ('InvalidArgument', 'CommandInvokeError'):
        pass

file = open('config.json', 'r')
contents = file.read()

bot.run(TOKEN) #token
