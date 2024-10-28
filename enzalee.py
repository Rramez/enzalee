import discord
import os
import asyncio
from discord.ext import commands

# files
import time
import reg

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REGISTRATION_FILE = os.getenv("REGISTRATION_FILE")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="reg", help="Register Codeforces Account.")
async def cfUserReg(ctx, handle):

    discordUserInfo = ctx.author
    discordUserName = discordUserInfo.name
    discordUserMention = discordUserInfo.mention

    if not reg.validHandle(handle):
        await ctx.send(f"{discordUserMention} Wrong username, How About you give me the real one.")
        return

    if reg.usedDiscord(discordUserName):
        await ctx.send(f"{discordUserMention} You Are Already Registerd, Stop Horsing Around.")
        return
    
    if reg.usedHandle(handle):
        await ctx.send(f"{discordUserMention} This CF Account is already being used by someone else.")
        return

    
    # if the user is trying to spam !reg handle, and the user submits successfully, the reg.txt file will add the user as many times as he spams, so the below if statement is meant to not allow that
    if reg.userSpamming(discordUserName):
        await ctx.send(f"{discordUserMention} You Are Already Trying To Register, Calm Down.")
        return
    else:
        reg.putInProcess(discordUserName)


    timer = 30
    await ctx.send(f"{discordUserMention} Make a Submission with \"Compilation Error\" Verdict. You Have **{timer}** Seconds To Do it, Go Go Goooo.")

    currentTime = int(time.time())
    await asyncio.sleep(timer) # Wait for the user to submit 


    submissionTime = reg.getSumbissionTime(handle)
    submissionVerdict = reg.getSubmissionVerdict(handle)


    # default message
    message = f"{discordUserMention} Registered Successfully. Now You Can Tenzilo."

    if submissionTime==None or submissionTime<currentTime or submissionVerdict!="COMPILATION_ERROR":
        message = f"{discordUserMention} That Didn't Work, Try Again."
    else:
        # bind discord username to this handle
        reg.bind(discordUserName,handle)


    # now the user got his result, we need to remove him from the regPorcess, if not he will not be able to try to register again.
    reg.removeFromProcess(discordUserName)

    await ctx.send(message)



@bot.command(name="unreg", help="Register Codeforces Account.")
async def cfUnregister(ctx):

    discordUserInfo = ctx.author
    discordUserName = discordUserInfo.name
    discordUserMention = discordUserInfo.mention

    reg.deleteHandle(discordUserName)

    await ctx.send(f"{discordUserMention} Done. You Are Now Not Registered To Any Codeforces Account.")


bot.run(DISCORD_TOKEN)