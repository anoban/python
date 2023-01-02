def checkNewPythonReleases(releaseType: str = "stable") -> None:
    
    """
    A function to check the newly released of Python versions at Python.org (official Home page)
    Accepts a single argument specifying release type: default is stable release but this can be overriden by passing "pre-release"
    as releaseType.
    Uses urllib, bs4 and colorama under the hood. 
    """
    
    try:
        from urllib import request
        from bs4 import BeautifulSoup
        from colorama import Fore, just_fix_windows_console, Style     # for pretty printing
    except ImportError:
        ImportError("Error occured when importing the necessary modules!")
        
    PYTHON_HOME_WINDOWS_DOWNLOADS = "https://www.python.org/downloads/windows/"
    
    try:
        with request.urlopen(PYTHON_HOME_WINDOWS_DOWNLOADS) as connexion:
            status_code = connexion.status
            response = connexion.read()
    except request.URLError:
        request.URLError("Could not access Python Home page..")
        ConnectionRefusedError(f"Request returned status code: {status_code}")
        
    soup = BeautifulSoup(response, "html.parser")
    python_releases = soup.find_all("div", attrs = {"class" : "column"})
    
    # python_releases[0] -> stable releases
    # python_releases[1] -> pre-releases
    
    if releaseType == "stable":
        releases = python_releases[0]
    elif releaseType == "pre-release":
        releases = python_releases[1]
    
    versions, release_dates = [], []
    for release in releases.find_all("a"):
        if "Python" in release.text:
            versions.append(release.text.split("-")[0].strip())
            release_dates.append(release.text.split("-")[1].strip())
        else:
            continue
    
    # console out
    just_fix_windows_console()   # enable ANSI escape characters in Windows terminal
    print()
    print(Fore.WHITE + "-----------------------------------------")
    print(Fore.RED + "  Python version     |     Release date")
    print(Fore.WHITE + "-----------------------------------------")
    print()
    for version, rl_date in zip(versions[:15], release_dates[:15]):     # just consider the latest 10 releases
        print(f"{Fore.GREEN} {version:18}  ->  {Fore.YELLOW} {rl_date:20}", end = "\n")
        
        # print(Fore.GREEN + version + "  ->  " + Fore.YELLOW + rl_date, end = "\n")
    print(Style.RESET_ALL)
    
if __name__ == "__main__":
    import sys
    # did not do error handling since sys is stdlib
    # sys.argv[0] is the programme name (script name)
    if (len(sys.argv) == 1) or (sys.argv[1] == "stable"):
        # call the function with default params
        checkNewPythonReleases()
    elif sys.argv[1] == "pre-release":
        checkNewPythonReleases(releaseType = "pre-release")
    sys.exit()