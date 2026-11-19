"""
plugins/utility/utility_cog.py
Utility commands: weather, translate, poll, remind, avatar, server/user info, vc247, calculator.
"""
import ast
import operator
import asyncio
import re
import datetime
import discord
import aiohttp
import psutil
import time
from discord.ext import commands
from config import PREFIX, WEATHER_API_KEY
from plugins.music.player import PERMA_VC
from utils import get_afk_data, save_afk_data


# ── Safe Calculator Evaluator ──────────────────────────────────────────────────
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval_math(expr: str):
    """
    Safely evaluate arithmetic expressions using the AST module.
    Prevents code execution, variable injection, and excessive exponent CPU DoS.
    """
    clean_expr = expr.replace(" ", "").replace("^", "**")
    if not re.match(r"^[\d+\-*/().%\s*]+$", clean_expr):
        raise ValueError("Invalid characters — only numbers and `+ - * / ^ %` allowed.")

    tree = ast.parse(clean_expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric literals are allowed.")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Operator {op_type.__name__} is not supported.")
            if op_type is ast.Pow:
                if abs(right) > 1000 or abs(left) > 100000:
                    raise ValueError("Exponent or base is too large.")
            return SAFE_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Operator {op_type.__name__} is not supported.")
            return SAFE_OPERATORS[op_type](operand)
        else:
            raise ValueError("Unsupported expression syntax.")

    return _eval(tree)


class UtilityCog(commands.Cog, name="Utility"):
    """🔧 Utility and miscellaneous commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()
        self.snipes: dict[int, dict] = {}  # channel_id: {content, author_name, author_avatar, time}
        self.vc_tasks: dict[int, asyncio.Task] = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        # Store snipe data with bounded cache size to avoid memory leaks
        if len(self.snipes) > 100:
            self.snipes.pop(next(iter(self.snipes)))
        self.snipes[message.channel.id] = {
            "content": message.content,
            "author_name": message.author.display_name,
            "author_avatar": message.author.display_avatar.url,
            "time": datetime.datetime.now(datetime.timezone.utc),
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Check AFK for author (remove AFK)
        afk_data = get_afk_data()
        user_id = str(message.author.id)
        if user_id in afk_data:
            del afk_data[user_id]
            save_afk_data(afk_data)
            try:
                await message.channel.send(f"Welcome back {message.author.mention}, I removed your AFK.")
            except discord.Forbidden:
                pass

        # Check AFK for mentioned users
        for mention in message.mentions:
            m_id = str(mention.id)
            if m_id in afk_data:
                reason = afk_data[m_id]
                try:
                    await message.channel.send(f"💤 **{mention.display_name}** is currently AFK: {reason}")
                except discord.Forbidden:
                    pass

    @commands.hybrid_command()
    async def snipe(self, ctx: commands.Context):
        """Get the last deleted message in this channel. Usage: !snipe"""
        snipe_data = self.snipes.get(ctx.channel.id)
        if not snipe_data:
            return await ctx.send("❌ There's nothing to snipe!")

        embed = discord.Embed(
            description=snipe_data["content"] or "*No text (embed/image only)*",
            color=discord.Color.blue(),
            timestamp=snipe_data["time"]
        )
        embed.set_author(
            name=snipe_data["author_name"],
            icon_url=snipe_data["author_avatar"]
        )
        embed.set_footer(text="Sniped message")
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def afk(self, ctx: commands.Context, *, reason: str = "AFK"):
        """Set your status to AFK. Usage: !afk [reason]"""
        data = get_afk_data()
        data[str(ctx.author.id)] = reason[:200]
        save_afk_data(data)
        await ctx.send(f"✅ {ctx.author.mention} I set your AFK: {reason[:200]}")

    @commands.hybrid_command(aliases=["calc"])
    async def calculator(self, ctx: commands.Context, *, expression: str):
        """Evaluate a math expression safely. Usage: !calc <expression>"""
        try:
            result = safe_eval_math(expression)
            embed = discord.Embed(title="🧮 Calculator", color=discord.Color.blue())
            embed.add_field(name="Expression", value=expression, inline=False)
            embed.add_field(name="Result", value=str(result), inline=False)
            await ctx.send(embed=embed)
        except ZeroDivisionError:
            await ctx.send("❌ Cannot divide by zero!")
        except Exception as e:
            await ctx.send(f"❌ Calculation error: {e}")

    @commands.hybrid_command()
    async def translate(self, ctx: commands.Context, target_lang: str, *, text: str):
        """Translate text. Usage: !translate <lang_code> <text>"""
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {"client": "gtx", "sl": "auto", "tl": target_lang, "dt": "t", "q": text}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        return await ctx.send("❌ Failed to translate. Try again later.")
                    data = await resp.json()
                    translated = data[0][0][0]
                    src_lang = data[2]
            embed = discord.Embed(title="🌐 Translation", color=discord.Color.blue())
            embed.add_field(name=f"Original ({src_lang})", value=text, inline=False)
            embed.add_field(name=f"Translated ({target_lang})", value=translated, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Translation error: {e}")

    @commands.hybrid_command()
    async def weather(self, ctx: commands.Context, *, location: str):
        """Get weather for a location. Usage: !weather <city>"""
        if not WEATHER_API_KEY:
            return await ctx.send("❌ Weather API key is not configured.")
        try:
            params = {"q": location, "appid": WEATHER_API_KEY, "units": "metric"}
            async with aiohttp.ClientSession() as session:
                async with session.get("http://api.openweathermap.org/data/2.5/weather", params=params) as resp:
                    if resp.status != 200:
                        return await ctx.send("❌ Could not find that location.")
                    data = await resp.json()
            embed = discord.Embed(
                title=f"⛅ Weather in {data['name']}, {data.get('sys', {}).get('country', '')}",
                description=f"**{data['weather'][0]['description'].title()}**",
                color=discord.Color.blue(),
            )
            embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
            embed.add_field(name="🌡️ Temperature", value=f"{data['main']['temp']}°C (feels {data['main']['feels_like']}°C)", inline=True)
            embed.add_field(name="💧 Humidity", value=f"{data['main']['humidity']}%", inline=True)
            embed.add_field(name="🌬️ Wind", value=f"{data['wind']['speed']} m/s", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command()
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """Create a poll. Usage: !poll "Question" "Option1" "Option2" ..."""
        if len(options) < 2:
            return await ctx.send("❌ Provide at least 2 options.")
        if len(options) > 10:
            return await ctx.send("❌ Maximum 10 options.")
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        desc = "\n".join(f"{emojis[i]} {opt}" for i, opt in enumerate(options))
        embed = discord.Embed(
            title=f"📊 Poll: {question}",
            description=desc,
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(emojis[i])

    @commands.hybrid_command()
    async def remind(self, ctx: commands.Context, time_str: str, *, reminder: str):
        """Set a reminder. Usage: !remind 1h30m <reminder>"""
        try:
            seconds = 0
            t = time_str.lower()
            for unit, secs in [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]:
                if unit in t:
                    idx = t.index(unit)
                    num_str = "".join(c for c in t[:idx] if c.isdigit())
                    if num_str:
                        seconds += int(num_str) * secs
                    t = t[idx + 1:]
            if seconds <= 0:
                return await ctx.send("❌ Provide a valid time (e.g. 1h30m).")
            await ctx.send(f"⏰ I'll remind you in **{time_str}**: {reminder}")
            await asyncio.sleep(seconds)
            embed = discord.Embed(
                title="⏰ Reminder",
                description=reminder,
                color=discord.Color.gold(),
            )
            embed.set_footer(text=f"Set {time_str} ago")
            await ctx.author.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Failed to set reminder: {e}")

    @commands.hybrid_command()
    @commands.has_permissions(manage_channels=True)
    async def vc247(self, ctx: commands.Context):
        """Make the bot stay in VC 24/7. Usage: !vc247"""
        if not ctx.author.voice:
            return await ctx.send("❌ Join a voice channel first!")
        vc = ctx.voice_client
        if vc and vc.is_connected():
            if vc.channel != ctx.author.voice.channel:
                await vc.move_to(ctx.author.voice.channel)
        else:
            vc = await ctx.author.voice.channel.connect()
        PERMA_VC[ctx.guild.id] = True

        if ctx.guild.id in self.vc_tasks and not self.vc_tasks[ctx.guild.id].done():
            return await ctx.send("🔊 24/7 VC is already active in this server. Use `!leave` to stop.")

        channel = ctx.author.voice.channel

        async def maintain():
            while PERMA_VC.get(ctx.guild.id):
                current_vc = ctx.guild.voice_client
                if not current_vc or not current_vc.is_connected():
                    try:
                        await channel.connect()
                    except Exception:
                        pass
                await asyncio.sleep(10)

        task = asyncio.create_task(maintain())
        self.vc_tasks[ctx.guild.id] = task
        await ctx.send("🔊 Bot will stay in VC 24/7. Use `!leave` to stop.")

    @commands.hybrid_command()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        """Get a user's avatar. Usage: !avatar [@user]"""
        target = member or ctx.author
        embed = discord.Embed(title=f"{target.display_name}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def serverinfo(self, ctx: commands.Context):
        """Get server information. Usage: !serverinfo"""
        g = ctx.guild
        embed = discord.Embed(title=f"Server: {g.name}", color=discord.Color.blue())
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="Owner", value=g.owner.mention if g.owner else "Unknown", inline=True)
        embed.add_field(name="Created", value=g.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Members", value=g.member_count, inline=True)
        embed.add_field(name="Roles", value=len(g.roles), inline=True)
        embed.add_field(name="Channels", value=f"Text: {len(g.text_channels)}  Voice: {len(g.voice_channels)}", inline=True)
        embed.add_field(name="Boosts", value=g.premium_subscription_count, inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        """Get user information. Usage: !userinfo [@user]"""
        target = member or ctx.author
        embed = discord.Embed(title=f"User: {target.display_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="ID", value=target.id, inline=True)
        embed.add_field(name="Nickname", value=target.nick or "None", inline=True)
        embed.add_field(name="Account Created", value=target.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Joined Server", value=target.joined_at.strftime("%B %d, %Y") if target.joined_at else "Unknown", inline=True)
        roles = [r.mention for r in target.roles if r.name != "@everyone"]
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=" ".join(roles) if roles else "None",
            inline=False,
        )
        if ctx.message:
            try:
                await ctx.message.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["binfo", "stats"])
    async def botinfo(self, ctx: commands.Context):
        """Show detailed statistics about the bot."""
        process = psutil.Process()
        memory_usage = process.memory_full_info().uss / 1024**2
        cpu_usage = process.cpu_percent()

        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"

        embed = discord.Embed(
            title="🤖 Bot Statistics",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(name="Ping", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        embed.add_field(name="Uptime", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="Memory", value=f"`{memory_usage:.2f} MB`", inline=True)

        embed.add_field(name="CPU", value=f"`{cpu_usage}%`", inline=True)
        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Users", value=f"`{sum(g.member_count for g in self.bot.guilds if g.member_count)}`", inline=True)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["rinfo"])
    async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
        """Show detailed information about a role."""
        embed = discord.Embed(
            title=f"Role: {role.name}",
            color=role.color,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        embed.add_field(name="ID", value=f"`{role.id}`", inline=True)
        embed.add_field(name="Color", value=f"`{role.color}`", inline=True)
        embed.add_field(name="Position", value=f"`{role.position}`", inline=True)

        embed.add_field(name="Members", value=f"`{len(role.members)}`", inline=True)
        embed.add_field(name="Mentionable", value=f"`{'Yes' if role.mentionable else 'No'}`", inline=True)
        embed.add_field(name="Hoisted", value=f"`{'Yes' if role.hoist else 'No'}`", inline=True)

        created_at = role.created_at.strftime("%b %d, %Y")
        embed.add_field(name="Created At", value=f"`{created_at}`", inline=True)

        key_perms = []
        if role.permissions.administrator: key_perms.append("Administrator")
        if role.permissions.manage_guild: key_perms.append("Manage Server")
        if role.permissions.manage_roles: key_perms.append("Manage Roles")
        if role.permissions.manage_channels: key_perms.append("Manage Channels")
        if role.permissions.manage_messages: key_perms.append("Manage Messages")
        if role.permissions.ban_members: key_perms.append("Ban Members")
        if role.permissions.kick_members: key_perms.append("Kick Members")

        if key_perms:
            embed.add_field(name="Key Permissions", value=", ".join(f"`{p}`" for p in key_perms), inline=False)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(UtilityCog(bot))
