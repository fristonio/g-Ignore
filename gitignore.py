#!/usr/bin/python3

import requests
import os
import json


BASE_URL = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"
APP_PATH = os.environ['HOME'] + "/.gIgnore/"


def createGitignore(files):
    # Language extensions for the directory.
    allExt = []
    for file in files:
        file = file.split('.')
        fileExt = '.' + file[-1]
        if fileExt not in allExt:
            allExt.append(fileExt)
    print(allExt)

    allLangs = []
    with open("gitIgnore-lang.json", "r") as f:
        langJson = json.load(f)
        for ext in allExt:
            for lang, exts in langJson.items():
                if ext in exts:
                    allLangs.append(lang)
                    break
    print(allLangs)

    gitignoreContent = ""

    for lang in allLangs:
        path = APP_PATH + lang + ".gitignore"
        try:
            with open(path, "r") as f:
                gitignoreContent += f.read()
        except:
            pass

    print(gitignoreContent)
    with open(".gitignore", "w") as f:
        f.write(gitignoreContent)


def traverseDirectory():
    allFiles = []
    for (curDir, dirs, files) in os.walk(os.getcwd()):
        if ".git" not in curDir:
            for file in files:
                allFiles.append(curDir + '/' + file)
    print(allFiles)
    createGitignore(allFiles)


def main():
    try:
        os.makedirs(APP_PATH)
    except:
        print("[-] Home directory exists")

    with open("gitIgnore-lang.json", "r") as file:
        langJson = json.load(file)
        for lang, exts in langJson.items():
            try:
                langPath = APP_PATH + lang + '.gitignore'
                res = requests.get(BASE_URL % lang)
                with open(langPath, "w") as gigFile:
                    gigFile.write(res.text)
                    print("[+] Updated %s.gitignore" % lang)

            except:
                print("[-] File Already Exist")

    traverseDirectory()


if __name__ == "__main__":
    main()
