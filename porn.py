import re
import requests
from plugins import register, Plugin, Event, logger, Reply, ReplyType
import base64
import json
import random
@register
class Porn(Plugin):
    name = "porn"

    def did_receive_message(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        query = event.context.query
        if query == self.config.get("command"):
            event.reply = self.reply()
            event.bypass()

    def will_send_reply(self, event: Event):
        pass

    def help(self, **kwargs) -> str:
        return "Use the command #porn(or whatever you like set with command field in the config) to get a wonderful video"

    def reply(self) -> Reply:
        reply = Reply(ReplyType.TEXT, "Failed to get porn videos")
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'X-User-Token': '73e93643d4724af0a2c5abe6eff4f562',
                'X-User-Id': '22677860'
            }
            response = requests.get(
                "https://hj4deca.top/api/video/node_list?pageIndex=1&type=1", headers = header
            ).json()
            if response['success'] == 'True':

                decodeData = base64.b64decode(response['data']).decode('utf-8')
                decodeData2 = base64.b64decode(decodeData).decode('utf-8')
                finalData = base64.b64decode(decodeData2).decode('utf-8')
                choiceData = json.loads(finalData)
                choiceItem = random.choice(choiceData)

                videos_url = choiceItem['attachment']['remoteUrl'],
                if len(videos_url) > 0:
                    reply = Reply(ReplyType.VIDEO, f"{videos_url}")
                else:
                    logger.error("Error: Unrecognized URL connection")
            else:
                logger.error(f"Abnormal site status, request: ")
        except Exception as e:
            logger.error(f"Video api call error: {e}")
        return reply
