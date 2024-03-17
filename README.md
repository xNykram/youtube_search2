

<div class="center">
  <img src="https://i.ibb.co/f9f3tMM/image.png">
  <p>ytsearch2 is a <a href="https://github.com/joetats/youtube_search">youtube-search</a> fork. The main focus is adding new features and patches.</p>
</div>


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![GitHub Release](https://img.shields.io/github/v/release/xnykram/youtube_search2?&style=flat-square)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/xnykram/youtube_search2/pytest.yml?label=tests&style=flat-square)


## Example usage

### Using URL

``` Python
from youtube_search2 import YoutubeSearch

search_engine = YTSearch()
video_info = search_engine.search_by_url("https://www.youtube.com/watch?v=jNQXAC9IVRw")

output: {'id': 'jNQXAC9IVRw', 'title': 'Me at the zoo', 'thumbnail': 'https://i.ytimg.com/vi/jNQXAC9IVRw/maxresdefault.jpg', 'duration': '19063'}

```

### Using keyword

``` Python
from youtube_search2 import YoutubeSearch

search_engine = YTSearch()
video_info = search_engine.search_by_term("Me at the zoo", max_results=1)

output: [{'id': 'jNQXAC9IVRw', 'thumbnails': ['https://i.ytimg.com/vi/jNQXAC9IVRw/hqdefault.jpg?sqp=-oaymwE9COADEI4CSFryq4qpAy8IARUAAAAAGAElAADIQj0AgKJDeAHwAQH4Ab4CgALwAYoCDAgAEAEYVCBYKGUwDw==&rs=AOn4CLC4lp5lwDTP5b30m6scq6a7lKyA8Q'], 'title': 'Me at the zoo', 'long_desc': None, 'channel': 'jawed', 'duration': '0:19', 'views': '310\xa0243\xa0516 views', 'publish_time': '18 years ago', 'url_suffix': '/watch?v=jNQXAC9IVRw&pp=ygUNTWUgYXQgdGhlIHpvbw%3D%3D'}]

```

### Plans

- scrap more data like sub count for method `search_by_url`.

Please report any suggestions and issues [here](https://github.com/xNykram/youtube_search2/issues).
