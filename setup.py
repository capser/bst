from setuptools import find_packages, setup

with open("README.md", "r") as longdesc:
    long_description = longdesc.read()

setup(name="bst",
      description="This package implements ordered binary trees with various O(log(n)) performance guarantees.",
      long_description=long_description,
      author="Anthony Barrett",
      version="0.1.0",
      packages=find_packages(where="bst/"),
      package_dir={"": "src"})
