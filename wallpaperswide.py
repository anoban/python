from urllib.request import urlopen

WALLPAPERSWIDE_BASE_URL: str = r"https://wallpaperswide.com"
WALLPAPERSWIDE_WALLPAPER_CATEGORY_URL: str = "https://wallpaperswide.com/{}-desktop-wallpapers.html"


def retrieve_thumbnail_grid_information(wallpaper_category: str) -> str:
    """ """

    first_category_page_uri: str = WALLPAPERSWIDE_WALLPAPER_CATEGORY_URL.format(wallpaper_category)
    with urlopen(url=first_category_page_uri) as request:
        webpage_content = request.read()
