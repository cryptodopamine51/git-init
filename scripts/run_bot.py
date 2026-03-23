import asyncio

from app.bot.dispatcher import run_polling


if __name__ == "__main__":
    asyncio.run(run_polling())
