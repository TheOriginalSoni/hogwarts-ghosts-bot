import nextcord
import constants
from typing import Union
from nextcord.ext import commands
from .role_view import RoleView
from .tictactoe import TicTacToe
from utils import discord_utils, logging_utils, command_predicates


class ButtonViewCog(commands.Cog, name="Button Roles"):
    """Give and remove roles based on button presses"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def tic(self, ctx: commands.Context):
        """Starts a tic-tac-toe game with yourself."""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

    @commands.command()
    @command_predicates.is_owner_or_admin()
    async def roleview(self, ctx: commands.Context, rolename: Union[nextcord.Role, str], *args: str):
        """Adds roleview to a message made by the bot. If no such message exists, makes a new message for it.

        See also `~botsay` and `~botsayembed`.

        Usage: `~roleview @Rolename "Full Message"`
        Usage: `~roleview "RoleName"` (as reply to message written by bot)
        """
        logging_utils.log_command("roleview", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        role_to_view = None
        if isinstance(rolename, str):
            roles = await ctx.guild.fetch_roles()
            for role in roles:
                if role.name.lower() == rolename.lower():
                    role_to_view = role
                    break
        else:
            role_to_view = rolename

        if not role_to_view:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"I can't find `{rolename}` in this server. Make sure you check the spelling and punctuation!",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        """Starts a role view"""
        arg = "".join(args)
        if(len(arg)==0):
            msg = f'If you want to write confessionals for the HWW Game, click "Create a ticket" below. This will make a private confessional channel for you where spectators and dead players can read your thoughts!'
        else:
            msg = arg

        if not ctx.message.reference:
            embed.add_field(
                name=f"Confessional Bot",
                value=f"{msg}",
                inline=False,
            )
            message_reference = await ctx.send(embed=embed)
        else:
            message_reference = ctx.message.reference

        if message_reference.author != self.bot.user:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"I cannot edit any message written by another user.",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        try:
            #await message_reference.edit(view=RoleView(role_to_view))
            pass
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
            value=f"Done! Added roleview to the message for {role}.",
            inline=False,
        )
        await ctx.send(embed=embed)

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

        if message.author != self.bot.user:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"I cannot edit any message written by another user.",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

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
    bot.add_cog(ButtonViewCog(bot))
