import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os   

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents )

secretRole = "idk"

@bot.event
async def on_ready():
    print(f"Im Up and Im working, From {bot.user.name}")

@bot.event
async def on_member_join(member):
    print(f"OH BOY I cant wait to call {member} a slur.")

@bot.event
async def on_message(message):
    # Prevents the bot from responding to its own messages, which could lead to infinite loops.
    if message.author == bot.user:
        return
    
    # Check if the message starts with the command prefix and process commands if it does.
    if message.content.startswith('!AmIRightorAmIRight'):
        await message.channel.send(f'Yea you right {message.author.mention}!')

    # Check for banned phrases and delete the message if found, then send a warning to the user.
    if "slowing hex" in message.content.lower():
        await message.delete()
        await message.channel.send(f"Hey {message.author.mention}, please refrain from talking about Slowing Hex.")

    await bot.process_commands(message)    

# This is a simple command that responds with a greeting when a user types "!hello".
@bot.command()
async def hello(ctx): #ctx stands for context
    await ctx.send(f"Hello {ctx.author.mention}!")

# This command assigns a role to the user who invoked it. If the role doesn't exist, it sends a message indicating that the role is unavailable.
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secretRole)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has woken up to immense power!")
    else:
        await ctx.send(f"{ctx.author.mention} Wanted all the cake but but Jospeh ate them all :(")

# This command removes a role from the user who invoked it. If the role doesn't exist, it sends a message indicating that the role was never assigned.
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secretRole)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been smited by Tom Cruise during their Scientology Speedrun!")
    else:
        await ctx.send(f"{ctx.author.mention}, How can one remove what never existed? -Master Joseph 200 B.C.E")

# This command sends a direct message to the user who invoked it, warning them about the content of their message and threatening to call them a name in DMs if they say it again.
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"{ctx.author.mention}, you can't be saying \"{msg}\" next time imma have to call you a name in DMs.")

# This command replies to the user's message with a sarcastic remark, indicating that they are correct in a humorous way.
@bot.command()
async def reply(ctx):
    await ctx.reply(f"Really thats how it is huh {ctx.author}?")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question, color=0x00ff00)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

# This command is restricted to users with a specific role. If the user has the required role, it sends a message boasting about their superiority. If the user does not have the required role, it sends a message indicating that they are not worthy.
@bot.command()
@commands.has_role(secretRole)
async def secret(ctx):
    await ctx.send(f"{ctx.author.mention} just wanted to let you guys know that they are better then you and that you all mean nothing to them. They are the best and you all suck.")

# This error handler is triggered when a user without the required role tries to invoke the "secret" command. It sends a message indicating that the user is not worthy and needs to train for another 300 years to even think about using the command.  
@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention}, you are not worthy you must train another 300 years to even think about this command.")



bot.run(token, log_handler=handler, log_level=logging.DEBUG)