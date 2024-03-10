import discord
from discord.ext import commands


listening_channel = set()

# Define the intents
intents = discord.Intents.all()

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    print(f'Currently at {len(bot.guilds)} servers!')
    print('Servers connected to:')
    print('')
    for server in bot.guilds:
        print(server.name)
        for channel in server.text_channels:
            print(channel)
    print('------')


async def send_message(message: str, reply_to: discord.Message = None) -> list:
    try:
        # print("Sending Message!!!!")
        # print(message)
        sent_msgs = []
        for channel in listening_channel:
            # print(f"Sending Message to {channel}!!!!")
            filtered = None 
            if reply_to:
                filtered = list(filter(lambda x: channel.id == x.channel.id, reply_to))
            msg = await channel.send(message, reference=filtered[0] if filtered else None)
            # print('Sent!')
            # print(msg)
            sent_msgs.append(msg)
        # print(len(sent_msgs))
        return sent_msgs
    except Exception as e:
        print(e)


# Event: Message received
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to avoid an infinite loop
    # if message.author == bot.user:
    #     return

    # if not message.content.lower().startswith('!'):
    #     return

    # if message.content.lower() == '!listen':
    #     listening_channel.add(message.channel)
        
    # elif message.content.lower() == '!unlisten':
    #     listening_channel.remove(message.channel) if message in listening_channel else None
    # global previous_message

    # Check if the message content is 'hello' and react to the previous message
    # if message.content.lower() == 'hello':
    #     if previous_message:
    #         await previous_message.add_reaction('👍')
    # print(message)
    # Update the previous_message variable for the next iteration
    # previous_message = message
    # print(message)
    # Continue processing other commands and events
    await bot.process_commands(message)
    # print(123123213)

# Command: !hello
@bot.command(name='hello')
async def hello(ctx):
    for channel in listening_channel:
        await channel.send(f"Hello to {channel}")
    # print(ctx.channel.id)
    # print(await ctx.send('Hello!'))
    
@bot.command(name='listen')
async def add_listening_channel(ctx):
    if ctx.channel not in listening_channel:
        listening_channel.add(ctx.channel)
        print(listening_channel)
        await ctx.send("This channel is now listening")

@bot.command(name='unlisten')
async def remove_listening_channel(ctx):
    if ctx.channel in listening_channel:
        listening_channel.remove(ctx.channel) 
        print(listening_channel)
        await ctx.send("This channel will not listen anymore")