import sys
from setuptools import setup, find_packages

setup(
    name='gifparse',
    version='0.0.1',
    description="[Work in progress.] Parse the GIF 89a file format, down to the minor details. Pure Python, no dependencies.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3'
    ],
    keywords='gif gifs 89a',
    author='Jeremy Singer-Vine',
    author_email='jsvine@gmail.com',
    url='http://github.com/jsvine/gifparse/',
    license='MIT',
    packages=find_packages(exclude=['test',]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    test_suite='test',
)
