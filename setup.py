from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
  
with open('./requirements.txt') as f:
    requirements = f.readlines()
    requirements = list(map(lambda r: r.strip(), requirements))
  
setup(
    name ='imgetr',
    version ='1.0.0',
    author ='Brandon Aguirre',
    author_email ='branciscodigital@gmail.com',
    url ='https://github.com/brancisco/imgetr',
    description ='Command line tool for downloading images from web page.',
    long_description = long_description,
    long_description_content_type ="text/markdown",
    license ='GNU GENERAL PUBLIC LICENSE',
    packages = find_packages(),
    entry_points ={
        'console_scripts': [
            'imgetr = imgetr.imgetr:main'
        ]
    },
    classifiers =(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords ='command line scrape python package imgetr img image download',
    install_requires = requirements,
    zip_safe = False
)