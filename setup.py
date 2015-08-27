from distutils.core import setup

setup(name = "pysplatoon",
      version = "0.0.1",
      description = "Python client library to get Splatoon data",
      author = "Mitsuhiro Setoguchi",
      author_email = "setomits@gmail.com",
      packages = ["splatoon"],
      install_requires = ["cssselect", "lxml", "pyquery", "requests"])
