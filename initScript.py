#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json
import os

GITIGNORE_URL = "https://github.com/github/gitignore"
APP_PATH = os.environ['HOME'] + "/.gIgnore/"
LANG_MAP_URL = "https://raw.githubusercontent.com/fristonio/Resources/master/lang-ext.json"
BASE_URL = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"


def getGitIgnoreLanguages():
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
    res = requests.get(LANG_MAP_URL)
    data = res.text
    with open(APP_PATH + "lang-ext.json", "w") as file:
        file.write(data)
        file.close()


def refineData(data):
    data = data.split("\n")
    refinedData = ""
    for line in data:
        if line and line.strip()[:1] != "#":
            refinedData += line.strip()
    return refinedData


if __name__ == "__main__":
    langList = getGitIgnoreLanguages()
    langExtMapping = {}
    try:
        os.makedirs(APP_PATH)
    except:
        print("[-] Home directory exists")
    getLangExtMapping()
    with open(APP_PATH + "lang-ext.json", "r") as file:
        langJSON = json.load(file)
        for lang in langList:
            extensions = []
            for key, value in langJSON.items():
                if value.lower() == lang.lower():
                    extensions.append(key)
            if len(extensions) != 0:
                langExtMapping[lang] = extensions

    with open(APP_PATH + "langs.json", "w") as file:
        json.dump(langExtMapping, file)

    with open(APP_PATH + "langs.json", "r") as file:
        langJson = json.load(file)
        for lang, exts in langJson.items():
            try:
                langPath = APP_PATH + lang + '.gitignore'
                res = requests.get(BASE_URL % lang)
                data = refineData(res.text)
                with open(langPath, "w") as gigFile:
                    gigFile.write(data)
                    print("[+] Updated %s.gitignore" % lang)

            except:
                print("[-] File Already Exist")
