#!/usr/bin/python3

from threading import Thread
import requests
import json
import os
import sys
from .config import Config
from . import utils


CONFIG = Config.getConfig()


def getLangExtMapping():
    """
    Returns Languages-File_Extensions mapping from my Resources Repo
    """
    try:
        res = requests.get(CONFIG["LANG_MAP_URL"])
        mappingJson = json.loads(res.text)
        return mappingJson
    except Exception as e:
        print(e)
        sys.stderr.write("[-] An error occurred while fetching language mapping")
        sys.exit(1)


def getFilteredMapping(langList, langExtMapping):
    filteredMapping = {}
    for lang in langList:
        extensions = []
        for key, value in langExtMapping.items():
            if value.lower() == lang.lower():
                extensions.append(key)
        if len(extensions) != 0:
            filteredMapping[lang] = extensions

    with open(CONFIG["APP_PATH"] + "langs.json", "w") as file:
        json.dump(filteredMapping, file)
    return filteredMapping


def refineData(data):
    data = data.split("\n")
    refinedData = ""
    for line in data:
        if line and line.strip()[:1] != "#":
            refinedData += (line.strip() + '\n')
    return refinedData


def updateGitignoreFile(lang):
    """
    Fetch gitignore files from github/gitignore for the given language
    """
    try:
        langPath = CONFIG["APP_PATH"] + lang + '.gitignore'
        res = requests.get(CONFIG["GITIGNORE_BASE_URL"] % lang)
        data = refineData(res.text)
        with open(langPath, "w") as gigFile:
            gigFile.write(data)
            print("[+] Updated %s.gitignore" % lang)
    except:
        print("[-] Update Unsuccessful .... %s.gitignore" % lang)


def main():
    langList = utils.getGitIgnoreLanguages()
    try:
        os.makedirs(CONFIG["APP_PATH"])
        print("[*] Creating gIgnore ... This might take a while")
    except:
        print("[*] Updating gIgnore")

    langExtMapping = getLangExtMapping()
    filteredMapping = getFilteredMapping(langList, langExtMapping)

    for lang, exts in filteredMapping.items():
        thread = Thread(target=updateGitignoreFile, args=(lang,))
        thread.start()
        thread.join()


if __name__ == "__main__":
    main()
