import re
import requests
response = requests.get(
                "https://tucdn.wpon.cn/api-girl/", timeout=5, verify=False
            )
print(response.text)
videos_url = re.findall(
                    '<video src="(.*?)" muted controls preload="auto"',
                    response.text,
                    re.S,
                )
print(videos_url)