#!/usr/bin/python3

from bs4 import BeautifulSoup
from threading import Thread
import requests
import json
import os
import sys

GITIGNORE_URL = "https://github.com/github/gitignore"
APP_PATH = os.environ['HOME'] + "/.gIgnore/"
LANG_MAP_URL = "https://raw.githubusercontent.com/fristonio/Resources/master/lang-ext.json"
GITIGNORE_BASE_URL = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"


def getGitIgnoreLanguages():
    """
    Get Languages supported by github/gitignore
    Returns a python list storing languages names
    """
    a = requests.get(GITIGNORE_URL)
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


def getLangExtMapping():
    """ Returns Languages-File_Extensions mapping from my Resources Repo"""
    try:
        res = requests.get(LANG_MAP_URL)
        mappingJson = json.loads(res.text)
        return mappingJson
    except:
        sys.stderr.write("[-] An error occurred while fetching language mapping")
        sys.exit(1)


def refineData(data):
    data = data.split("\n")
    refinedData = ""
    for line in data:
        if line and line.strip()[:1] != "#":
            refinedData += (line.strip() + '\n')
    return refinedData


def updateGitignoreFile(lang):
    """
    Fetch gitignore files from github/gitignore
    """
    try:
        langPath = APP_PATH + lang + '.gitignore'
        res = requests.get(GITIGNORE_BASE_URL % lang)
        data = refineData(res.text)
        with open(langPath, "w") as gigFile:
            gigFile.write(data)
            print("[+] Updated %s.gitignore" % lang)
    except:
        print("[-] Update Unsuccessful .... %s.gitignore" % lang)


def main():
    langList = getGitIgnoreLanguages()
    filteredMapping = {}
    try:
        os.makedirs(APP_PATH)
    except:
        print("[-] Home directory exists")
    langExtMapping = getLangExtMapping()
    for lang in langList:
        extensions = []
        for key, value in langExtMapping.items():
            if value.lower() == lang.lower():
                extensions.append(key)
        if len(extensions) != 0:
            filteredMapping[lang] = extensions

    with open(APP_PATH + "langs.json", "w") as file:
        json.dump(filteredMapping, file)

    for lang, exts in filteredMapping.items():
        thread = Thread(target=updateGitignoreFile, args=(lang,))
        thread.start()
        thread.join()


if __name__ == "__main__":
    main()
