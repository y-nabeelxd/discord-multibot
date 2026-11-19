"""
test_load.py - Automated verification test suite for Discord MultiBot.
Tests loading of all cogs, commands registration, and security evaluator.
"""
import sys
import asyncio
import discord
from discord.ext import commands

EXTENSIONS = [
    "plugins.music.music_cog",
    "plugins.moderation.moderation_cog",
    "plugins.verification.verification_cog",
    "plugins.fun.fun_cog",
    "plugins.economy.economy_cog",
    "plugins.utility.utility_cog",
    "plugins.slash.slash_cog",
    "plugins.leveling.leveling_cog",
    "plugins.ticket.ticket_cog",
    "plugins.giveaway.giveaway_cog",
]

async def run_tests():
    print("=" * 60)
    print("RUNNING EXTENSION & COG LOAD TESTS")
    print("=" * 60)

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    failed = []
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f" [PASS] Loaded {ext}")
        except Exception as e:
            failed.append((ext, str(e)))
            print(f" [FAIL] Failed to load {ext}: {e}")

    print("-" * 60)
    total_cmds = len(bot.commands)
    total_app_cmds = len(bot.tree.get_commands())
    print(f"Total prefix/hybrid commands registered: {total_cmds}")
    print(f"Total slash commands in tree: {total_app_cmds}")
    print("-" * 60)

    print("TESTING SAFE CALCULATOR EVALUATOR...")
    from plugins.utility.utility_cog import safe_eval_math

    test_cases = [
        ("2 + 2", 4),
        ("10 - 3 * 2", 4),
        ("(100 / 4) * 2", 50.0),
        ("2 ^ 10", 1024),
        ("50 % 7", 1),
        ("-5 + 10", 5),
    ]

    for expr, expected in test_cases:
        res = safe_eval_math(expr)
        assert res == expected, f"Expected {expected} for {expr}, got {res}"
        print(f" [PASS] safe_eval_math('{expr}') == {res}")

    # Security tests
    security_cases = [
        "__import__('os')",
        "open('test.txt')",
        "9 ** 9999",
        "import sys",
        "globals()",
    ]
    for bad_expr in security_cases:
        try:
            safe_eval_math(bad_expr)
            print(f" [FAIL] Security test failed to block: {bad_expr}")
            failed.append(("Security: " + bad_expr, "Was not blocked!"))
        except Exception:
            print(f" [PASS] Security test successfully blocked: {bad_expr}")

    print("=" * 60)
    if failed:
        print(f"TESTS FINISHED WITH {len(failed)} FAILURE(S):")
        for f, err in failed:
            print(f" - {f}: {err}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED SUCCESSFULLY! (10/10 cogs loaded cleanly)")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
