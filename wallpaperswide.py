# https://wallpaperswide.com/games-desktop-wallpapers.html
# https://wallpaperswide.com/spider_man_miles_morales_art-wallpapers.html

# import re
import argparse
import sys
from typing import Optional, Union, override
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, element

WALLPAPERSWIDE_BASE_URL: str = r"https://wallpaperswide.com"
WALLPAPERSWIDE_WALLPAPER_DOWNLOAD_TEMPLATE_URL: str = r"https://wallpaperswide.com/download/{}"


class FirefoxImpersonator(Request):
    # impersonate Firefox Win64 to avoid request denials by the server

    """
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate, br, zstd
    Content-Type: application/json;odata=verbose
    Prefer: NotificationSession
    DNT: 1
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: same-origin
    Sec-Fetch-Site: same-origin
    Connection: keep-alive
    Cookie: rtFa=fgmdwXK9FWPCrFk3ncwXiMS47dkQI7VJfjAEKPenh4AmM2VkYmYxMzgtNzgwZC00MTE4LWE0OGMtMzFjNTJiOGNhNmE1IzEzMzkyODcwNDM2Mzg3NzQ4NiNmNTZiYTJhMS01MGRlLTUwMDAtNGVhYS0xMzFlZDY2MGRlZDMjOTA5NjM0MjUlNDB3ZXN0ZXJuc3lkbmV5LmVkdS5hdSMxOTY0MjkjcDI4SXlmdEpQaGgydnlRbUFjdmZSR0xSRjU0I3R5R1RTYTlSeG02My03bzc3VXdZODdWaC1lSV9s7TzrDZbX0Cpbp4kTaOgL+TDFAcJrPVLUgIxomQjwRnI2uyNKusAcbSShiLfMZyqIoj7VHYe30/oGYHjtDGl8mJLVeDy0A3tLILOAEnDlWW1FHs/e0zjq8xOqNgHNgSoHKCw324njv9Fb0bhBMFdTBZ6nq5U3MTgscLjIAHghNXVMBS53sjotLK8zbPB7sqE4/9c0BiNKUQ0hnFpD8JuGdOfNl1A43HJrMJmc08a+tuZwlaq6MRpsGxDlpcAI+3ExpszZI9pOnCI40OSAw6MQvoSpjMKbsDwXgl+n0uwVxpHD61RwE/f1BnIMIbnTW0jheA1F+2n6uh3J9JVoChbcAAAA; SIMI=eyJzdCI6MH0=; FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE0LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwNDJkNjE1MjZkQGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHw5MDk2MzQyNUB3ZXN0ZXJuc3lkbmV5LmVkdS5hdSwxMzM5Mjg3MDQyNjAwMDAwMDAsMTMzOTA4MTYxNDcwMDAwMDAwLDEzMzkzMzAyNDM2MzcyMTIxNSwxMzcuMTU0LjYwLjIyOCw2NywzZWRiZjEzOC03ODBkLTQxMTgtYTQ4Yy0zMWM1MmI4Y2E2YTUsLDAwNTA5OGU5LTgzMzktMTNhYy0yZDU0LWYwYWY4MTc5MmE0MixmNTZiYTJhMS01MGRlLTUwMDAtNGVhYS0xMzFlZDY2MGRlZDMsZjU2YmEyYTEtNTBkZS01MDAwLTRlYWEtMTMxZWQ2NjBkZWQzLCwwLDEzMzkyOTU2ODM2MzQwODY4NiwxMzM5MzEyOTYzNjM0MDg2ODYsLCxleUpqWVhCdmJHbGtjMTlzWVhSbFltbHVaQ0k2SWx0Y0lqWXpOVGRpTnpsbUxUSTROMkl0TkdNME9DMDRZalptTFdFMllXUTFPREE0TnpneVkxd2lYU0lzSW5odGMxOWpZeUk2SWx0Y0lrTlFNVndpWFNJc0luaHRjMTl6YzIwaU9pSXhJaXdpY0hKbFptVnljbVZrWDNWelpYSnVZVzFsSWpvaU9UQTVOak0wTWpWQWQyVnpkR1Z5Ym5ONVpHNWxlUzVsWkhVdVlYVWlMQ0oxZEdraU9pSXpUWFpoVDBOTlFVaEZRMDFuYmpGQ1JFTnRORUZCSW4wPSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzMzkyODcwNDM2MDAwMDAwMCwzYzIwYmQ2Zi0xNzk5LTRlZmItOTI1Ni1hMjhjNWZjZjFmNDIsLCwsLCwxMTUyOTIxNTA0NjA2ODQ2OTc2LCwxOTY0MjksVTNKTFZ1TFJXVGY0ZVhKSU9TdGV3WkhGeTd3LCxMMWxRbTN4dEszZkFZaHlKQkM1N2Y5QUV3NlNJTmViQUhzS3U5Yjg4N04wdkZzRVNjeG5Xa3FMUk0zV21ET3IvTGF6ZzJ1VDBEdk8zVmVQSEVBSit5VEVTT2VpbDcrOVVzYTUxZE5COXZHVzNneHpZcWp2NHQ5RVVrV05yRkdTRUMvTG1FVE85bHB3U1lHUVpxREZCRGd4QWZsU05BRTJDK28yQVpaT242a3dnNlFmeEJ2UjZ1N0YxM1FrWnIvbUpJUUt3dDN4RHk4aUMwcVNsNU1hd2RuNE1wd2xqMFhHQnlCa3V2TW12WGpJWTVhaktiUmxKcmQ0cEJ3dHpycUlBend2S3RNTlg0MnhSL1dsWEFTLzNxQkhmUzhnQk5PTnNuYXJnNXNWV25IbkpLalhhRGZGdjNVcHVKeklWbjRxZ2VnaWFKOUNsd2ppN3NDOG1QdkNUL3c9PTwvU1A+; FeatureOverrides_experiments=[]; ai_session=xMGc1WYbp2wjaGGqYW2AtY|1748396836943|1748400391680; MSFPC=GUID=abc29ab7ef794aaa804aedbb060ee6f3&HASH=abc2&LV=202505&V=4&LU=1748396841774; odbn=1; MicrosoftApplicationsTelemetryDeviceId=b1efa4bc-c5e6-4c9f-8267-6d7717fe58ff
    Priority: u=4
    """

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


def extract_wallpaper_page_links_from_thumbnails_and_next_thumbnails_page_link(_thumbnail_grid_page: str) -> tuple[list[str], str]:
    """
    returns the links for each thumbnail in the current page and the link to the next thumbnails page
    the html parsing logic used in this function is very brittle and highly sensitive to the markup structure in the web page
    any changes by the frontend developers to the markup could possibly break the logic and result in errors.
    """
    page: BeautifulSoup = BeautifulSoup(_thumbnail_grid_page, features="html.parser")
    thumbnail_grid: Optional[Union[element.PageElement, element.Tag, element.NavigableString]] = page.find(
        "ul", attrs={"class": "wallpapers"}
    )

    return (
        [
            WALLPAPERSWIDE_BASE_URL  # should be in this format - https://wallpaperswide.com/racing_mercedes_amg_sports_car-wallpapers.html
            + thumb.find("div", attrs={"class": "thumb"})  # start the descent into the thumbnail tag hierarchy
            .find(
                "div", attrs={"align": "center", "class": "mini-hud", "id": "hudtitle"}
            )  # locate the <div> with the format <div align="center" class="mini-hud" id="hudtitle"> that contains the link to the wallpaper's html page
            .find(
                "a"
            )  # find the <a> like <a href="/cute_kitten_close_up-wallpapers.html" title="Cute Kitten Close-up 4K UHD Wallpaper for Widescreen and UltraWide Desktop, UltraHD TV, Smartphone, Tablet">
            .get("href", "")  # harvest the actual link from the <a> tag
            for thumb in thumbnail_grid.find_all("li", attrs={"class": "wall"}, recursive=True)  # for each thumbnail in the thumbnail grid
        ],
        "",
    )


def download_html(_wallpaper_url: str) -> str:
    """
    a generic
    """

    try:
        with urlopen(FirefoxImpersonator(url=_wallpaper_url)) as connection:
            html_page = connection.read()
    except BaseException as error:
        raise RuntimeError(f"{error.__dict__}") from error
    return html_page


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
    parser.add_argument("--category")
    parser.add_argument("--parallel-downloads")
    parser.add_argument("--include-random-waits")


def main() -> None:
    """ """
    print(sys.argv)
    first_thumbnails_page: str | None = download_html(WallpaperCategory(r"motors").url())
    print(extract_wallpaper_page_links_from_thumbnails_and_next_thumbnails_page_link(first_thumbnails_page))


if __name__ == "__main__":
    main()
