import traceback

import telebot
from telebot import types

from config import BOT_TOKEN
from message_parser import get_suggestions
from polls import Poll

bot = telebot.TeleBot(BOT_TOKEN)
polls = {}


def generate_markup(message_hash, suggestions):
    keyboard = types.InlineKeyboardMarkup()
    for suggestion in suggestions:
        callback_button = types.InlineKeyboardButton(
            text=suggestion,
            callback_data=message_hash + ',' + suggestion
        )
        keyboard.add(callback_button)
    return keyboard


@bot.message_handler(content_types=["text"])
def any_msg(message):
    if message.chat.id > 0:
        bot.send_message(message.chat.id, 'Я не делаю опросы в одиночных чатах.')
        return
    print(message.text)
    suggestions = get_suggestions(message.text)
    if suggestions is None:
        return
    if len(suggestions) <= 1:
        return
    new_poll = Poll(suggestions)

    polls[str(hash(message))] = new_poll
    stat = new_poll.get_results()[1]
    bot.send_message(
        chat_id=message.chat.id,
        text=new_poll.get_title(),
        reply_markup=generate_markup(
            str(hash(message)),
            ['{} - {}'.format(e, stat[e]) for e in sorted(new_poll.suggestions)]
        )
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        poll_hash, suggestion = call.data.split(',')
        nickname = call.from_user.username
        poll = polls.get(poll_hash, None)
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
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            traceback.print_exc()
