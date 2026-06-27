import requests
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, API_URL

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        """
👋 Welcome To Free Fire Info Bot

UID এবং Region পাঠান।

Example:

338277714 SG
338277714 IND
338277714 BR
"""
    )


@dp.message(F.text)
async def player_info(message: Message):

    try:
        uid, region = message.text.split()

    except:
        await message.answer(
            "❌ ভুল ফরম্যাট।\n\nExample:\n338277714 SG"
        )
        return

    url = f"{API_URL}?region={region.upper()}&uid={uid}"

    try:
        response = requests.get(url)

        data = response.json()

        info = data.get("basicInfo")

        if not info:
            await message.answer("❌ Player পাওয়া যায়নি")
            return

        text = f"""
👤 Nickname: {info.get('nickname')}

🆔 UID: {info.get('accountId')}

🌍 Region: {info.get('region')}

⭐ Level: {info.get('level')}

❤️ Likes: {info.get('liked')}

🏆 Rank: {info.get('rank')}

🎖 Badge Count: {info.get('badgeCnt')}

🖼 Banner ID: {info.get('bannerId')}

🖼 Avatar ID: {info.get('headPic')}
"""

        await message.answer(text)

    except Exception as e:
        await message.answer(
            f"❌ Error:\n{e}"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
