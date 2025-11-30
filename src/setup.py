from setuptools import setup, find_packages

setup(
    name="icloud_api",
    version="0.1.0",
    description="A package for iCloud backup utilities.",
    author="Your Name",
    author_email="your.email@example.com",
    package_dir={"": "./"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here, e.g.:
        # "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)