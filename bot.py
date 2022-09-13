from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from voice_eng import text_to_file_eng
from voice_ru import text_to_file_ru


# download build(скачать или не заработает):     pip install python-telegram-bot==20.0a0


read_key = open('TOKEN.txt', 'rt')
TOKEN = read_key.readline()
read_key.close()



async def hello(update, context):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def reply(update, context):
    """Reply (echo) the user message."""
    # file_name = text_to_file(update.message.text)
    incoming_text = determine_language(update.message.text)
    print(incoming_text)
    if incoming_text == 'Russian':
        file_name = text_to_file_ru(update.message.text)
        language = f'{update.effective_user.first_name}, Ваше сообщение на русском языке и оно было следующим:'
        await update.message.reply_text(f'{language}\n\n{update.message.text}')  # зеркально возвращает сообщение пользоателя
        await update.message.reply_voice(voice=open(file_name, 'rb'))

    if incoming_text == 'English':
        file_name = text_to_file_eng(update.message.text)
        language = f'{update.effective_user.first_name}, Your message is in English and it was like this:'
        await update.message.reply_text(f'{language}\n\n{update.message.text}')  # зеркально возвращает сообщение пользоателя
        await update.message.reply_voice(voice=open(file_name, 'rb'))

    if incoming_text == 'Error':
        language = f'{update.effective_user.first_name}, язык не определен, БОТ понимает только русский и английский языки. The language is not defined, BOT understands only Russian and English:'
        await update.message.reply_text(f'{language}\n\n{update.message.text}')

    if incoming_text == 'Ru_Eng':
        language = f'{update.effective_user.first_name}, БОТ видит, что тут часть русского и часть английского текста, определитесь:) The BOT sees there is partly Russian and partly English tex, make your choice already:)'
        await update.message.reply_text(f'{language}\n\n{update.message.text}')


def determine_language(language):
    eng_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ru_string = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    # symbols = '! "#$%&()*+,-./:;<=>?@[\]^_`{|}~'''
    temp_list_eng = []
    temp_list_ru = []
    temp_list_error = []
    temp_list_no_symbols = []
    language_check = None
    processed_text = None

    for l in language:
        if l.isalpha():
            temp_list_no_symbols.append(l)
    processed_text = ''.join(temp_list_no_symbols)

    for letter in processed_text:
        for eng_letter in eng_string:
            if letter.find(eng_letter) in range(0, 94):
                # language_check = 'English'
                temp_list_eng.append(letter)
                break
                if letter.find(eng_letter) == -1:
                    temp_list_error.append(letter)

        for ru_letter in ru_string:
            if letter.find(ru_letter) in range(0, 108):
                # language_check = 'Russian'
                temp_list_ru.append(letter)
                break
        if letter.find(ru_letter) == -1 and letter.find(eng_letter) == -1:
            temp_list_error.append(letter)

    if len(temp_list_eng) == len(processed_text):
        language_check = 'English'
    if len(temp_list_ru) == len(processed_text):
        language_check = 'Russian'
    if len(temp_list_eng) >= 1 and len(temp_list_ru) >= 1 and len(temp_list_error) == 0:
        language_check = 'Ru_Eng'
    if len(temp_list_error) >= 1:
        language_check = 'Error'
    return language_check


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, determine_language))
app.run_polling()