import os

from vkbottle import API, BuiltinStateDispenser

TOKEN = os.getenv("VK_TOKEN")
if not TOKEN:
    raise ValueError("`VK_TOKEN` environment must be set!")

api = API(token=TOKEN)
state_dispenser = BuiltinStateDispenser()
