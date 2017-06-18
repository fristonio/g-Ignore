#!/usr/bin/python3

import requests
import os
import json


BASE_URL = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"
APP_PATH = os.environ['HOME'] + "/.gIgnore/"


def main():
    try:
        os.makedirs(APP_PATH)
    except:
        print("[-] Home directory exists")

    with open("gitIgnore-lang.json", "r") as file:
        langJson = json.load(file)
        for language in langJson:
            lang = list(language.keys())[0]
            try:
                langPath = APP_PATH + lang + '.gitignore'
                res = requests.get(BASE_URL % lang)
                with open(langPath, "w") as gigFile:
                    gigFile.write(res.text)
                    print("[+] Updated %s.gitignore" % lang)

            except:
                print("[-] File Already Exist")


if __name__ == "__main__":
    main()
