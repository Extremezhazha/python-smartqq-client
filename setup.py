from setuptools import setup

version = "0.2.5"
setup(
    name="python-smartqq-client",
    version=version,
    description="A simple smartqq client implemented with python to be used as component in other projects",
    author="Extremezhazha",
    author_email="extremezhazha@gmail.com",
    license="MIT",
    keywords="python smartqq",
    install_requires=["requests", "pymongo"],
    packages=["pyclient"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ]
)
