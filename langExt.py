import requests

URL = "https://raw.githubusercontent.com/blakeembrey/node-language-detect/master/vendor/extensions.json"

if __name__ == "__main__":
    res = requests.get(URL)
    data = res.text
    with open("language.json", "w") as file:
        file.write(data)
        file.close()
