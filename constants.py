###############
# DISCORD BOT #
###############
DEFAULT_BOT_PREFIX = "~"
EMBED_COLOR = 0xD4E4FF


DEFAULT_COMMANDS = []
CUSTOM_COMMANDS = {}

# Command success/fail
SUCCESS = "Success"
FAILED = "Failed"

# File size restriction
BYTES_TO_MEGABYTES = 1_048_576  # 1024 squared

###########
# MODULES #
###########
MODULES_DIR = "modules"


############
# DATABASE #
############

DB_GLOBAL = "global"

############
# REMINDER #
############

# Used for time utils
UTC = "UTC"
DISPLAY_DATETIME_FORMAT = "%a %B %d, %H:%M %Z"
SHEET_DATETIME_FORMAT = "%m/%d/%y %H:%M %Z"


###############
# ROLE BUTTON #
###############

import os
from dotenv.main import load_dotenv

load_dotenv()

# Bot setup
BOT_NAME = "Hogwarts-Ghosts-Bot"

# Discord Role IDs
SUBSCRIBER_ROLE_ID = int(os.getenv("SUBSCRIBER_ROLE_ID", ""))

# Discord Message IDs
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID", ""))
