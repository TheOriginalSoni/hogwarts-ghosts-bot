import nextcord
import constants
from modules import channel_management
from typing import Union

VIEW_NAME = "RoleView"

class RoleViewButton(nextcord.ui.Button):
    def __init__(self, role: nextcord.Role, category: nextcord.Category, sub: str):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='Write Confessional')
        self.role = role
        self.sub = sub
        self.category = category

    async def callback(self, interaction: nextcord.Interaction):
        if role in interaction.user.roles:
            # await interaction.user.remove_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"Your were already in {button.label} role. Nothing to do",
                ephemeral=True,
            )
        # if the member does not have the role, add it
        else:
            await interaction.user.add_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"You have been given the {button.label} role", ephemeral=True
            )
            a = await makechanfor(self.category,interaction.user)
            if(a):
                await interaction.response.send_message(
                f"Your channel is ready at {a.mention}", ephemeral=True
                )

