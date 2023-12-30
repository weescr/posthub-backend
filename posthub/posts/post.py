import vk_api
import requests
from telegram import Bot
from telegram.error import BadRequest
from posthub.exceptions import SocialTokenError


async def post_to_vk(vk_token: str, title: str, description: str, content: str):
    try:
        vk_session = vk_api.VkApi(token=vk_token)
    except Exception as e:
        raise SocialTokenError from e

    finally:
        # константы с вк
        vk = vk_session.get_api()
        users = vk_session.method("users.get")
        user_id = users[0]['id']
        # Тут параметры, плюс постик сразу делаем, потому что мы крутые
        params = {
            'owner_id': user_id,
            'message': f"{title}\n\n{description}\n\n{content}",
        }
        try:
            vk.wall.post(**params)
        except Exception as e:
            raise vk_api.exceptions.AccessDenied

async def post_to_telegram(tgbot_token: str, tg_channel: str, title: str, description:str, content:str):
    try:
        tg_bot = Bot(token=tgbot_token)
    except Exception as e:
        raise SocialTokenError from e
    finally:
        tg_params = {
            'chat_id': tg_channel,
            'text': f"{title}\n\n{description}\n\n{content}",
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True,
        }
        try:
            await tg_bot.send_message(**tg_params)
        except:
            raise BadRequest
