#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from bot import Bot
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1001951277428

if __name__ == "__main__":
    Bot().run()
