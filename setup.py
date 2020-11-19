"""Setup script."""

from pathlib import Path
import re
import setuptools


if __name__ == "__main__":
    # Read metadata from version.py
    with Path("fireconfig/version.py").open(encoding="utf-8") as file:
        metadata = dict(re.findall(r'__([a-z]+)__\s*=\s*"([^"]+)"', file.read()))

    # Read description from README
    with Path(Path(__file__).parent, "README.md").open(encoding="utf-8") as file:
        long_description = file.read()

    # Run setup
    setuptools.setup(
        name="fireconfig",
        author=metadata["author"],
        version=metadata["version"],
        install_requires=[
            "fire>=0.3",
            "jsonnet>=0.15",
            "skein>=0.8",
        ],
        tests_require=["pytest"],
        dependency_links=[],
        entry_points={"console_scripts": ["fireconfig = fireconfig.main:main"]},
        data_files=[(".", ["requirements.txt", "README.md"])],
        packages=setuptools.find_packages(),
        description=long_description.split("\n")[0],
        long_description=long_description,
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Intended Audience :: Developers",
            "Development Status :: 5 - Production/Stable",
        ],
    )
