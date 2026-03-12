import discord
from dotenv import load_dotenv
import os
load_dotenv()
from discord.ext import commands
import random
import requests
from datetime import datetime

# ─────────────────────────────────────────
#  BOT SETUP
# ─────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
# Channel names for organized bot responses
TRIVIA_CHANNEL = "trivia"
BOT_COMMANDS_CHANNEL = "bot-commands"
LEVEL_UPS_CHANNEL = "level-ups"

bot = commands.Bot(command_prefix="!", intents=intents)

# ─────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"👋 Welcome to the server, {member.mention}! Check the rules and enjoy your stay!")

# ─────────────────────────────────────────
#  FUN COMMANDS
# ─────────────────────────────────────────
@bot.command()
async def hello(ctx):
    """Say hello to the bot"""
    await ctx.send(f"Hey {ctx.author.mention}! I am alive and ready!")

@bot.command()
async def roll(ctx, sides: int = 6):
    """Roll a dice. Usage: !roll 20"""
    result = random.randint(1, sides)
    await ctx.send(f"You rolled a {result} (d{sides})")

@bot.command()
async def flip(ctx):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on {result}!")

@bot.command()
async def joke(ctx):
    """Get a random programming joke"""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache!",
        "A SQL query walks into a bar and asks two tables: 'Can I join you?'",
        "Why do Java developers wear glasses? Because they don't C#!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def choose(ctx, *options):
    """Choose between options. Usage: !choose pizza burger tacos"""
    if len(options) < 2:
        await ctx.send("Give me at least 2 options! Example: !choose pizza burger tacos")
        return
    await ctx.send(f"I choose... {random.choice(options)}!")

# ─────────────────────────────────────────
#  UTILITY COMMANDS
# ─────────────────────────────────────────
@bot.command()
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")

@bot.command()
async def poll(ctx, question: str, *options):
    """Create a poll. Usage: !poll "Best language?" Python JavaScript Rust"""
    if len(options) < 2:
        await ctx.send('Provide a question and at least 2 options!\nExample: !poll "Best food?" Pizza Burger Tacos')
        return

    emojis = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    description = "\n".join([f"{emojis[i]}. {opt}" for i, opt in enumerate(options[:10])])

    embed = discord.Embed(
        title=f"Poll: {question}",
        description=description,
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"Poll by {ctx.author.display_name}")
    message = await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, *, city: str):
    """Get weather for a city. Usage: !weather Lagos"""
    api_key = "YOUR_OPENWEATHER_API_KEY"  # Get free key at openweathermap.org
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await ctx.send(f"City '{city}' not found!")
            return

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]

        embed = discord.Embed(title=f"Weather in {city.title()}", color=discord.Color.orange())
        embed.add_field(name="Temperature", value=f"{temp}C (feels like {feels_like}C)", inline=False)
        embed.add_field(name="Condition", value=description, inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Could not fetch weather. Check your API key!")

@bot.command()
async def serverinfo(ctx):
    """Show server information"""
    guild = ctx.guild
    embed = discord.Embed(title=guild.name, color=discord.Color.green())
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Channels", value=len(guild.text_channels), inline=True)
    await ctx.send(embed=embed)

    # ─────────────────────────────────────────
#  TRIVIA GAME
# ─────────────────────────────────────────
trivia_questions = [
    {"question": "What is the capital of France?", "answer": "paris"},
    {"question": "How many sides does a hexagon have?", "answer": "6"},
    {"question": "What programming language is this bot written in?", "answer": "python"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What planet is closest to the sun?", "answer": "mercury"},
    {"question": "How many bytes are in a kilobyte?", "answer": "1024"},
    {"question": "What is the largest ocean on Earth?", "answer": "pacific"},
    {"question": "Who created Python programming language?", "answer": "guido van rossum"},
]

trivia_scores = {}
active_trivia = {}

@bot.command()
async def trivia(ctx, arg=None):
    """Start a trivia question or check scores"""
    if arg == "score":
        if not trivia_scores:
            await ctx.send("No scores yet! Start a game with !trivia")
            return
        leaderboard = sorted(trivia_scores.items(), key=lambda x: x[1], reverse=True)
        result = "**Trivia Leaderboard**\n"
        for i, (user, score) in enumerate(leaderboard[:5], 1):
            result += f"{i}. {user} — {score} points\n"
        await ctx.send(result)
        return

    if ctx.channel.id in active_trivia:
        await ctx.send("A trivia question is already active! Answer it first!")
        return

    question = random.choice(trivia_questions)
    active_trivia[ctx.channel.id] = question["answer"]

    await ctx.send(f"**TRIVIA TIME!** 🎮\n{question['question']}\n*First to answer correctly wins a point!*")

    def check(m):
        return m.channel == ctx.channel and not m.author.bot

    try:
        while True:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower().strip() == active_trivia[ctx.channel.id]:
                del active_trivia[ctx.channel.id]
                username = msg.author.display_name
                trivia_scores[username] = trivia_scores.get(username, 0) + 1
                await ctx.send(f"🎉 {msg.author.mention} got it right! The answer was **{question['answer']}**! You now have **{trivia_scores[username]}** points!")
                break
    except:
        del active_trivia[ctx.channel.id]
        await ctx.send(f"⏰ Time's up! The answer was **{question['answer']}**!")

        # ─────────────────────────────────────────
#  XP & LEVELING SYSTEM
# ─────────────────────────────────────────
xp_data = {}

def get_level(xp):
    return int(xp ** 0.4)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 0, "name": message.author.display_name}

    old_level = xp_data[user_id]["level"]
    xp_data[user_id]["xp"] += random.randint(5, 15)
    xp_data[user_id]["name"] = message.author.display_name
    new_level = get_level(xp_data[user_id]["xp"])
    xp_data[user_id]["level"] = new_level

    if new_level > old_level:
   level_channel = discord.utils.get(message.guild.text_channels, name=LEVEL_UPS_CHANNEL)
        channel = level_channel or message.channel
        await channel.send(f"🎉 {message.author.mention} just leveled up to **Level {new_level}!** Keep chatting!")

    await bot.process_commands(message)

@bot.command()
async def rank(ctx, member: discord.Member = None):
    """Check your XP and level. Usage: !rank or !rank @user"""
    member = member or ctx.author
    user_id = str(member.id)

    if user_id not in xp_data:
        await ctx.send(f"{member.display_name} hasn't earned any XP yet!")
        return

    xp = xp_data[user_id]["xp"]
    level = xp_data[user_id]["level"]
    next_level_xp = ((level + 1) ** (1/0.4))

    embed = discord.Embed(title=f"{member.display_name}'s Rank", color=discord.Color.gold())
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="XP", value=xp, inline=True)
    embed.add_field(name="Next Level", value=f"{int(next_level_xp)} XP", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    """Show top 5 members by XP"""
    if not xp_data:
        await ctx.send("Nobody has earned XP yet! Start chatting!")
        return

    sorted_users = sorted(xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:5]
    embed = discord.Embed(title="XP Leaderboard", color=discord.Color.gold())
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, (user_id, data) in enumerate(sorted_users):
        embed.add_field(
            name=f"{medals[i]} {data['name']}",
            value=f"Level {data['level']} — {data['xp']} XP",
            inline=False
        )
    await ctx.send(embed=embed)

# ─────────────────────────────────────────
#  RUN THE BOT
# ─────────────────────────────────────────
bot.run(os.getenv("DISCORD_TOKEN"))
