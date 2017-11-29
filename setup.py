import os
from setuptools import setup


requires = []


def get_lang_data():
    static_files = []
    root = "sumeval/metrics/lang/data/"
    for _dir in os.listdir(root):
        lang_dir = os.path.join(root, _dir)
        if not os.path.isdir(lang_dir):
            continue
        for content in os.listdir(lang_dir):
            f = os.path.join(lang_dir, content)
            if os.path.isfile(f) and not content.startswith("."):
                static_files.append(os.path.join("data/" + _dir, content))
    return static_files


setup(
    name="sumeval",
    version="0.1.1",
    description="Well tested evaluation framework for Text summarization",
    url="https://github.com/chakki-works/sumeval",
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="Apache License 2.0",
    keywords="text summarization machine learning",
    packages=[
        "sumeval",
        "sumeval.metrics",
        "sumeval.metrics.lang",
    ],
    package_data={
        "sumeval.metrics.lang": get_lang_data()
    },
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)
