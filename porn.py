import re
import requests
from plugins import register, Plugin, Event, logger, Reply, ReplyType
import base64
import json
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
@register
class Porn(Plugin):
    name = "porn"
    key = 'B1A1Fwi4YNeIm1ce'
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

    def encrypt(raw):
        raw_str = json.dumps(raw)
        raw_bytes = pad(raw_str.encode(), 16)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw_bytes))

    def decrypt(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(enc), 16)
        plaintext = plaintext.decode('utf-8')
        return json.loads(plaintext)

    def reply(self) -> Reply:
        reply = Reply(ReplyType.TEXT, "Failed to get porn videos")
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
            params = {'order_key': '', 'tag_id': '', 'is_long': 0, 'paytype': '', 'keywords': '', 'type_id': '', 'code': '', 'page': 1, 'page_size': 20}
            payload=json.dumps(params)
            payload = self.encrypt(payload)
            response = requests.post(
                "https://c.onljx.cc/h5/app/api/video/search", data=payload,headers = header
            ).json()
            print(response)
            if response['code'] == 200:

                choiceData = self.decrypt(response['data'])
                choiceItem = random.choice(choiceData)

                videos_url = choiceItem['smu']
                print(videos_url)
                if len(videos_url) > 0:
                    reply = Reply(ReplyType.M3U8, f"{videos_url}")
                else:
                    logger.error("Error: Unrecognized URL connection")
            else:
                logger.error(f"Abnormal site status, request: ")
        except Exception as e:
            logger.error(f"Video api call error: {e}")
        return reply
