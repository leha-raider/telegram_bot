import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import othe_handlers, user_handlers
from keyboards.main_menu import set_main_menu

#инцилизоровать логер
logger = logging.getLogger(__name__)

#функция запуска бота
async def main():
    #конфиг логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
#вывод в консоль фниформацию о начале запуска бота
logger.info('Starting bot')
#загружаем конфиг в переменную config
config: Config = load_config()

#иницилизируем в бот в диспетчер
bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

#настроиваем главное меню бота
await set_main_menu(Bot)

#регистрируем роутеры в диспетчере
dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)

#пропускаем накопившиеся апдейты и запускаем polling
await bot.delete_webhook(drop_pending_updates=True)
await dp.start_polling(bot)

