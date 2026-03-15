import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import asyncio
import aiohttp

# Токен из переменных окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")  # Токен второго бота
ADMIN_ID = int(os.getenv("ADMIN_ID", "6915077397"))

if not BOT_TOKEN or not ADMIN_BOT_TOKEN:
    raise ValueError("Токены не найдены в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


# ========== ТВОИ ОРИГИНАЛЬНЫЕ КНОПКИ ==========
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Д3Ф")],
            [KeyboardButton(text="Д3АН0Н"), KeyboardButton(text="СВ1ТТИНГ")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_payment_keyboard(service_type: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплата по Крипте", callback_data=f"crypto_{service_type}")],
            [InlineKeyboardButton(text="Оплата по DonationAlerts", callback_data=f"donate_{service_type}")],
        ]
    )
    return keyboard


def get_donate_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить", url="https://www.donationalerts.com/r/iouhh_def")]
        ]
    )
    return keyboard


def get_def_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Бесплатный дефф", callback_data="info_more2")],
            [InlineKeyboardButton(text="Платный дефф", callback_data="info_more3")]
        ]
    )
    return keyboard


def get_dox_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Обычный деанон", callback_data="dox_normal")],
            [InlineKeyboardButton(text="Подробный + цепочка", callback_data="dox_detailed")]
        ]
    )
    return keyboard


# ========== НОВЫЕ КНОПКИ ==========
def get_proof_keyboard(service):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data=f"send_proof_{service}")]
        ]
    )
    return keyboard


# ========== ФУНКЦИИ УДАЛЕНИЯ ==========
async def delete_previous_message(message: Message):
    try:
        await message.delete()
    except:
        pass


async def delete_callback_message(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass


# ========== ССЫЛКИ НА ФОТО ==========
PHOTO_URLS = {
    "crypto_def": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_dox": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_dox_detailed": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_swat": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_def": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_dox": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_dox_detailed": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_swat": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "info_more2": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "info_more3": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "def_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "dox_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "dox_normal_main": "https://postimg.cc/v1pnfyqs",
    "dox_detailed_main": "https://postimg.cc/Wtp2vBYC",
    "swat_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg"
}

# ========== Цены и названия услуг ==========
SERVICES = {
    "def": {"name": "Платный Д3Ф", "price": "10$"},
    "dox": {"name": "Обычный деанон", "price": "3$"},
    "dox_detailed": {"name": "Подробный деанон + цепочка", "price": "5$"},
    "swat": {"name": "СВ1ТТИНГ", "price": "20$"}
}


# ========== ФУНКЦИЯ ОТПРАВКИ В АДМИН-БОТА ==========
async def send_to_admin_bot(user_id, username, text, photo_url=None):
    async with aiohttp.ClientSession() as session:
        if photo_url:
            # Отправляем фото
            await session.post(
                f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendPhoto",
                json={
                    "chat_id": ADMIN_ID,
                    "photo": photo_url,
                    "caption": f"🆕 **НОВОЕ ПОДТВЕРЖДЕНИЕ**\n\n👤 Пользователь: @{username} (ID: {user_id})\n📝 {text}",
                    "parse_mode": "Markdown",
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": "✅ ПОДТВЕРДИТЬ", "callback_data": f"approve_{user_id}"}],
                            [{"text": "❌ ОТКЛОНИТЬ", "callback_data": f"reject_{user_id}"}]
                        ]
                    }
                }
            )
        else:
            # Отправляем текст
            await session.post(
                f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": ADMIN_ID,
                    "text": f"🆕 **НОВОЕ ПОДТВЕРЖДЕНИЕ**\n\n👤 Пользователь: @{username} (ID: {user_id})\n📝 {text}",
                    "parse_mode": "Markdown",
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": "✅ ПОДТВЕРДИТЬ", "callback_data": f"approve_{user_id}"}],
                            [{"text": "❌ ОТКЛОНИТЬ", "callback_data": f"reject_{user_id}"}]
                        ]
                    }
                }
            )


# ========== СТАРТ ==========
@router.message(Command("start"))
async def start(message: Message):
    await delete_previous_message(message)
    await message.answer(
        "Привет! *Это бот с услугами от @Iouhh_def*\n\nВыбери то что тебе нужно",
        parse_mode="Markdown",
        reply_markup=get_main_reply_keyboard()
    )


# ========== ВСЯ ТВОЯ ЛОГИКА СЮДА ==========
# [ВСТАВЬ СЮДА ВСЕ ТВОИ ОБРАБОТЧИКИ ИЗ ТВОЕГО КОДА]
# def_handler, dox_handler, swat_handler, crypto_*, donate_* и т.д.

# ========== КРИПТА ==========
@router.callback_query(lambda c: c.data == "crypto_def")
async def crypto_payment_def(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["crypto_def"],
        caption="[root@localhost]# КРИПТА · DEF\n"
                "──────────────────────────────\n"
                "USDT TRC20:\n"
                "TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n"
                "──────────────────────────────\n"
                "💵 СУММА: 10 USDT\n"
                "⏳ ДОСТУП: НАВСЕГДА\n"
                "──────────────────────────────\n"
                "✅ ПОСЛЕ ОПЛАТЫ НАЖМИ КНОПКУ НИЖЕ",
        reply_markup=get_proof_keyboard("def")
    )
    await callback.answer()


# [ДОБАВЬ ВСЕ ОСТАЛЬНЫЕ CRYPTO И DONATE ОБРАБОТЧИКИ]

# ========== ОБРАБОТЧИК ПОДТВЕРЖДЕНИЯ ==========
@router.callback_query(lambda c: c.data.startswith("send_proof_"))
async def send_proof(callback: CallbackQuery):
    service = callback.data.replace("send_proof_", "")
    await delete_callback_message(callback)

    await callback.message.answer(
        f"📸 **ОТПРАВЬ ПОДТВЕРЖДЕНИЕ ОПЛАТЫ**\n\n"
        f"Услуга: {SERVICES[service]['name']}\n"
        f"Сумма: {SERVICES[service]['price']}\n\n"
        f"📤 Отправь скриншот оплаты или хеш транзакции одним сообщением.",
        parse_mode="Markdown"
    )
    await callback.answer()


# ========== ПОЛУЧЕНИЕ ПОДТВЕРЖДЕНИЯ ==========
@router.message(F.photo | F.text)
async def handle_proof(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"

    # Игнорируем сообщения от админа
    if user_id == ADMIN_ID:
        return

    if message.photo:
        # Получаем URL фото
        file = await bot.get_file(message.photo[-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        await send_to_admin_bot(
            user_id=user_id,
            username=username,
            text=message.caption or "Без описания",
            photo_url=file_url
        )
    else:
        await send_to_admin_bot(
            user_id=user_id,
            username=username,
            text=message.text
        )

    await message.reply("✅ Подтверждение отправлено админу. Жди ответа!")


# ========== НЕ КОМАНДА ==========
@router.message()
async def mess(message: Message):
    if message.from_user.id == ADMIN_ID:
        return
    await delete_previous_message(message)
    await message.answer("ты шо бальной?")


# ========== ЗАПУСК ==========
async def main():
    dp.include_router(router)
    print(f"🚀 Основной бот запущен! Админ ID: {ADMIN_ID}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())