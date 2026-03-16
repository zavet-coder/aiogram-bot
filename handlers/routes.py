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

router = Router()


# ТВОИ ОРИГИНАЛЬНЫЕ КНОПКИ
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Д3Ф")],
            [KeyboardButton(text="Д3АН0Н"), KeyboardButton(text="Д0Н0С")],  # Д0Н0С вместо СВ1ТТИНГ
            [KeyboardButton(text="СВ1ТТИНГ"), KeyboardButton(text="🌐 САЙТ")]  # Кнопка сайта
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


# 👇 ФУНКЦИЯ ДЛЯ УДАЛЕНИЯ СООБЩЕНИЯ
async def delete_previous_message(message: Message):
    try:
        await message.delete()
    except:
        pass


# 👇 ФУНКЦИЯ ДЛЯ УДАЛЕНИЯ СООБЩЕНИЯ ИЗ CALLBACK
async def delete_callback_message(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass


# 👇 ССЫЛКИ НА ФОТО
PHOTO_URLS = {
    "crypto_def": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_dox": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_dox_detailed": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_donos": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "crypto_swat": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_def": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_dox": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_dox_detailed": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_donos": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "donate_swat": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "info_more2": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "info_more3": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "def_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "dox_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
    "dox_normal_main": "https://postimg.cc/v1pnfyqs",
    "dox_detailed_main": "https://postimg.cc/Wtp2vBYC",
    "donos_main": "https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
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


# ========== Д0Н0С (7$) ==========
@router.message(Command("donos"))
@router.message(F.text.lower() == "д0нос")
@router.message(F.text.lower() == "донос")
async def donos_handler(message: Message):
    await delete_previous_message(message)
    await message.answer_photo(
        photo=PHOTO_URLS["donos_main"],
        caption="██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗\n"
                "██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝\n"
                "██║  ██║██║   ██║██╔██╗ ██║██║   ██║███████╗\n"
                "██║  ██║██║   ██║██║╚██╗██║██║   ██║╚════██║\n"
                "██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████║\n"
                "╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝\n\n"
                "[root@localhost]# ИНФОРМАЦИОННАЯ АТАКА\n"
                "──────────────────────────────\n"
                "▸ ДОНОС РОДСТВЕННИКАМ\n"
                "▸ ДОНОС КОЛЛЕГАМ ПО РАБОТЕ\n"
                "▸ ДОНОС НА УЧЕБУ\n"
                "▸ КОМПРОМЕТИРУЮЩАЯ ИНФОРМАЦИЯ\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 7$\n"
                "──────────────────────────────",
        reply_markup=get_payment_keyboard("donos")
    )


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
                "✉️ @Iouhh_def"
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
                "✉️ @Iouhh_def"
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
                "✉️ @Iouhh_def"
    )
    await callback.answer()


# 👇 ДОНОС 7$ (КРИПТА)
@router.callback_query(lambda c: c.data == "crypto_donos")
async def crypto_payment_donos(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["crypto_donos"],
        caption="[root@localhost]# КРИПТА · ДОНОС\n"
                "──────────────────────────────\n"
                "USDT TRC20:\n"
                "TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n"
                "──────────────────────────────\n"
                "💵 СУММА: 7 USDT\n"
                "📋 РОДСТВЕННИКИ + КОЛЛЕГИ + ФЕЙК КОМПРОМАТ\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def"
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
                "✉️ @Iouhh_def"
    )
    await callback.answer()


# ========== DONATIONALERTS ==========

@router.callback_query(lambda c: c.data == "donate_def")
async def donate_payment_def(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_def"],
        caption="[root@localhost]# DONATION · DEF\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 10$ / 1000р\n"
                "──────────────────────────────\n"
                "Обязательно:\n"
                "1. Пишешь в причине свой юз\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_donate_keyboard()
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
                "1. Пишешь в причине свой юз\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_donate_keyboard()
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
                "Обязательно:\n"
                "1. Пишешь в причине свой юз\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_donate_keyboard()
    )
    await callback.answer()


# 👇 ДОНОС 7$ (DONATE)
@router.callback_query(lambda c: c.data == "donate_donos")
async def donate_payment_donos(callback: CallbackQuery):
    await delete_callback_message(callback)
    await callback.message.answer_photo(
        photo=PHOTO_URLS["donate_donos"],
        caption="[root@localhost]# DONATION · ДОНОС\n"
                "──────────────────────────────\n"
                "💰 ЦЕНА: 7$ / 700р\n"
                "📋 РОДСТВЕННИКИ + КОЛЛЕГИ + КОМПРОМАТ\n"
                "──────────────────────────────\n"
                "1. Пишешь в причине свой юз\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_donate_keyboard()
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
                "Обязательно:\n"
                "1. Пишешь в причине свой юз\n"
                "──────────────────────────────\n"
                "✉️ @Iouhh_def",
        reply_markup=get_donate_keyboard()
    )
    await callback.answer()


# ========== РЕКЛАМА САЙТА ==========
@router.message(Command("site"))
@router.message(F.text.lower() == "сайт")
@router.message(F.text.lower() == "🌐 сайт")
async def site_handler(message: Message):
    await delete_previous_message(message)

    site_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 ПЕРЕЙТИ НА САЙТ", url="https://7ouhdef.up.railway.app/")],
            [InlineKeyboardButton(text="📋 ПОДРОБНЕЕ ОБ УСЛУГАХ", url="https://7ouhdef.up.railway.app/services")]
        ]
    )

    await message.answer_photo(
        photo="https://i.pinimg.com/736x/e4/6c/93/e46c93b203d60622025ff16364353616.jpg",
        caption="[root@localhost]# 7OUH.DEF - ОФИЦИАЛЬНЫЙ САЙТ\n"
                "──────────────────────────────\n"
                "🌐 На сайте ты можешь:\n"
                "▸ Подробнее ознакомиться с услугами\n"
                "▸ Узнать цены и способы оплаты\n"
                "▸ Почитать FAQ\n"
                "🔗 Переходи по ссылке ниже\n"
                "──────────────────────────────",
        reply_markup=site_button
    )


# ========== НЕ КОМАНДА ==========
@router.message()
async def mess(message: Message):
    await delete_previous_message(message)
    await message.answer("ты шо бальной?")