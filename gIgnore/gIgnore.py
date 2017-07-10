#!/usr/bin/python3

import os
import json
import fnmatch
import argparse
from . import initScript
from . import utils
from .config import Config


CONFIG = Config.getConfig()
APP_PATH = CONFIG["APP_PATH"]


def removeDuplicate(saved):
    """
    Remove duplicate file matchings from gitignore files
    """
    seen = []
    with open(".gitignore", "r") as gitIgn:
        for file in gitIgn.read().split('\n'):
            if file not in seen:
                seen.append(file)
    with open(".gitignore", "w") as gitIgn:
        for file in seen:
            gitIgn.write(file + '\n')
        gitIgn.write(saved)


def refineGitignore(contents, files):
    """
    Ignore only those files which are present in the repository
    """
    refinedContents = ""
    for exp in contents.split('\n'):
        for file in files:
            if fnmatch.fnmatch(file, exp):
                refinedContents += exp + '\n'
                break
    return refinedContents


def saveUserDefinedIgnores():
    """
    User can add their own ignores that won't be wiped out during the
    updation of gitignore by adding a comment(#) before ignores at the
    end of the file.
    """
    try:
        with open(".gitignore", "r") as gitIgn:
            userIgn = gitIgn.read().split("#")[1]
        return "#" + userIgn
    except:
        return ""


def createGitignore(gitIgnoreLangs, files):
    """
    Creates or updates gitignores for the current repository structure
    """
    saved = saveUserDefinedIgnores()
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
    removeDuplicate(saved)


def getLangs(files):
    """
    Returns a python list of gIgnore supported languages used in the repo
    """
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


def handleGitignore():
    allFiles, allDirs = utils.traverseDirectory(os.getcwd())
    gitIgnoreLangs = getLangs(allFiles)
    data = allDirs + allFiles
    createGitignore(gitIgnoreLangs, data)
    print("[*] Updated gitignore successfully")


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--update",
                        help="Update gitignores for gIgnore",
                        action="store_true"
                        )
    parser.add_argument("-s",
                        "--supports",
                        help="Prints supported languages ...",
                        action="store_true"
                        )
    parser.add_argument("-i",
                        "--langIgnore",
                        help="To view standard ignores for the given language",
                        )
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()
    try:
        os.stat(APP_PATH + "langs.json")
    except:
        print("[*] Initializing gIgnore ...")
        initScript.main()

    if args.update:
        initScript.main()
    elif args.supports:
        utils.showSupportedLangs()
    elif args.langIgnore:
        utils.showLangIgnores(args.langIgnore)
    else:
        handleGitignore()


if __name__ == "__main__":
    main()
