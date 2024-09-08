import asyncio

from vkbottle import Bot

from fe.vk.config import api, state_dispenser
from fe.vk.handlers import labelers


async def main() -> None:
    bot = Bot(api=api, state_dispenser=state_dispenser)
    for labeler in labelers:
        bot.labeler.load(labeler)
    await bot.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
