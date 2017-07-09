import os


class Config:
    __CONFIG = {
        "APP_PATH": os.environ['HOME'] + "/.gIgnore/",
        "GITIGNORE_URL": "https://github.com/github/gitignore",
        "LANG_MAP_URL": "https://raw.githubusercontent.com/fristonio/Resources/master/lang-ext.json",
        "GITIGNORE_BASE_URL": "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"
    }

    def getConfig():
        return Config.__CONFIG
