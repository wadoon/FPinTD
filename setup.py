"""
Standard Installation file for python.
 System-wide installation with:
    python setup.py install
"""
from distutils.core import setup

__author__ = "Alexander Weigl <weigla@fh-trier.de>"
__date__   = "2012-07-21"

VERSION = "0.3"
RELEASE = "alpha"

if __name__ == "__main__":
	setup(
	    name="FPinTD",
	    license="bsd",
	    version=VERSION, 
	    description="",
	    author="Alexander Weigl",
	    author_email="weigla@fh-trier",
	    url="https://github.com/areku/FPinTD",
	    package_dir = {'' : 'src/'},
	    py_modules=["dfa","algorithms1","algorithms2","algorithms3","trap"],
	    scripts=["src/dfa_in_lc.py"],
	)
