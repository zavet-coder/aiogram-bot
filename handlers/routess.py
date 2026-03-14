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

# Команды на панели
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Д3Ф")],
            [KeyboardButton(text="Д3АН0Н"), KeyboardButton(text="СВ1ТТИНГ")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Клавиатура для выбора способа оплаты
def get_payment_keyboard(service_type: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплата по Крипте", callback_data=f"crypto_{service_type}")],
            [InlineKeyboardButton(text="Оплата по DonationAlerts", callback_data=f"donate_{service_type}")],
        ]
    )
    return keyboard

# Оплата по донату
def get_donate_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить", url="https://www.donationalerts.com/r/iouhh_def")]
        ]
    )
    return keyboard

# Клавиатура для деффа (бесплатный/платный)
def get_def_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Бесплатный дефф", callback_data="info_more2")],
            [InlineKeyboardButton(text="Платный дефф", callback_data="info_more3")]
        ]
    )
    return keyboard

# Оплата по крипте деф
@router.callback_query(lambda c: c.data == "crypto_def")
async def crypto_payment_def(callback: CallbackQuery):
    await callback.message.answer("USDT TRC20: TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n\nПосле оплаты пиши @Iouhh_def\n\nСумма 10$ навсегда")
    await callback.answer()

# Оплата по крипте докс
@router.callback_query(lambda c: c.data == "crypto_dox")
async def crypto_payment_dox(callback: CallbackQuery):
    await callback.message.answer("USDT TRC20: TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n\nПосле оплаты пиши @Iouhh_def\n\nСумма 3 USDT")
    await callback.answer()

# Оплата по крипте сват
@router.callback_query(lambda c: c.data == "crypto_swat")
async def crypto_payment_swat(callback: CallbackQuery):
    await callback.message.answer("USDT TRC20: TGrtRCizSghyrp8pjZsMb5pc31v9JsRfyF\n\nПосле оплаты пиши @Iouhh_def\n\nСумма 20 USDT")
    await callback.answer()

# Инструкция по донату деф
@router.callback_query(lambda c: c.data == "donate_def")
async def donate_payment_def(callback: CallbackQuery):
    await callback.message.answer("Цена: 10$\n\nИнструкция:\nЗаходишь на сайт - вводишь сумму и оплачиваешь.\n\n1$ = 100р а не по курсу.\n\nПосле оплаты пиши @Iouhh_def", reply_markup=get_donate_keyboard())
    await callback.answer()

# Инструкция по донату докс
@router.callback_query(lambda c: c.data == "donate_dox")
async def donate_payment_dox(callback: CallbackQuery):
    await callback.message.answer("Цена: 3$\n\nИнструкция:\nЗаходишь на сайт - вводишь сумму и оплачиваешь.\n\n1$ = 100р а не по курсу.\n\nПосле оплаты пиши @Iouhh_def", reply_markup=get_donate_keyboard())
    await callback.answer()

# Инструкция по донату сват
@router.callback_query(lambda c: c.data == "donate_swat")
async def donate_payment_swat(callback: CallbackQuery):
    await callback.message.answer("Цена: 20$\n\nИнструкция:\nЗаходишь на сайт - вводишь сумму и оплачиваешь.\n\n1$ = 100р а не по курсу.\n\nПосле оплаты пиши @Iouhh_def", reply_markup=get_donate_keyboard())
    await callback.answer()

# Бесплатный дефф
@router.callback_query(lambda c: c.data == "info_more2")
async def def_free(callback: CallbackQuery):
    await callback.message.answer("Что входит в бесплатный Д3Ф?\n\n1) Защита от Д3АН0НА/УГР03\n2) Полный Д0КС на Ж3РТВУ\n3) Д0Н0С на Ж3РТВУ\n\nНО ТОЛЬКО НА 1 РАЗ\nДля получения бесплатного деффа напиши @Iouhh_def")
    await callback.answer()

# Платный дефф
@router.callback_query(lambda c: c.data == "info_more3")
async def def_paid(callback: CallbackQuery):
    await callback.message.answer("Что входит в платный Д3Ф?\n\n1) Защита от Д3АН0НА/УГР03\n\n2) Полный Д0КС на Ж3РТВУ\n\n3) Д0Н0С на Ж3РТВУ", reply_markup=get_payment_keyboard("def"))
    await callback.answer()

# Старт
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! *Это бот с услугами от @Iouhh_def*\n\nВыбери то что тебе нужно",
        parse_mode="Markdown",
        reply_markup=get_main_reply_keyboard()
    )

# Деф
@router.message(Command("def"))
@router.message(F.text.lower() == "д3ф")
async def def_handler(message: Message):
    await message.answer(
        "*Деффинг* - защита от деанона/угроз.", reply_markup=get_def_keyboard(),
        parse_mode="Markdown")

# Докс
@router.message(Command("dox"))
@router.message(F.text.lower() == "д3ан0н")
async def dox_handler(message: Message):
    await message.answer(
        "*Деанон* - поиск всей информации о жертве.", reply_markup=get_payment_keyboard("dox"),
        parse_mode="Markdown")

# Сват
@router.message(Command("swat"))
@router.message(F.text.lower() == "св1ттинг")
async def swat_handler(message: Message):
    await message.answer(
        "*Сваттинг* - ложное минирование.\n\nЦена: *20$\n\nПосле оплаты пиши @Iouhh_def*", reply_markup=get_payment_keyboard("swat"),
        parse_mode="Markdown")

# Не команда
@router.message()
async def mess(message: Message):
    await message.answer("ты шо бальной?")