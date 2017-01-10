import logging
import os

from slackbot.bot import Bot


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
