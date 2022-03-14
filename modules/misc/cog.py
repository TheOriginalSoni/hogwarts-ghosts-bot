import nextcord
import os
from nextcord.ext import commands
from emoji import UNICODE_EMOJI
from typing import Union
import constants
from utils import discord_utils, logging_utils, command_predicates
import random

class MiscCog(commands.Cog, name="Misc"):
    """A collection of Misc useful/fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="emoji")
    async def emoji(
        self, ctx, emojiname: Union[nextcord.Emoji, str], to_delete: str = ""
    ):
        """Finds the custom emoji mentioned and uses it.
        This command works for normal as well as animated emojis, as long as the bot is in one server with that emoji.

        If you say delete after the emoji name, it deletes original message

        If this command is a reply to another message, it'll instead be a react to that message.

        Usage : `~emoji snoo_glow delete`
        Usage : `~emoji :snoo_grin:`
        """
        logging_utils.log_command("emoji", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        try:
            if to_delete.lower()[0:3] == "del":
                await ctx.message.delete()
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Unable to delete original message. Do I have `manage_messages` permissions?",
            )
            await ctx.send(embed=embed)
            return

        emoji = None
        hasurl = False

        # custom emoji
        if isinstance(emojiname, nextcord.Emoji):
            emoji = emojiname
            hasurl = True
        # default emoji
        elif isinstance(emojiname, str) and emojiname in UNICODE_EMOJI:
            emoji = emojiname
            hasurl = False
        elif emojiname[0] == ":" and emojiname[-1] == ":":
            emojiname = emojiname[1:-1]
            for guild in self.bot.guilds:
                emoji = nextcord.utils.get(guild.emojis, name=emojiname)
                if emoji is not None:
                    break
                hasurl = True

        if emoji is None:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Emoji named {emojiname} not found",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        if ctx.message.reference:
            # If it's replying to a message
            orig_msg = ctx.message.reference.resolved
            await orig_msg.add_reaction(emoji)
            return
        else:
            # Just a normal command
            if hasurl:
                await ctx.send(emoji.url)
            else:
                await ctx.send(emoji)
            return

    ###################
    # BOTSAY COMMANDS #
    ###################

    @command_predicates.is_trusted()
    @commands.command(name="botsay")
    async def botsay(self, ctx, channel_id_or_name: str, *args):
        """Say something in another channel

        Permission Category : Trusted roles only.
        Usage: `~botsay channelname Message`
        Usage: `~botsay #channelmention Longer Message`
        """
        logging_utils.log_command("botsay", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if len(args) < 1:
            embed = discord_utils.create_no_argument_embed("Message")
            await ctx.send(embed=embed)
            return

        message = " ".join(args)
        guild = ctx.message.guild

        try:
            channel = await commands.TextChannelConverter().convert(
                ctx, channel_id_or_name
            )
        except ValueError:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Error! The channel `{channel_id_or_name}` was not found",
            )
            await ctx.send(embed=embed)
            return

        try:
            await channel.send(message)
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Forbidden! The bot is unable to speak on {channel.mention}! Have you checked if "
                f"the bot has the required permisisons?",
            )
            await ctx.send(embed=embed)
            return

        embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"Message sent to {channel.mention}: {message}!",
        )
        # reply to user
        await ctx.send(embed=embed)

    @command_predicates.is_trusted()
    @commands.command(name="botsayembed")
    async def botsayembed(self, ctx, channel_id_or_name: str, *args):
        """Say something in another channel, but as an embed

        Permission Category : Trusted roles only.
        Usage: `~botsayembed channelname Message`
        Usage: `~botsayembed #channelmention Longer Message`
        """
        logging_utils.log_command("botsayembed", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if len(args) < 1:
            embed = discord_utils.create_no_argument_embed("Message")
            await ctx.send(embed=embed)
            return

        message = " ".join(args)

        try:
            channel = await commands.TextChannelConverter().convert(
                ctx, channel_id_or_name
            )
        except ValueError:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Error! The channel `{channel_id_or_name}` was not found",
            )
            await ctx.send(embed=embed)
            return

        try:
            sent_embed = discord_utils.create_embed()
            sent_embed.description = message
            await channel.send(embed=sent_embed)
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Forbidden! The bot is unable to speak on {channel.mention}! Have you checked if "
                f"the bot has the required permisisons?",
            )
            await ctx.send(embed=embed)
            return

        # reply to user
        sent_embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"Embed sent to {channel.mention}",
            inline=False,
        )
        await ctx.send(embed=sent_embed)

    @commands.command(name="choose")
    async def choose(self, ctx, *args : str):
        """Choose one of N things

        Usage : `~choose "Eat potato" "Dont eat potato"`
        """
        logging_utils.log_command("choose", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if(len(args)<1):
            embed = discord_utils.create_no_argument_embed("Option")
            await ctx.send(embed=embed)
            return
        message = f"The options are `{str(args)}`\n I choose **{random.choice(args)}**" 

        embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=message,
            inline=False,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MiscCog(bot))
