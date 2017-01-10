# -*- coding: utf-8 -*-
import re

from slackbot.bot import respond_to, default_reply


@default_reply()
def my_default_handler(message):
    message.reply('Hey there! How can I help you?')


@respond_to('\?', re.IGNORECASE)
@respond_to('help', re.IGNORECASE)
def show_help(message):
    message.reply('docs')
