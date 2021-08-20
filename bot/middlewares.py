"""Аутентификация — пропускаем сообщения только от одного Telegram аккаунта"""
import logging
import yaml
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from typing import List


class AccessMiddleware(BaseMiddleware):
    def __init__(self, accessed_id: List[int]):
        self.accessed_id = accessed_id
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if int(message.from_user.id) not in self.accessed_id:
            await message.answer('Access Denied')
            raise CancelHandler()


class HZMiddleware(BaseMiddleware):
    def __init__(self):
        with open('bot/phrases/response_messages.yaml', encoding='utf-8') as yaml_file:
            self.bot_responses = yaml.safe_load(yaml_file)
        # self.bot_responses = self.__parse_bot_responses_to_markdownV2(self.bot_responses)
        super().__init__()

    def __parse_bot_responses_to_markdownV2(self, bot_responses):
        for key, value in bot_responses.items():
            if not isinstance(value, str):
                bot_responses[key] = self.__parse_bot_responses_to_markdownV2(value)
            else:
                bot_responses[key] = value.replace('.', '\.')
        return bot_responses

    async def on_pre_process_message(self, _: types.Message, data: dict):
        logging.info(data)
        data['bot_responses'] = self.bot_responses

    @staticmethod
    async def on_post_process_message(message: types.Message, data_from_handler: List, data: dict):
        logging.info(data.keys())
        logging.info(data_from_handler)
        text = data_from_handler[0]['text'].replace('.', r'\.')
        reply_markup = data_from_handler[0].get('reply_markup')
        await message.answer(text=text, reply_markup=reply_markup)
