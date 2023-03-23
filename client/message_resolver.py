from os.path import join
from cachetools import cached, TTLCache
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import xml.etree.ElementTree as ET
import re

class XMLMessageResolver(): 
    def __init__(self, root):
        self.root = root 

    @cached(TTLCache(16, 10))
    def get(self, name): 
        filename = f'{name}.xml'
        path = join(self.root, filename)

        tree = ET.parse(path)
        text = self.__prepare_text(tree)
        inline_reply_markup = self.__prepare_inline_reply_keyboard(tree)
        reply_markup = self.__prepare_reply_keyboard(tree)

        message = {
            'text': text,
            'reply_markup': inline_reply_markup if inline_reply_markup else reply_markup,
            'parse_mode': 'HTML'
        }
            
        return message
    
    def __prepare_text(self, tree):
        text = ET.tostring(tree.find('text'), encoding="unicode", method="html").strip()[6:-7]
        with_correct_indentation = re.sub(r'( )( )+', ' ', text)
        with_replaced_br = re.sub(r'<br/?>', '\n', with_correct_indentation)
        with_fixed_spaces = re.sub(r'\n( )*', '\n', with_replaced_br)

        return with_fixed_spaces
    
    def __prepare_inline_reply_keyboard(self, tree): 
        keyboard = tree.find('inline-keyboard')

        if keyboard is None: 
            return

        buttons = [[i.text.strip(), i.attrib] for i in keyboard.findall('button')]

        reply_markup = InlineKeyboardMarkup(resize_keyboard=True)
        
        for button in buttons: 
            reply_markup.add(InlineKeyboardButton(button[0], **button[1]))

        return reply_markup
    
    def __prepare_reply_keyboard(self, tree): 
        keyboard = tree.find('reply-keyboard')

        if keyboard is None: 
            return

        buttons = [[i.text.strip(), i.attrib] for i in keyboard.findall('button')]

        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        
        for button in buttons: 
            reply_markup.add(KeyboardButton(button[0]))

        return reply_markup