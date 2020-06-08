import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hithwen", # Replace with your own username
    version="0.0.1",
    author="Hithwen",
    author_email="hithwen@example.com",
    description="GPG clipboard tools",
    long_description="It lets you encript and decript messages directly out/to the clipboard",
    long_description_content_type="text/markdown",
    url="https://github.com/hithwen/gpg_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.7',
)