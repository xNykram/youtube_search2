import pytest
from src.ytsearch import YTSearch
from requests import RequestException


@pytest.fixture
def yt_search():
    return YTSearch()


def test_search_by_url_valid(yt_search):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = yt_search.search_by_url(url)
    assert result["id"] == "dQw4w9WgXcQ"


def test_search_by_url_invalid(yt_search):
    url = "invalid_url"
    with pytest.raises(ValueError):
        yt_search.search_by_url(url)


def test_search_by_term(yt_search):
    term = "openai"
    result = yt_search.search_by_term(term)
    assert len(result) > 0


def test_search_by_term_not_finished_loop(yt_search, mocker):
    mocker.patch("src.ytsearch.YTSearch._prepare_data", return_value=[])
    term = "openai"
    result = yt_search.search_by_term(term)

    assert result == []


def test_search_by_term_no_results(yt_search):
    term = "#########################"
    result = yt_search.search_by_term(term)
    print(result)
    assert len(result) == 0


def test_search_by_term_with_max_results(yt_search):
    term = "openai"
    max_results = 5
    result = yt_search.search_by_term(term, max_results)
    assert len(result) == max_results


def test_search_by_url_exception(yt_search):
    with pytest.raises(RequestException) as exc_info:
        url = "https://wrong_url"
        yt_search.search_by_url(url)
    assert str(exc_info.value) == "Failed to fetch data from YouTube."
