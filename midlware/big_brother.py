from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from db.bd_cursor import cursor_connect
from settings.config import password


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, date: dict, state='*'):
        #print(update)
        if update.message:
            print('1')
            cursor_conn = cursor_connect()
            cursor = cursor_conn[0]
            conn = cursor_conn[1]
            id_person = update.message['from']['id']
            cursor.execute(f"SELECT user_id FROM key_access WHERE user_id='{id_person}'")
            user_info = cursor.fetchone()
            if user_info == None:
                cursor.execute(
                    f"INSERT INTO `key_access` (`id`, `user_id`, `access`) VALUES (NULL, '{id_person}', '0');")
                conn.commit()
            cursor.execute(f"SELECT access FROM key_access WHERE user_id='{id_person}';")
            access = cursor.fetchone()
            if access[0] == 1:
                pass
            else:

                if update.message.text == password:
                    cursor.execute(f"UPDATE `key_access` SET `access` = '1' WHERE user_id = {id_person};")
                    conn.commit()
                else:
                    raise CancelHandler()
            cursor.close()
        elif update.callback_query:
            print('2')
            id_person = update.callback_query.from_user.id
