#!/usr/bin/python3

import os
import json
import re
import fnmatch


APP_PATH = os.environ['HOME'] + "/.gIgnore/"


def removeDuplicate():
    """
    Remove duplicate file matching from gitignore files
    """
    seen = []
    with open(".gitignore", "r") as gitIgn:
        for file in gitIgn.read().split('\n'):
            if file not in seen:
                seen.append(file)
    with open(".gitignore", "w") as gitIgn:
        for file in seen:
            gitIgn.write(file + '\n')


def refineGitignore(contents, files):
    refinedContents = ""
    for exp in contents.split('\n'):
        for file in files:
            if fnmatch.fnmatch(file, exp):
                refinedContents += exp + '\n'
                break
    return refinedContents


def createGitignore(gitIgnoreLangs, files):
    with open(".gitignore", "w") as gitIgn:
        for lang in gitIgnoreLangs:
            gitignoreContent = ""
            path = APP_PATH + lang + ".gitignore"
            try:
                with open(path, "r") as f:
                    gitignoreContent += refineGitignore(f.read(), files)
                    gitIgn.write(gitignoreContent)
            except:
                pass
    removeDuplicate()


def getLangs(files):
    allExt = []
    for file in files:
        fileExt = '.' + file.split('.')[-1]
        if fileExt not in allExt:
            allExt.append(fileExt)

    gitIgnoreLangs = []
    with open(APP_PATH + "langs.json", "r") as f:
        langJson = json.load(f)
        for ext in allExt:
            for lang, exts in langJson.items():
                if ext in exts:
                    gitIgnoreLangs.append(lang)
                    break
    return gitIgnoreLangs


def checkIfGitRepo():
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
                allDirs = allDirs + dirs
                allFiles = allFiles + files
        return allFiles, allDirs
    else:
        print("[-] Directory is not a git repository") 


def main():
    allFiles, allDirs = traverseDirectory(os.getcwd())
    gitIgnoreLangs = getLangs(allFiles)
    data = allDirs + allFiles
    createGitignore(gitIgnoreLangs, data)


if __name__ == "__main__":
    try:
        os.stat(APP_PATH)
        main()
    except Exception as e:
        print(e)
