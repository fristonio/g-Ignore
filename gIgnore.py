#!/usr/bin/python3

import os
import json


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

    traverseDirectory()


if __name__ == "__main__":
    main()
