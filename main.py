import sys
import traceback
import logging

import telebot
from telebot import types

from config import BOT_TOKEN, POLLS_STORAGE_DIR
from message_parser import get_suggestions_in_common_case, COMMON_TRIGGER_PATTERN, BREAKFAST_TIME_TRIGGER_PATTERN,\
    DINNER_PLACE_TRIGGER_PATTERN, DINNER_TIME_TRIGGER_PATTERN
from polls import Poll, create_new_breakfast_time_poll, create_new_dinner_place_poll, create_new_dinner_time_poll
from storage import Storage

bot = telebot.TeleBot(BOT_TOKEN)
polls_storage = Storage(POLLS_STORAGE_DIR)
logging.getLogger().setLevel(logging.INFO)


def generate_markup(message_hash, suggestions):
    keyboard = types.InlineKeyboardMarkup()
    for suggestion in suggestions:
        callback_button = types.InlineKeyboardButton(
            text=suggestion,
            callback_data=message_hash + ',' + suggestion
        )
        keyboard.add(callback_button)
    return keyboard


def send_answer_by_poll(message, new_poll):
    polls_storage[str(hash(message))] = new_poll
    stat = new_poll.get_results()[1]
    bot.send_message(
        chat_id=message.chat.id,
        text=new_poll.get_title(),
        reply_markup=generate_markup(
            str(hash(message)),
            ['{} - {}'.format(e, stat[e]) for e in sorted(new_poll.suggestions)]
        )
    )


@bot.message_handler(content_types=['text'], regexp=COMMON_TRIGGER_PATTERN)
def common_case(message):
    logging.info('common case has been triggered')
    if message.chat.id > 0:
        bot.send_message(message.chat.id, 'Я не делаю опросы в одиночных чатах.')
        return
    logging.info('Handle text: "{}"'.format(message.text))
    suggestions = get_suggestions_in_common_case(message.text)
    if suggestions is None:
        return
    if len(suggestions) <= 1:
        return
    send_answer_by_poll(message, Poll(suggestions))


@bot.message_handler(content_types=['text'], regexp=DINNER_TIME_TRIGGER_PATTERN)
def dinner_time_case(message):
    logging.info('dinner time case has been triggered')
    send_answer_by_poll(message, create_new_dinner_time_poll())


@bot.message_handler(content_types=['text'], regexp=DINNER_PLACE_TRIGGER_PATTERN)
def dinner_place_case(message):
    logging.info('dinner place case has been triggered')
    send_answer_by_poll(message, create_new_dinner_place_poll())


@bot.message_handler(content_types=['text'], regexp=BREAKFAST_TIME_TRIGGER_PATTERN)
def breakfast_time_case(message):
    logging.info('breakfast time case has been triggered')
    send_answer_by_poll(message, create_new_breakfast_time_poll())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    logging.info('callback with data: {}'.format(call.data))
    if call.message:
        poll_hash, suggestion = call.data.split(',')
        nickname = call.from_user.username
        poll = polls_storage.get(poll_hash)
        if poll is None:
            return
        poll.vote(nickname, suggestion.split()[0])
        title_suffix, stat = poll.get_results()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=poll.get_title() + '\n' + title_suffix,
            reply_markup=generate_markup(poll_hash, ['{} - {}'.format(e, stat[e]) for e in sorted(poll.suggestions)])
        )


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-d':
            logging.info('DEBUG MODE ON')
            bot.polling(none_stop=True)
            sys.exit(0)
    while True:
        try:
            bot.polling(none_stop=True)
            logging.info('bot has been restarted')
        except Exception:
            traceback.print_exc()
            logging.info('restart after exception')
