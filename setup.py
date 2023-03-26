from setuptools import setup, find_packages

setup(
    name="makedo",
    version="0.1.0",
    description="Diagnostic message parser",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Morten Hustveit",
    author_email="morten.hustveit@gmail.com",
    url="https://github.com/mortehu/makedo",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "makedo = makedo.makedo:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
