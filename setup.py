from setuptools import setup, find_packages

setup(
    name="got-search",
    version="0.0.1",
    packages=find_packages(exclude=("tests*",)),
    author="lidatong",
    author_email="charles.dt.li@gmail.com",
    description="Search for GoT episodes",
    url="https://github.com/lidatong/got-search",
    license="Unlicense",
    keywords="GoT game of thrones search",
    install_requires=[
        "gensim==3.4.0",
        "spacy==2.0.11",
        "numpy==1.14.2",
        "scipy==1.0.1",
        "scikit-learn==0.19.1",
        "requests==2.18.4",
        "flask==0.12.2",
        "dataclasses==0.5",
        "psycopg2==2.7.4"
    ],
    python_requires=">=3.6",
    extras_require={
        "dev": ["pytest", "jupyterlab", "ipython"]
    },
    entry_points={
        'console_scripts': [
            'crawl = got_search.search.crawler:main',
            'index = got_search.search.index:main',
            'query = got_search.search.query:main'
        ]
    },
    include_package_data=True
)
