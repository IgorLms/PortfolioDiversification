from aiogram.contrib.fsm_storage.memory import MemoryStorage
from variables import aiogram_api_token, telegram_my_id
from sheets_to_image import creating_pictures, del_file
from aiogram import Bot, Dispatcher, executor, types
from google_api import update_google_sheets
from aiogram.dispatcher import FSMContext
from variables import spreadsheet_id

# Настройка бота
bot = Bot(token=aiogram_api_token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


# Формирование клавиатуры
@dispatcher.message_handler(commands=['start'])
async def start_keyboard(message: types.Message):
    # Массив кнопок
    button = [
        [types.KeyboardButton(text="Диверсификация портфеля")]
    ]
    # Формирование клавиатуры
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=button,
        resize_keyboard=True
    )
    # Отправить сообщение
    await message.answer("Укажите, какую информацию необходимо показать:", reply_markup=keyboard)


# Ответ на кнопку
@dispatcher.message_handler(lambda message: message.text == "Диверсификация портфеля")
async def portfolio_diversification(message: types.Message, state: FSMContext):
    # Проверить, что это я и функция уже не запущена
    if message.from_user.id == telegram_my_id and await state.get_state() != 'run_state':
        # Изменить статус на запущено
        await state.set_state('run_state')
        # Отправить сообщение
        await message.answer('Ожидайте...')
        # Запустить формирование Google sheets
        if update_google_sheets():
            # Формирование картинок из Google sheets
            image_list = creating_pictures(spreadsheet_id)
            # Отправить картинки
            for image in image_list:
                await bot.send_photo(chat_id=telegram_my_id, photo=types.InputFile(image))
            # Добавить pdf файл в массив для удаления
            image_list.append("portfolio_diversification.pdf")
            # Удалить pdf и png
            del_file(image_list)
            # Сбросить статус запуска
            await state.finish()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
