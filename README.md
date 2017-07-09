# gIgnore
> gIgnore is a automatic gitignore generator tool for git repositories.

### Installation

* Clone the repo to your local system using `git clone https://github.com/fristonio/g-Ignore.git` and navigate to it.

* Install the package using pip `sudo pip install .`

* The installation itself sets required **$PATH** variables and command `gign` can be used to run package.

### Usage

`gign [-h] [-u] [-s] [-i langIgnore]`

Optional Arguments:

  * **-h, --help**            show this help message and exit
  * **-u, --update**          Update github/gitignores for gIgnore
  * **-s, --supports**        Prints supported languages ...
  * **-i [Language]** 		  To view standard ignores for the given language

 If no argument is provided then app will run in default mode and create/update the .gitignore 

### To-Do

* Add supports for framworks specific ignores.
* Add supports for text-editors specific ignores.

### Dependencies

* [Python requests](https://pypi.python.org/pypi/requests)
* [Python BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4)

### License

[MIT License](https://github.com/fristonio/g-Ignore/blob/master/LICENSE.md)
