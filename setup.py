import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Game",
    version="1.1.1",
    author="Gantulga G",
    author_email="limited.tulgaa@gmail.com>",
    description="Pygame base class for ease of use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gantulga9480/Game",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['pygame'],
)
