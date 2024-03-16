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
        video_id = re.search(r"(?<=\?v=)[\w-]+", self.url).group(0)
        title = soup_obj.find("meta", {"name": "title"})["content"]
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        js_script = str(soup_obj.find_all("script")[20])
        duration_mil = re.search(r'"approxDurationMs":"(\d+)"', js_script).group(1)
        return {
            "id": video_id,
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration_mil,
        }

    def _fetch_yt_data(self) -> str:
        try:
            response = requests.get(url=self.url)
            response.raise_for_status()
        except requests.RequestException:
            raise requests.RequestException("Failed to fetch data from YouTube.")
        return response.text

    def search_by_url(self, url: str):
        if "https://" in url:
            self.url = url
            response = self._fetch_yt_data()
            soup_obj = BeautifulSoup(response, features="lxml")
            return self._parse_html(soup_obj)
        else:
            raise ValueError("Please provide valid URL.")

    def search_by_term(self, term: str, max_results: int = None):
        encoded_search = urllib.parse.quote_plus(term)
        BASE_URL = "https://youtube.com"
        self.url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = self._fetch_yt_data()

        results = []
        searched_obj = self._prepare_data(response)
        for contents in searched_obj:
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
                    return results[:max_results]
            self.videos = results
            break
        return results

    def _prepare_data(self, response):
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)
        searched_obj = data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]

        return searched_obj
