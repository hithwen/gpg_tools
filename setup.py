import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hithwen", # Replace with your own username
    version="0.0.1",
    author="Hithwen",
    author_email="hithwen@example.com",
    description="GPG clipboard tools",
    long_description="It lets you encrypt and decrypt messages directly out/to the clipboard",
    long_description_content_type="text/markdown",
    url="https://github.com/hithwen/gpg_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyperclip'
    ],
    python_requires='>=3.7',
    entry_points={"console_scripts": ["realpython=gpgclip.__main__:main"]},
)