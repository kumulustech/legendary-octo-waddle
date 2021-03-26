import pathlib
from setuptools import setup, find_packages

"""Setuptools setup.py for rollback
"""

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="rollback",
    version="0.1.0",
    description="A k8s rollback agent for Prometheus/Alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kumulustech/rollback",
    author="Robert Starmer",
    author_email="robert@kumul.us",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Operators",
        "Topic :: Kubernetes Operations :: Alert Webhooks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="kubernetes,rollback,prometheus,alerts,webhook",
    package_dir={"": "rollback"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[
        "click",
        "Flask",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "Werkzeug",
        "gunicorn",
    ],
    extras_require={
        "dev": ["yapf", "black"],
        "test": ["tox", "pytest"],
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/kumulustech/rollback/issues",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/kumulustech/rollback/",
    },
)
