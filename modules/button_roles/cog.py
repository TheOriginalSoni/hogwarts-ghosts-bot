from nextcord.ext import commands
from .role_view import RoleView


class ButtonRolesCog(commands.Cog, name="Button Roles"):
    """Give and remove roles based on button presses"""

    def __init__(self, bot: commands.Bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready, load the role view"""
        self.__bot.add_view(RoleView())
        print("Button view added")

    @commands.command()
    @commands.is_owner()
    async def roles(self, ctx: commands.Context, game: str= "the current HWW Game"):
        """Starts a role view"""
        msg = f"If you want to write confessionals for {game}, click \"Create a ticket\" below. This will make a private confessional channel for you where spectators and dead players can read your thoughts!"
        await ctx.send(msg, view=RoleView())


# setup functions for bot
def setup(bot):
    bot.add_cog(ButtonRolesCog(bot))