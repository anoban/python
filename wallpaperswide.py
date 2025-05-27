# https://wallpaperswide.com/games-desktop-wallpapers.html
# https://wallpaperswide.com/spider_man_miles_morales_art-wallpapers.html

# import re
# from bs4 import BeautifulSoup

import argparse
from typing import Union, override
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

WALLPAPERSWIDE_BASE_URL: str = r"https://wallpaperswide.com"
WALLPAPERSWIDE_WALLPAPER_DOWNLOAD_TEMPLATE_URL: str = r"https://wallpaperswide.com/download/{}"


class FirefoxImpersonator(Request):
    # impersonate Firefox Win64 to avoid request denials by the server
    def __init__(self, url: str) -> None:
        """
        to be used as a drop-in replacement for a Request type objects with urlopen()
        """
        super().__init__(
            url,
            data=None,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"},
            origin_req_host=None,
            unverifiable=False,
            method="GET",
        )


class WallpaperCategory(object):
    WALLPAPERSWIDE_WALLPAPER_CATEGORY_TEMPLATE_URL: str = r"https://wallpaperswide.com/{}-desktop-wallpapers.html"
    WALLPAPERSWIDE_VALID_WALLPAPER_CATEGORIES: list[str] = [  # categories valid in wallpaperswide as of writing
        "aero",
        "animals",
        "architecture",
        "army",
        "artistic",
        "awareness",
        "black_and_white",
        "cartoons",
        "celebrities",
        "city",
        "computers",
        "cute",
        "elements",
        "food_and_drink",
        "funny",
        "games",
        "girls",
        "holidays",
        "love",
        "motors",
        "movies",
        "music",
        "nature",
        "seasons",
        "space",
        "sports",
        "travel",
        "vintage",
    ]

    def __init__(self, _category: str) -> None:
        if _category not in WallpaperCategory.WALLPAPERSWIDE_VALID_WALLPAPER_CATEGORIES:  # do a preliminary input validation
            raise ValueError(
                f"Invalid wallpaper category {_category}, expected one of {WallpaperCategory.WALLPAPERSWIDE_VALID_WALLPAPER_CATEGORIES}"
            )

        self._category: str = _category
        self._url: str = WallpaperCategory.WALLPAPERSWIDE_WALLPAPER_CATEGORY_TEMPLATE_URL.format(_category)

    @override
    def __repr__(self) -> str:
        return f"{self._category} :: url <<{self._url}>>"

    def url(self) -> str:
        """
        returns the url for the wallpaper category of choice,
        when the choosen category is "games" the returned url will be https://wallpaperswide.com/games-desktop-wallpapers.html"
        """
        return self._url


def download_category_first_thumbnails_page(category: WallpaperCategory) -> str | None:
    try:
        with urlopen(FirefoxImpersonator(category.url())) as connection:
            html_page = connection.read()
    except BaseException as error:
        raise RuntimeError(f"{error.__dict__}") from error
    return html_page


def extract_wallpaper_page_links_from_thumbnails_and_next_thumbnails_page_link(_wallpapers_grid_page_link: str) -> tuple[tuple[str], str]:
    """
    returns the links for each thumbnail in the current page and the link to the next thumbnails page
    """
    soup: BeautifulSoup = BeautifulSoup(_wallpapers_grid_page_link, features="html.parser")
    pass


def download_wallpaper_download_page(_wallpaper_url: str) -> str:
    """ """
    with urlopen(url=FirefoxImpersonator(url=_wallpaper_url)) as connection:
        wallpaper_download_page: str = connection.read()


def extract_best_169_resolution_link(wallpaper_resolutions_html_div: str) -> Union[str, None]:
    """
    16:9
    """
    [
        _.get("href", None)
        for _ in link_grid.find_all("a", attrs={"target": "_self"})
        if "16:9" in _.get("title") and "Dual" not in _.get("title")
    ][-1]


def extract_best_1610_resolution_link(wallpaper_resolutions_html_div: str) -> Union[str, None]:
    """
    16:10
    """

    [
        _.get("href", None)
        for _ in link_grid.find_all("a", attrs={"target": "_self"})
        if "16:10" in _.get("title") and "Dual" not in _.get("title")
    ][-1]


def parse_programme_commandline_arguments() -> dict[str, str]:
    """ """

    parser = argparse.ArgumentParser(prog=r"WallpapersWide")
    pass


def main() -> None:
    """ """
    first_page: str | None = download_category_first_thumbnails_page(WallpaperCategory(r"girls"))
    print(first_page)


if __name__ == "__main__":
    main()
