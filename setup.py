from setuptools import setup

setup(name="gIgnore",
      version="0.1",
      description="A python utility to create gitignore for git repos",
      url="http://github.com/fristonio/g-Ignore",
      author="Deepesh Pathak",
      packages=['gIgnore'],
      install_requires=[
                        'requests',
                        'bs4'
                        ],
      entry_points={
          'console_scripts': [
              'gign = gIgnore.gIgnore:main'
          ],
      })
