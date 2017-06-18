#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json


if __name__ == "__main__":
    a = requests.get("https://github.com/github/gitignore")
    langList = []
    if a.status_code == 200:
        soup = BeautifulSoup(a.text, "lxml")
        spans = soup.find_all("a", attrs={"class": "js-navigation-open"})
        for span in spans:
            if "gitignore" in span.text:
                langList.append(span.text.split(".")[0])
            else:
                continue

    langExtList = []
    with open("lang-ext.json", "r") as file:
        langJSON = json.load(file)
        for lang in langList:
            extensions = []
            for key, value in langJSON.items():
                if value.lower() == lang.lower():
                    extensions.append(key)
            langExtList.append({lang: extensions})

    a = []

    for lang in langExtList:
        key, val = list(lang.keys())[0], list(lang.values())[0]
        if val:
            a.append({key: val})

    with open("gitIgnore-lang.json", "w") as file:
        json.dump(a, file)