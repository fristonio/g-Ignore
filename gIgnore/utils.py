from bs4 import BeautifulSoup
import requests
import os
import json
import re
import sys
from .config import Config


CONFIG = Config.getConfig()


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
