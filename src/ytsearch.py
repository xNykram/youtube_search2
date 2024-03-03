import requests
import urllib.parse
import json
from bs4 import BeautifulSoup
import re

class YTSearch:
    def __init__(self):
        self.url: str
        self.videos: list

    def _parse_html(self, soup_obj: BeautifulSoup):
        video_id = re.search(r'(?<=\?v=)[\w-]+', self.url).group(0)
        title = soup_obj.find("meta", {"name": "title"})['content']
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        js_script = str(soup_obj.find_all("script")[20])
        duration_mil = re.search(r'"approxDurationMs":"(\d+)"',js_script).group(1)
        return {"id" : video_id, "title" : title, "thumbnail": thumbnail, "duration": duration_mil}
        
    def search_by_url(self, url: str):
        if "https://" in url:
            self.url = url
            response = requests.get(url).text
            soup_obj = BeautifulSoup(response, features="lxml")
            return self._parse_html(soup_obj)
    
    def search_by_term(self, term: str, max_results: int = 10):
        encoded_search = urllib.parse.quote_plus(term)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        
        results = []
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        for contents in data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["thumbnails"] = [
                        thumb.get("url", None)
                        for thumb in video_data.get("thumbnail", {}).get(
                            "thumbnails", [{}]
                        )
                    ]
                    res["title"] = (
                        video_data.get("title", {})
                        .get("runs", [[{}]])[0]
                        .get("text", None)
                    )
                    res["long_desc"] = (
                        video_data.get("descriptionSnippet", {})
                        .get("runs", [{}])[0]
                        .get("text", None)
                    )
                    res["channel"] = (
                        video_data.get("longBylineText", {})
                        .get("runs", [[{}]])[0]
                        .get("text", None)
                    )
                    res["duration"] = video_data.get("lengthText", {}).get(
                        "simpleText", 0
                    )
                    res["views"] = video_data.get("viewCountText", {}).get(
                        "simpleText", 0
                    )
                    res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                        "simpleText", 0
                    )
                    res["url_suffix"] = (
                        video_data.get("navigationEndpoint", {})
                        .get("commandMetadata", {})
                        .get("webCommandMetadata", {})
                        .get("url", None)
                    )
                    results.append(res)

            if results:
                if max_results is not None and len(results) > max_results:
                    return results[: max_results]
            self.videos = results
            return results

    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result

search_engine = YTSearch()
video_info = search_engine.search_by_term("Me at the zoo", max_results=1)
print(video_info)