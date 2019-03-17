import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "avlpy",
	version = "0.1",
	author ="Kevin Course",
	author_email = "kevin.course@mail.utoronto.ca",
	description="A high-level avl wrapper in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coursekevin/avlpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)