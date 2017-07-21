from bs4 import BeautifulSoup
import requests
import os
import json
import re
import sys
from .config import CONFIG


def showSupportedLangs():
    """
    Prints the supported languages by gIgnore
    """
    print("[+] Supported languages are :  \n")
    with open(CONFIG["APP_PATH"] + "langs.json", "r") as langs:
        langsMapping = json.load(langs)
        i = 1
        for lang, _ in langsMapping.items():
            print("[%d]. %s" % (i, lang))
            i += 1
    print("\n[*] Currently gIgnore does not supports framworks")


def showLangIgnores(query):
    """
    Show standard ignores for requested languages
    """
    try:
        path = CONFIG["APP_PATH"] + query + ".gitignore"
        print("[+] Ignore for %s are :\n" % query)
        with open(path, "r") as gitignore:
            ignores = gitignore.read()
            print(ignores)
    except:
        print("[-] Language reuqested not found")


def getGitIgnoreLanguages():
    """
    Get Languages supported by github/gitignore
    Returns a python list storing languages names
    """
    a = requests.get(CONFIG["GITIGNORE_URL"])
    langList = []
    if a.status_code == 200:
        soup = BeautifulSoup(a.text, "lxml")
        spans = soup.find_all("a", attrs={"class": "js-navigation-open"})
        for span in spans:
            if "gitignore" in span.text:
                langList.append(span.text.split(".")[0])
            else:
                continue
    return langList


def checkIfGitRepo():
    """
    To check if the current repo is a git repo or not
    """
    files = os.listdir(os.getcwd())
    if '.git' in files:
        return True
    return False


def traverseDirectory(cwd):
    """
    Traverses current directory and returns a list of files and dirs present,
    skips hidden directories
    """
    gitRepo = checkIfGitRepo()
    allFiles = []
    allDirs = []
    if gitRepo:
        for (curDir, dirs, files) in os.walk(cwd):
            try:
                re.search(r'/(\.\w+)', curDir).group(0)
            except:
                for d in dirs:
                    allDirs.append(d + '/')
                allFiles = allFiles + files
        return allFiles, allDirs
    else:
        print("[-] Directory is not a git repository")
        sys.exit(1)


def copyFileContents(fpath1, fpath2):
    """
    Copy the content of one file whose path is provided as first argument to the
    file with path provided as second argument
    """
    if os.path.exists(fpath1):
        with open(fpath1, "r") as file:
            with open(fpath2, "w") as f:
                f.write(file.read())
        return True
    else:
        return False


def saveCurrentVersion():
    """
    Saves current state of gitignore as a version that can be restored at any point of time
    """
    savedGignPath = CONFIG["APP_PATH"] + "data/" + os.getcwd().replace('/', '|') + ".gign"
    gitignorePath = os.getcwd() + "/.gitignore"
    if copyFileContents(gitignorePath, savedGignPath):
        print("[*] Current version saved successfully")
    else:
        print("[-] No gitignore to save")


def restorePreviousVersion():
    """
    Fetches previous version of gitignores overwrittern while creating a new
    one with gIgnore.
    """
    savedGignPath = CONFIG["APP_PATH"] + "data/" + os.getcwd().replace('/', '|') + ".gign"
    gitignorePath = os.getcwd() + "/.gitignore"
    if copyFileContents(savedGignPath, gitignorePath):
        print("[*] Gitignore restored successfully")
    else:
        print("[-] No gitignore to restore")
