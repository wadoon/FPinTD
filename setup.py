"""
Standard Installation file for python.
 System-wide installation with:
    python setup.py install
"""
from distutils.core import setup

setup(
    name="",
    version="0.1",
    description="",
    author="Alexander Weigl",
    author_email="weigla@fh-trier",
    url="",

    packages=[ ],
    package_dir = {'' : 'src/'},
    license="cc-by-nc-sa 3.0",

    maintainer="Heinz Schmitz",
    maintainer_email="schmitz@fh-trier.de"
)