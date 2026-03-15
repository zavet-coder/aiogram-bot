import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
import asyncio
import aiohttp

# Токены из переменных окружения
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
MAIN_BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6915077397"))

if not ADMIN_BOT_TOKEN or not MAIN_BOT_TOKEN:
    raise ValueError("Токены не найдены!")

bot = Bot(token=ADMIN_BOT_TOKEN)
dp = Dispatcher()
router = Router()


# Функция отправки пользователю через основного бота
async def send_to_user(user_id, text):
    async with aiohttp.ClientSession() as session:
        await session.post(
            f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": user_id,
                "text": text,
                "parse_mode": "Markdown"
            }
        )


# Проверка на админа
def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# Подтверждение оплаты
@router.callback_query(lambda c: c.data.startswith("approve_"))
async def approve_payment(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен")
        return

    user_id = int(callback.data.replace("approve_", ""))

    await send_to_user(user_id, "✅ **ОПЛАТА ПОДТВЕРЖДЕНА!**\n\n📞 Свяжись с админом: @Iouhh_def")

    await callback.message.edit_text(
        text=f"{callback.message.text}\n\n✅ ПОДТВЕРЖДЕНО",
        reply_markup=None
    )
    await callback.answer("✅ Подтверждено!")


# Отклонение оплаты
@router.callback_query(lambda c: c.data.startswith("reject_"))
async def reject_payment(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен")
        return

    user_id = int(callback.data.replace("reject_", ""))

    await send_to_user(user_id, "❌ **ОПЛАТА НЕ ПОДТВЕРЖДЕНА**\n\nПопробуй еще раз или напиши @Iouhh_def")

    await callback.message.edit_text(
        text=f"{callback.message.text}\n\n❌ ОТКЛОНЕНО",
        reply_markup=None
    )
    await callback.answer("❌ Отклонено!")


@router.message()
async def any_message(message: Message):
    if is_admin(message.from_user.id):
        await message.answer("👋 Админ-бот работает. Жду подтверждений.")
    else:
        await message.answer("⛔ Доступ запрещен")


async def main():
    dp.include_router(router)
    print(f"🚀 Админ-бот запущен! Админ ID: {ADMIN_ID}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())