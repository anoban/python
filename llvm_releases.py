import re
import sys
import typing
from urllib import (request, error)
import threading
import ctypes
from ctypes import (windll, wintypes)
from bs4 import BeautifulSoup


def fetch_llvm_releases_github_page() -> str:
    """

    Returns the HTML page at https://github.com/llvm/llvm-project/releases as a string object.

    """

    page: str = ""
    LLVM_RELEASE_PAGE = r"https://github.com/llvm/llvm-project/releases"
    req = request.Request(url=LLVM_RELEASE_PAGE, method="GET", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Connection": "close"
    })
    try:
        with request.urlopen(req) as response:
            page = str(response.read())
    except error.HTTPError as err:
        print(err.__dict__)
    return page


def extract_llvm_release_versions_and_links(html_document: str) -> typing.Dict[str, str]:
    """

    html_document: str
    returns dict[version: str, uri: str]

    Takes the LLVM releases GitHub HTML page as a string, parses the page to extract released LLVM versions and their cognate
    download URIs and returns them paired in a dictionary.
    Requires BeautifulSoup for parsing the HTML document.

    Note that this function is delicate and prone to breaks as it depends on very intricate structural details of the HTML document.
    Any small changes in the structure of the HTML document could potentially break the parsing logic. (If GitHub decides to change their page 
    structures)

    """

    if not isinstance(html_document, str):
        raise TypeError(
            "Incompatible types. Argument must be of string <class 'str'> type.")

    links: typing.Dict[str, str] = {}

    soup = BeautifulSoup(html_document, "html.parser")

    for section in soup.find_all("section"):
        version = section.find("h2", attrs={"class": "sr-only"}).text
        include_fragment = section.find(
            "include-fragment", attrs={"loading": "lazy"})

        if include_fragment:
            links[version] = include_fragment.get("src")

        else:
            lazy_load = section.find(
                "include-fragment", attrs={"class": "js-truncated-assets-fragment"})
            links[version] = lazy_load.get("data-deferred-src")
    return links


class Win64FetcherThread(threading.Thread):

    """

    A class that extends the threading.Thread class.
    Upon instantiation, requires a 
    link: str - URI to the web page of a specific LLVM release version.
    regex: typing.Pattern[str] - a compiled regex pattern to match the download URI of the downloadable win64 executable.

    the .run() method (invoked implicitly when calling thread.start()) sends a HTTP GET request to the specified URI,
    receives, parses the response body to extract the download URI.
    This URI is stored in the .result attribute.
    If a specific LLVM release hasn't provided a downloadable win64 executable, the .result attribute will be "None".

    """

    def __init__(self, link: str, regex: typing.Pattern[str]) -> None:
        """

        link: str - URI to the web page of a specific LLVM release version.
        regex: typing.Pattern[str] - a compiled regex pattern to match the download URI of the downloadable win64 executable.
        Having to compile the regex at every instantiation of this class would likely lead to performance losses.
        So, this function takes a pre-compiled regex object on initialization. (One pre-compiled regex object can be passed to instantiation
        of multiple objects, if the pattern to be matched is same for all tasks, thus removing a significant overhead.)

        """

        threading.Thread.__init__(self)
        self.link: str = link
        self.result: str = ""
        self.BASE_URL: str = "https://github.com"
        self.pattern: typing.Pattern[str] = regex

    def run(self):
        """

        The method that gets called when thread.start() is invoked.

        """

        req_custom = request.Request(url=self.link, method="GET", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "Connection": "close"
        })

        with request.urlopen(req_custom) as response:
            try:
                resp_body = str(response.read().decode("utf8"))
                download_link = re.findall(self.pattern, resp_body)
                if download_link:
                    self.result = self.BASE_URL + download_link[0]
                else:
                    self.result = "None"
            except error.HTTPError as err:
                print(err.__dict__)


def run_threads(page_links: typing.Dict[str, str]) -> typing.Dict[str, str]:
    """

    page_links: typing.Dict[str, str] - a dictionary with LLVM release versions as keys and LLVM release page URIs as values.
    returns: typing.Dict[str, str] - a dictionary with LLVM release versions as keys and win64 LLVM downloadable .exe URIs as values.

    A function that runs a set of Win64FetcherThreads in parallel.
    Spawns a new OS thread with every URI of the LLVM download page.
    Once the spawned threads finish their tasks, joins them with the main thread. (Current thread)

    """

    regex = re.compile(
        r"/llvm/llvm-project/releases/download/[\d\w\-\.\/]*win64.exe"
    )
    win64_downloads = dict.fromkeys(page_links.keys(), "")

    threads = [Win64FetcherThread(link=uri, regex=regex)
               for uri in page_links.values()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for (i, release) in enumerate(win64_downloads.keys()):
        win64_downloads[release] = threads[i].result

    return win64_downloads


def activate_virtual_terminal_escapes_win32() -> None:
    """
    A function that activates the virtual terminal escape sequences in Windows.
    Windows specific, uses a C FFI to interact with Win32 API functions.
    Uses GetStdHandle, GetConsoleMode and SetConsoleMode Win32 procedures.
    """

    # Emulating C macros.
    STD_OUTPUT_HANDLE = wintypes.DWORD(-11)
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1)
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = wintypes.DWORD(0x0004)

    # Function (re-)declarations.
    GetStdHandle = windll.kernel32.GetStdHandle
    GetStdHandle.argtypes = [wintypes.DWORD]
    GetStdHandle.restype = wintypes.HANDLE

    GetConsoleMode = windll.kernel32.GetConsoleMode
    GetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
    GetConsoleMode.restype = wintypes.BOOL

    SetConsoleMode = windll.kernel32.SetConsoleMode
    SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    SetConsoleMode.restype = wintypes.BOOL

    std_out: wintypes.HANDLE = GetStdHandle(STD_OUTPUT_HANDLE)
    if std_out == INVALID_HANDLE_VALUE:
        print(
            f"Access to standard output denied! Error: {ctypes.GetLastError()}"
        )
    else:
        dwMode = wintypes.DWORD(0)
        if GetConsoleMode(std_out, ctypes.byref(dwMode)):
            dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING.value
            if not SetConsoleMode(std_out, dwMode):
                print(
                    f"Activation of Win32 virtual terminal escapes failed. Error {ctypes.GetLastError()}"
                )


def print_results(results: typing.Dict[str, str]) -> None:
    """
    Prints the dictionary to console, taking advantage of the virtual terminal escapes to
    print keys and values in separate colours.
    """

    activate_virtual_terminal_escapes_win32()
    for (release, link) in results.items():
        print(f"\x1b[33m{release:15s}  ->  \x1b[32m{link}")
    print("\x1b[0m")


if __name__ == "__main__":
    page: str = fetch_llvm_releases_github_page()
    versions_and_page_links: typing.Dict[str, str] = extract_llvm_release_versions_and_links(page)
    versions_and_win64_uris: typing.Dict[str, str] = run_threads(versions_and_page_links)
    activate_virtual_terminal_escapes_win32()
    print_results(versions_and_win64_uris)
    sys.exit(0)