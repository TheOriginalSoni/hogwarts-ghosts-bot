import nextcord
import constants
from modules import channel_management
from typing import Union

VIEW_NAME = "RoleView"

class RoleView(nextcord.ui.View):

    role2 = None
    def __init__(self, role: nextcord.Role, sub: str = "Confessional"):
        super().__init__(timeout=None)
        self.role2 = role