import os
import json


APP_PATH = os.environ['HOME'] + "/.gIgnore/"


def showSupportedLangs():
    """
    Prints the supported languages by gIgnore
    """
    print("[+] Supported languages are :  \n")
    with open(APP_PATH + "langs.json", "r") as langs:
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
        path = APP_PATH + query + ".gitignore"
        print("[+] Ignore for %s are :\n" % query)
        with open(path, "r") as gitignore:
            ignores = gitignore.read()
            print(ignores)
    except:
        print("[-] Language reuqested not found")
