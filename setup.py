import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ytsearch2",
    version="2.1.3",
    description="Perform YouTube video searches without the API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/joetats/youtube_search",
    author="xNykram",
    author_email="patrykladocha76@gmail.com",
    license="Unlicense license",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=["youtube-search2"],
    include_package_data=True,
    install_requires=["requests"],
)