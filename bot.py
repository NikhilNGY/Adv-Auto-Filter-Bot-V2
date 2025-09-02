#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @SpEcHIDe

from pyrogram import Client
from pyrogram.types import BotCommand

from .config import API_HASH, APP_ID, LOGGER, BOT_TOKEN
from .user import User


class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "bot/plugins"},
            workers=200,
            bot_token=BOT_TOKEN,
            sleep_threshold=10,
        )
        self.LOGGER = LOGGER
        self.user: User = None
        self.user_id: int = None

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(f"@{bot_details.username} started!")
        self.user, self.user_id = await User().start()
        await self.set_bot_commands(
            [
                BotCommand("start", "Starts the bot"),
                BotCommand("help", "Shows the help message"),
                BotCommand("about", "Shows the about message"),
            ]
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
