from setuptools import find_packages, setup


def version():
    """Return current package version."""
    with open("multifile_reader/version/A-major", "rt") as f:
        major = f.read().replace("\n", "")
    with open("multifile_reader/version/B-minor", "rt") as f:
        minor = f.read().replace("\n", "")
    with open("multifile_reader/version/C-patch", "rt") as f:
        patch = f.read().replace("\n", "")

    return "{}.{}.{}".format(major, minor, patch)


setup(
    name="multifile-reader",
    version=version(),
    packages=find_packages(exclude=["tests"]),
    url="",
    license="MIT",
    author="Altonotch",
    author_email="info@altonotch.com",
    description="File-like object that allows to read multiple files "
    "as if they are one",
    package_data={"multifile_reader": ["version/*"]},
    install_requires=["requests>=2.23.0", ],
    tests_require=["pytest>=5.4", "tox>=3.14.5", ],
)
