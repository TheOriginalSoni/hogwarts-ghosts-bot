import nextcord
import constants

VIEW_NAME = "RoleView"

class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def custom_id(view: str, id: int) -> str:
        """create a custom id from the bot name : the view : the identifier"""
        return f"{constants.BOT_NAME}:{view}:{id}"


    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        # get role from the role id
        role = interaction.guild.get_role(int(button.custom_id.split(":")[-1]))
        assert isinstance(role, nextcord.Role)
        # if member has the role, remove it
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"Your were already in {button.label} role. Nothing to do", ephemeral=True
            )
        # if the member does not have the role, add it
        else:
            await interaction.user.add_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"You have been given the {button.label} role", ephemeral=True
            )

    @nextcord.ui.button(
        label="Subscriber",
        emoji="💖",
        style=nextcord.ButtonStyle.primary,
        # set custom id to be the bot name : the class name : the role id
        custom_id=custom_id(VIEW_NAME, constants.SUBSCRIBER_ROLE_ID),
    )
    async def subscriber_button(self, button, interaction):
        await self.handle_click(button, interaction)