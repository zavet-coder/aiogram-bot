from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
from datetime import datetime

router = Router()

# ========== БАЗА ДАННЫХ ==========
conn = sqlite3.connect('tickets.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    service TEXT,
    amount TEXT,
    proof TEXT,
    status TEXT DEFAULT 'waiting',
    created_at TEXT
)
''')
conn.commit()

# ТВОЙ TELEGRAM ID (ВСТАВЬ СВОЙ)
ADMIN_ID = 6915077397  # 👈 ЗАМЕНИ НА СВОЙ ID


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


# ========== НОВЫЕ КНОПКИ ДЛЯ ТИКЕТОВ ==========
def get_proof_keyboard(service):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data=f"send_proof_{service}")]
        ]
    )
    return keyboard


def get_ticket_keyboard(ticket_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 НАПИСАТЬ АДМИНУ", callback_data=f"ticket_msg_{ticket_id}")],
            [InlineKeyboardButton(text="❌ ЗАКРЫТЬ ТИКЕТ", callback_data=f"ticket_close_{ticket_id}")]
        ]
    )
    return keyboard


def get_admin_actions_keyboard(ticket_id, user_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ ПОДТВЕРДИТЬ", callback_data=f"admin_approve_{ticket_id}_{user_id}")],
            [InlineKeyboardButton(text="❌ ОТКЛОНИТЬ", callback_data=f"admin_reject_{ticket_id}_{user_id}")],
            [InlineKeyboardButton(text="💬 ОТВЕТИТЬ", callback_data=f"admin_reply_{ticket_id}_{user_id}")]
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


# ========== СТАРТ ==========
@router.message(Command("start"))
async def start(message: Message):
    await delete_previous_message(message)
    await message.answer(
        "Привет! *Это бот с услугами от @Iouhh_def*\n\nВыбери то что тебе нужно",
        parse_mode="Markdown",
        reply_markup=get_main_reply_keyboard()
    )


# ========== Д3Ф ==========
@router.message(Command("def"))
@router.message(F.text.lower() == "д3ф")
async def def_handler(message: Message):
    await delete_previous_message(message)
    await message.answer_photo(
        photo=PHOTO_URLS["def_main"],
        caption="██████╗ ███████╗███████╗\n"
                "██╔══██╗██╔════╝██╔════╝\n"
                "██║  ██║█████╗  █████╗  \n"
                "██║  ██║██╔══╝  ██╔══╝  \n"
                "██████╔╝██║     ██║     \n"
                "╚═════╝ ╚═╝     ╚═╝     \n\n"
                "──────────────────────────────\n"
                "ВЫБЕРИ ВАРИАНТ\n"
                "──────────────────────────────",
        reply_markup=get_def_keyboard()
    )


@router.callback_query(lambda c: c.data == "info_more2")
async def def_free(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["info_more2"],
        caption="[root@localhost]# БЕСПЛАТНЫЙ Д3Ф\n"
                "──────────────────────────────\n"
                "▸ ЗАЩИТА ОТ Д3АН0НА/УГР03\n"
                "▸ ПОЛНЫЙ Д0КС НА Ж3РТВУ\n"
                "▸ Д0Н0С НА Ж3РТВУ\n"
                "──────────────────────────────\n"
                "⚠️ ТОЛЬКО 1 РАЗ\n"
                "──────────────────────────────\n"
                "✉️Получить --> @Iouhh_def"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "info_more3")
async def def_paid(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["info_more3"],
        caption="[root@localhost]# ПЛАТНЫЙ Д3Ф\n"
                "──────────────────────────────\n"
                "▸ ЗАЩИТА ОТ Д3АН0НА/УГР03\n"
                "▸ ПОЛНЫЙ Д0КС НА Ж3РТВУ\n"
                "▸ Д0Н0С НА Ж3РТВУ\n"
                "──────────────────────────────\n"
                "💰 СУММА: 10$\n"
                "⏳ ДОСТУП: НАВСЕГДА\n"
                "──────────────────────────────",
        reply_markup=get_payment_keyboard("def")
    )
    await callback.answer()


# ========== Д3АН0Н ==========
@router.message(Command("dox"))
@router.message(F.text.lower() == "д3ан0н")
async def dox_handler(message: Message):
    await delete_previous_message(message)
    await message.answer_photo(
        photo=PHOTO_URLS["dox_main"],
        caption="██████╗  ██████╗ ██╗  ██╗\n"
                "██╔══██╗██╔═══██╗╚██╗██╔╝\n"
                "██║  ██║██║   ██║ ╚███╔╝ \n"
                "██║  ██║██║   ██║ ██╔██╗ \n"
                "██████╔╝╚██████╔╝██╔╝ ██╗\n"
                "╚═════╝  ╚═════╝ ╚═╝  ╚═╝\n\n"
                "[root@localhost]# ПОИСК ИНФОРМАЦИИ О Ж3РТВЕ\n"
                "──────────────────────────────\n"
                "ВЫБЕРИ ТИП ДЕАНОНА\n"
                "──────────────────────────────",
        reply_markup=get_dox_keyboard()
    )


@router.callback_query(lambda c: c.data == "dox_normal")
async def dox_normal(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["dox_normal_main"],
        caption="[root@localhost]# ОБЫЧНЫЙ ДЕАНОН\n"
                "──────────────────────────────\n"
                "▸ БАЗОВАЯ ИНФОРМАЦИЯ\n"
                "▸ АККАУНТЫ В СОЦСЕТЯХ\n"
                "▸ НОМЕР ТЕЛЕФОНА\n"
                "▸ АДРЕС\n"
                "▸ ТАКАЯ ЖЕ ИНФА О МАМЕ И ПАПЕ\n"
                "▸ ИНОГДА ДАЖЕ ПАРОЛИ\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 3$\n"
                "──────────────────────────────",
        reply_markup=get_payment_keyboard("dox")
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "dox_detailed")
async def dox_detailed(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["dox_detailed_main"],
        caption="[root@localhost]# ПОДРОБНЫЙ ДЕАНОН + ЦЕПОЧКА\n"
                "──────────────────────────────\n"
                "▸ ВСЯ ИНФОРМАЦИЯ ИЗ ОБЫЧНОГО\n"
                "▸ ПОЛНАЯ ЦЕПОЧКА СВЯЗЕЙ\n"
                "▸ КТО ЕЩЕ СВЯЗАН С Ж3РТВОЙ(вплоть до соседей/друзей/дальних родственников\n"
                "▸ ДОПЛАТИВ ЕЩЕ 5$ СДЕЛАЮ Д0Н0С ВСЕМ РОДСТВЕННИКАМ И БЛИЗКИМ\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 5$\n"
                "──────────────────────────────",
        reply_markup=get_payment_keyboard("dox_detailed")
    )
    await callback.answer()


# ========== СВ1ТТИНГ ==========
@router.message(Command("swat"))
@router.message(F.text.lower() == "св1ттинг")
async def swat_handler(message: Message):
    await delete_previous_message(message)
    await message.answer_photo(
        photo=PHOTO_URLS["swat_main"],
        caption="███████╗██╗    ██╗ █████╗ ████████╗\n"
                "██╔════╝██║    ██║██╔══██╗╚══██╔══╝\n"
                "███████╗██║ █╗ ██║███████║   ██║   \n"
                "╚════██║██║███╗██║██╔══██║   ██║   \n"
                "███████║╚███╔███╔╝██║  ██║   ██║   \n"
                "╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   \n\n"
                "[root@localhost]# ЛОЖНОЕ МИНИРОВАНИЕ\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 20$\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_payment_keyboard("swat")
    )


# ========== НОВЫЙ КОД: СИСТЕМА ПОДТВЕРЖДЕНИЯ ОПЛАТЫ ==========

# Цены и названия услуг
SERVICES = {
    "def": {"name": "Платный Д3Ф", "price": "10$"},
    "dox": {"name": "Обычный деанон", "price": "3$"},
    "dox_detailed": {"name": "Подробный деанон + цепочка", "price": "5$"},
    "swat": {"name": "СВ1ТТИНГ", "price": "20$"}
}


# КРИПТА
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


@router.callback_query(lambda c: c.data == "crypto_dox")
async def crypto_payment_dox(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["crypto_dox"],
        caption="[root@localhost]# КРИПТА · DOX\n"
                "──────────────────────────────\n"
                "USDT TRC20:\n"
                "TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n"
                "──────────────────────────────\n"
                "💵 СУММА: 3 USDT\n"
                "──────────────────────────────\n"
                "✅ ПОСЛЕ ОПЛАТЫ НАЖМИ КНОПКУ НИЖЕ",
        reply_markup=get_proof_keyboard("dox")
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "crypto_dox_detailed")
async def crypto_payment_dox_detailed(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["crypto_dox_detailed"],
        caption="[root@localhost]# КРИПТА · ПОДРОБНЫЙ DOX\n"
                "──────────────────────────────\n"
                "USDT TRC20:\n"
                "TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n"
                "──────────────────────────────\n"
                "💵 СУММА: 5 USDT\n"
                "📋 ВКЛЮЧАЕТ ЦЕПОЧКУ\n"
                "──────────────────────────────\n"
                "✅ ПОСЛЕ ОПЛАТЫ НАЖМИ КНОПКУ НИЖЕ",
        reply_markup=get_proof_keyboard("dox_detailed")
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "crypto_swat")
async def crypto_payment_swat(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["crypto_swat"],
        caption="[root@localhost]# КРИПТА · SWAT\n"
                "──────────────────────────────\n"
                "USDT TRC20:\n"
                "TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n"
                "──────────────────────────────\n"
                "💵 СУММА: 20 USDT\n"
                "──────────────────────────────\n"
                "✅ ПОСЛЕ ОПЛАТЫ НАЖМИ КНОПКУ НИЖЕ",
        reply_markup=get_proof_keyboard("swat")
    )
    await callback.answer()


# DONATIONALERTS
@router.callback_query(lambda c: c.data == "donate_def")
async def donate_payment_def(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_def"],
        caption="[root@localhost]# DONATION · DEF\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 10$ / 1000р\n"
                "──────────────────────────────\n"
                "1 В комментарии напиши свой юзернейм\n"
                "2 Нажми 'ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ'\n"
                "──────────────────────────────",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url="https://www.donationalerts.com/r/iouhh_def")],
                [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data="send_proof_def")]
            ]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "donate_dox")
async def donate_payment_dox(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_dox"],
        caption="[root@localhost]# DONATION · DOX\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 3$ / 300р\n"
                "──────────────────────────────\n"
                "1 В комментарии напиши свой юзернейм\n"
                "2 Нажми 'ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ'\n"
                "──────────────────────────────",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url="https://www.donationalerts.com/r/iouhh_def")],
                [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data="send_proof_dox")]
            ]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "donate_dox_detailed")
async def donate_payment_dox_detailed(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_dox_detailed"],
        caption="[root@localhost]# DONATION · ПОДРОБНЫЙ DOX\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 5$ / 500р\n"
                "📋 ВКЛЮЧАЕТ ЦЕПОЧКУ\n"
                "──────────────────────────────\n"
                "1 В комментарии напиши свой юзернейм\n"
                "2 Нажми 'ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ'\n"
                "──────────────────────────────",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url="https://www.donationalerts.com/r/iouhh_def")],
                [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data="send_proof_dox_detailed")]
            ]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "donate_swat")
async def donate_payment_swat(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_swat"],
        caption="[root@localhost]# DONATION · SWAT\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 20$ / 2000р\n"
                "──────────────────────────────\n"
                "1 В комментарии напиши свой юзернейм\n"
                "2 Нажми 'ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ'\n"
                "──────────────────────────────",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url="https://www.donationalerts.com/r/iouhh_def")],
                [InlineKeyboardButton(text="📸 ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ", callback_data="send_proof_swat")]
            ]
        )
    )
    await callback.answer()


# Обработчик кнопки "ОТПРАВИТЬ ПОДТВЕРЖДЕНИЕ"
@router.callback_query(lambda c: c.data.startswith("send_proof_"))
async def send_proof(callback: CallbackQuery):
    service = callback.data.replace("send_proof_", "")

    await delete_callback_message(callback)

    await callback.message.answer(
        f"📸 **ОТПРАВЬ ПОДТВЕРЖДЕНИЕ ОПЛАТЫ**\n\n"
        f"Услуга: {SERVICES[service]['name']}\n"
        f"Сумма: {SERVICES[service]['price']}\n\n"
        f"📤 Отправь скриншот оплаты или хеш транзакции одним сообщением.\n\n"
        f"Админ проверит и создаст тикет.",
        parse_mode="Markdown"
    )
    await callback.answer()


# Получение подтверждения от пользователя
@router.message(F.photo | F.text)
async def handle_proof(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"

    cursor.execute('''
    INSERT INTO tickets (user_id, username, service, amount, proof, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, username, "unknown", "unknown", "waiting_for_service", "waiting",
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    ticket_id = cursor.lastrowid

    if message.photo:
        file_id = message.photo[-1].file_id
        await message.bot.send_photo(
            ADMIN_ID,
            photo=file_id,
            caption=f"🆕 **НОВОЕ ПОДТВЕРЖДЕНИЕ #{ticket_id}**\n\n"
                    f"👤 Пользователь: @{username} (ID: {user_id})\n"
                    f"📝 Сообщение: {message.caption or 'Без описания'}\n\n"
                    f"⬇️ Выбери действие:",
            reply_markup=get_admin_actions_keyboard(ticket_id, user_id),
            parse_mode="Markdown"
        )
    else:
        await message.bot.send_message(
            ADMIN_ID,
            f"🆕 **НОВОЕ ПОДТВЕРЖДЕНИЕ #{ticket_id}**\n\n"
            f"👤 Пользователь: @{username} (ID: {user_id})\n"
            f"📝 Текст: {message.text}\n\n"
            f"⬇️ Выбери действие:",
            reply_markup=get_admin_actions_keyboard(ticket_id, user_id),
            parse_mode="Markdown"
        )

    await message.reply("✅ Подтверждение отправлено админу. Жди ответа!")


# Админ подтверждает оплату
@router.callback_query(lambda c: c.data.startswith("admin_approve_"))
async def admin_approve(callback: CallbackQuery):
    data = callback.data.replace("admin_approve_", "").split("_")
    ticket_id = int(data[0])
    user_id = int(data[1])

    cursor.execute('''
    UPDATE tickets SET status = 'approved' WHERE ticket_id = ?
    ''', (ticket_id,))
    conn.commit()

    await callback.bot.send_message(
        user_id,
        f"✅ **ОПЛАТА ПОДТВЕРЖДЕНА!**\n\n"
        f"🎫 Тикет #{ticket_id} создан.\n"
        f"Админ скоро свяжется с тобой.",
        reply_markup=get_ticket_keyboard(ticket_id),
        parse_mode="Markdown"
    )

    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n✅ ПОДТВЕРЖДЕНО",
        reply_markup=None
    )
    await callback.answer("✅ Подтверждено!")


# Админ отклоняет оплату
@router.callback_query(lambda c: c.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery):
    data = callback.data.replace("admin_reject_", "").split("_")
    ticket_id = int(data[0])
    user_id = int(data[1])

    cursor.execute('''
    UPDATE tickets SET status = 'rejected' WHERE ticket_id = ?
    ''', (ticket_id,))
    conn.commit()

    await callback.bot.send_message(
        user_id,
        f"❌ **ОПЛАТА НЕ ПОДТВЕРЖДЕНА**\n\n"
        f"Попробуй еще раз или напиши @Iouhh_def",
        parse_mode="Markdown"
    )

    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ ОТКЛОНЕНО",
        reply_markup=None
    )
    await callback.answer("❌ Отклонено!")


# Переписка в тикете (для админа) - ИСПРАВЛЕНО
@router.callback_query(lambda c: c.data.startswith("admin_reply_"))
async def admin_reply_start(callback: CallbackQuery, state: FSMContext):
    data = callback.data.replace("admin_reply_", "").split("_")
    ticket_id = int(data[0])
    user_id = int(data[1])

    await state.set_state("admin_reply")
    await state.update_data(reply_to_user=user_id, ticket_id=ticket_id)

    await callback.message.answer("✏️ Напиши ответ пользователю:")
    await callback.answer()


# Получение ответа от админа - ИСПРАВЛЕНО
@router.message(F.text)
async def admin_send_reply(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "admin_reply":
        data = await state.get_data()
        user_id = data.get('reply_to_user')
        ticket_id = data.get('ticket_id')

        if user_id:
            await message.bot.send_message(
                user_id,
                f"💬 **Админ**: {message.text}",
                parse_mode="Markdown"
            )
            await message.reply("✅ Ответ отправлен!")
            await state.clear()


# Сообщение от пользователя в тикете - ИСПРАВЛЕНО
@router.callback_query(lambda c: c.data.startswith("ticket_msg_"))
async def ticket_user_message(callback: CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.replace("ticket_msg_", ""))

    await state.set_state("user_ticket_reply")
    await state.update_data(ticket_id=ticket_id)

    await callback.message.answer("✏️ Напиши сообщение админу:")
    await callback.answer()


# Получение сообщения от пользователя - ИСПРАВЛЕНО
@router.message(F.text)
async def user_send_to_admin(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "user_ticket_reply":
        data = await state.get_data()
        ticket_id = data.get('ticket_id')

        await message.bot.send_message(
            ADMIN_ID,
            f"💬 **Сообщение от пользователя (тикет #{ticket_id})**:\n\n{message.text}"
        )
        await message.reply("✅ Сообщение отправлено админу!")
        await state.clear()


# Закрытие тикета пользователем
@router.callback_query(lambda c: c.data.startswith("ticket_close_"))
async def close_ticket(callback: CallbackQuery):
    ticket_id = int(callback.data.replace("ticket_close_", ""))

    cursor.execute('''
    UPDATE tickets SET status = 'closed' WHERE ticket_id = ?
    ''', (ticket_id,))
    conn.commit()

    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ ТИКЕТ ЗАКРЫТ",
        reply_markup=None
    )
    await callback.answer("❌ Тикет закрыт")


# Админ закрывает тикет
@router.callback_query(lambda c: c.data.startswith("admin_close_"))
async def admin_close_ticket(callback: CallbackQuery):
    data = callback.data.replace("admin_close_", "").split("_")
    ticket_id = int(data[0])
    user_id = int(data[1])

    cursor.execute('''
    UPDATE tickets SET status = 'closed' WHERE ticket_id = ?
    ''', (ticket_id,))
    conn.commit()

    await callback.bot.send_message(
        user_id,
        f"❌ **ТИКЕТ #{ticket_id} ЗАКРЫТ**\n\n"
        f"Если есть вопросы - напиши @Iouhh_def"
    )

    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ ТИКЕТ ЗАКРЫТ АДМИНОМ",
        reply_markup=None
    )
    await callback.answer("❌ Тикет закрыт")


# Не команда
@router.message()
async def mess(message: Message):
    await delete_previous_message(message)
    await message.answer("ты шо бальной?")