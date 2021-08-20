from datetime import date

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import CantParseEntities
from bot import reply_keyboards
from bot.reply_keyboards import reply_keyboard_texts, products, places, choice, after_choice
from bot.messages import bot_responses
from bot.handlers.utils import delete_messages, process_error
from db import db


class BuyProduct(StatesGroup):
    after_choice = State()
    user_id = State()
    place = State()
    date = State()
    choice = State()
    label = State()
    description = State()
    verification = State()
    message_ids = State()


async def navigate_category_state():
    return 'ok'


async def navigate_date_state(a, b):
    return 'ok'


async def navigate_state(message: types.Message, state: FSMContext) -> types.Message:
    print(state.get_state())
    if state.get_state() == 'date':
        client_settings = await db.get_client_settings(message.chat.id)
        if client_settings.asking_label:
            await BuyProduct.label.set()
            return await message.answer(text=bot_responses['adding expense']['label'],
                                        reply_markup=reply_keyboards.get_label_reply_keyboard(message.chat.id))
        if client_settings.asking_place:
            await BuyProduct.place.set()
            return await message.answer(text=bot_responses['adding expense']['place'],
                                        reply_markup=reply_keyboards.places)
        if client_settings.asking_description:
            await BuyProduct.description.set()
            return await message.answer(text=bot_responses['adding expense']['description'],
                                        reply_markup=reply_keyboards.description)


async def start_reply_buying(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text=db.get_products(),
                                       reply_markup=products)
    await state.update_data(message_ids=[message.message_id, bot_message.message_id])
    await BuyProduct.user_id.set()


async def process_user_id(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text="Выберите место доставки",
                                       reply_markup=reply_keyboards.places)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.next()


async def process_invalid_user_id(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text='Нет такого продукта',
                                       reply_markup=products)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])


async def process_place(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text="Вы уверены?",
                                       reply_markup=choice)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.choice.set()


async def process_choice_yes(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text="Ваш товар будет доставлен в выбранный пункт",
                                       reply_markup=reply_keyboards.menu_slave)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await state.finish()


async def process_after_choice_catalog(message: types.Message, state: FSMContext):
    bot_message = await message.answer(db.get_products(), reply_markup=products)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.user_id.set()


async def process_after_choice_place(message: types.Message, state: FSMContext):
    bot_message = await message.answer("Выберите место доставки?", reply_markup=places)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.place.set()


async def process_choice_no(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text='Куда вернуться?', reply_markup=after_choice)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.after_choice.set()


async def process_invalid_place(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text='Нет такого места',
                                       reply_markup=places)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])


async def process_invalid_choice(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text='Выберите из предложенных вариантов',
                                       reply_markup=choice)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])


async def process_after_choice_invalid(message: types.Message, state: FSMContext):
    bot_message = await message.answer(text='Выберите из предложенных вариантов',
                                       reply_markup=after_choice)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])


async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    bot_message = await message.answer(text=bot_responses['adding expense']['date'],
                                       reply_markup=reply_keyboards.dates)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.next()


async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    bot_message = await navigate_date_state(message, state)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])


async def process_label(message: types.Message, state: FSMContext):
    await state.update_data(label=message.text)
    bot_message = await message.answer(text=bot_responses['adding expense']['date'],
                                       reply_markup=reply_keyboards.dates)
    data = await state.get_data()
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.next()


async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text if message.text != reply_keyboard_texts['skip'][0] else '')
    data = await state.get_data()
    try:
        bot_message = await message.answer(
            text=bot_responses['adding expense']['verification of entered data'].format(
                user_id=data.get('user_id'),
                category=data.get('category'),
                label=data.get('label'),
                date=data.get('date'),
                place=data.get('place'),
                description=data.get('description'),
            ),
            reply_markup=reply_keyboards.create_reply_keyboards(
                reply_keyboard_texts['verification of entered data']
            )
        )
    except CantParseEntities as error:
        await process_error(error, message, state)
        return
    await state.update_data(message_ids=data['message_ids'] + [message.message_id, bot_message.message_id])
    await BuyProduct.next()


async def process_verification_is_ok(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await db.add_expense(
        telegram_user_id=message.chat.id,
        user_id=data['user_id'],
        category_name=data['category'],
        created_date=data['date'],
        label=data['label'],
        place=data['place'],
        description=data['description'],
    )
    await message.answer(
        text=bot_responses['adding expense']['verification is ok'].format(**data),
        reply_markup=reply_keyboards.menu
    )
    await delete_messages(message.chat.id, data.get('message_ids', []) + [message.message_id])
    await state.finish()


async def process_verification_is_not_ok(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=bot_responses['adding expense']['verification is not ok'],
                         reply_markup=reply_keyboards.menu)
    await delete_messages(message.chat.id, data['message_ids'] + [message.message_id])
    await state.finish()


def register_handlers_buying(dp: Dispatcher):
    dp.register_message_handler(start_reply_buying,
                                Text(equals=reply_keyboard_texts['menu slave']['Catalog'], ignore_case=True), state='*')
    dp.register_message_handler(process_user_id, lambda msg: msg.text in db.get_products(), state=BuyProduct.user_id)
    dp.register_message_handler(process_invalid_user_id, state=BuyProduct.user_id)
    dp.register_message_handler(process_place, lambda msg: msg.text in db.get_place(), state=BuyProduct.place)
    dp.register_message_handler(process_invalid_place, state=BuyProduct.place)
    dp.register_message_handler(process_choice_yes, Text(equals='да', ignore_case=True), state=BuyProduct.choice)
    dp.register_message_handler(process_choice_no, Text(equals='нет', ignore_case=True), state=BuyProduct.choice)
    dp.register_message_handler(process_invalid_choice, state=BuyProduct.choice)
    dp.register_message_handler(process_after_choice_catalog, Text(equals='product', ignore_case=True), state=BuyProduct.after_choice)
    dp.register_message_handler(process_after_choice_place, Text(equals='place', ignore_case=True),
                                state=BuyProduct.after_choice)
    dp.register_message_handler(process_after_choice_invalid,
                                state=BuyProduct.after_choice)

