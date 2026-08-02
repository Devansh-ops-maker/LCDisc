import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from registerUser import register,unregister
from recommender import recommend
from match import createMatch,registerMatch,startMatch
from help_commands import adminCommands,flow,bothelp
from duels import duels
from AddTeams import createTeam,addMember,removeMember

load_dotenv()

token=os.getenv("BOT_TOKEN")    

intents=discord.Intents.default()
intents.message_content=True

bot=commands.Bot(command_prefix='!',intents=intents)

bot.add_command(commands.Command(register))
bot.add_command(commands.Command(unregister))
bot.add_command(commands.Command(recommend))
bot.add_command(commands.Command(createMatch))
bot.add_command(commands.Command(registerMatch))
bot.add_command(commands.Command(startMatch))
bot.add_command(commands.Command(adminCommands))
bot.add_command(commands.Command(flow))
bot.add_command(commands.Command(bothelp))
bot.add_command(commands.Command(duels))
bot.add_command(commands.Command(createTeam))
bot.add_command(commands.Command(addMember))
bot.add_command(commands.Command(removeMember))
bot.run(token)


