import nextcord
import constants
from modules import channel_management
from typing import Union, List

VIEW_NAME = "RoleView"

class RoleViewButton(nextcord.ui.Button):
    def __init__(self, role: nextcord.Role, category: nextcord.CategoryChannel, sub: str):
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

class RoleButton(nextcord.ui.Button):
    def __init__(self, role: nextcord.Role):
        super().__init__(
            label=role.name,
            style=nextcord.ButtonStyle.blurple,
            custom_id=f"RoleView:{role.id}",
        )
        self.role = role

    async def callback(self, interaction: nextcord.Interaction):
        if self.role not in interaction.user.roles:
            await interaction.send(f"You have been given the {self.role.name} role")
            await interaction.user.add_roles(self.role)
        else:
            await interaction.send(f"Your {self.role.name} role has been removed")
            await interaction.user.remove_roles(self.role)


class RoleView(nextcord.ui.View):
    def __init__(self, guild: nextcord.Guild, role_ids: List[int]):
        super().__init__(timeout=None)
        for role_id in role_ids:
            role = guild.get_role(role_id)
            if not role:
                print(f"Role not found: {role_id}")
                continue
            self.add_item(RoleButton(role))


