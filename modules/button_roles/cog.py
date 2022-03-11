import nextcord
import constants
from nextcord.ext import commands
from .role_view import RoleView
from utils import discord_utils, logging_utils, command_predicates


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
    @command_predicates.is_owner_or_admin()
    async def roleview(self, ctx: commands.Context, game: str= "the current HWW Game"):
        """Adds roleview to a message. If no such message exists, makes a new message for it.

        Usage: `~roleview`
        Usage: `~roleview` (as reply to message)
        """
        logging_utils.log_command("roleview", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        """Starts a role view"""
        msg = f"If you want to write confessionals for {game}, click \"Create a ticket\" below. This will make a private confessional channel for you where spectators and dead players can read your thoughts!"
        embed.add_field(
            name=f"{constants.SUCCESS}",
            value=f"{msg}",
            inline=False,
        )
        await ctx.send(embed=embed, view=RoleView("HWWBot1"))

    @commands.command()
    @command_predicates.is_owner_or_admin()
    async def removeview(self, ctx: commands.Context):
        """Removes roleview from a message. The command must be a reply to that message.
        Also see `~roleview`

        Usage: `~removeview` (as reply to message)
        """
        logging_utils.log_command("removeview", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if not ctx.message.reference:
            embed.add_field(
                name=f"{constants.FAILED}",
                value=f"You need to reply to a message to remove the button view.",
                inline=False,
            )
            await ctx.send(embed=embed)
            return
        else:
            message = await ctx.fetch_message(ctx.message.reference.message_id)

        try:
            await message.edit(view=None)
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"I couldn't edit the message. Do I have the permission to edit on this server?",
                inline=False,
            )
            await ctx.send(embed=embed)
            return
            
        embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"Done! Removed roleview from the message.",
            inline=False,
        )
        await ctx.send(embed=embed)

# setup functions for bot
def setup(bot):
    bot.add_cog(ButtonRolesCog(bot))