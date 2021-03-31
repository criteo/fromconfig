"""Setup script."""

from pathlib import Path
import re
import setuptools


if __name__ == "__main__":
    # Read metadata from version.py
    with Path("fromconfig/version.py").open(encoding="utf-8") as file:
        metadata = dict(re.findall(r'__([a-z]+)__\s*=\s*"([^"]+)"', file.read()))

    # Read description from README
    with Path(Path(__file__).parent, "README.md").open(encoding="utf-8") as file:
        long_description = file.read()

    # Run setup
    setuptools.setup(
        author=metadata["author"],
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Intended Audience :: Developers",
        ],
        data_files=[(".", ["requirements.txt", "README.md"])],
        dependency_links=[],
        description=long_description.split("\n")[0],
        entry_points={"console_scripts": ["fromconfig = fromconfig.cli.main:main"]},
        install_requires=["fire", "jsonnet", "omegaconf", "pyyaml"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        name="fromconfig",
        packages=setuptools.find_packages(),
        tests_require=["pytest"],
        version=metadata["version"],
    )
