import re
import requests
from plugins import register, Plugin, Event, logger, Reply, ReplyType
from bs4 import BeautifulSoup
import random

@register
class Nsfw(Plugin):
    name = "nsfw"

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
        return "Use the command #nsfw(or whatever you like set with command field in the config) to get a wonderful video"

    def reply(self) -> Reply:
        reply = Reply(ReplyType.TEXT, "Failed to get nsfw videos")
        try:
            random_page = random.randint(1, 20)
            url = "https://bad.news/tag/porn/sort-hot/page-"+str(random_page)
            video_sources = self.get_video_sources(url)
            videos_url = random.choice(video_sources)
            if len(videos_url) > 0:
                reply = Reply(ReplyType.VIDEO, f"http:{videos_url}")
            else:
                logger.error("Error: Unrecognized URL connection")

        except Exception as e:
            logger.error(f"Video api call error: {e}")
        return reply
    def get_video_sources(self,url):
        # Send an HTTP request to the webpage
        response = requests.get(url)
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the video tags in the HTML document
        video_tags = soup.find_all('video')
        # Extract the source links from the video tags
        video_sources = []
        for video_tag in video_tags:
            source_tags = video_tag.find_all('source')
            for source_tag in source_tags:
                source_link = source_tag.get('src')
                if source_link:
                    video_sources.append(source_link)
        # Return the list of video source links
        return video_sources
    
