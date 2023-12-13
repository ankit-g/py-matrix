from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text()

setup(
    name='pyneorain',
    version='2.0.8',
    py_modules=['pyneorain'],
    install_requires=[
        'blessed',
        'six',
        'wcwidth'
    ],
    package_data={
        'pyneorain': ['config/*.toml']
    },
    entry_points={
        'console_scripts': [
            'pyneorain = pyneorain:main'
        ]
    },
    author='Ankit Gupta',
    author_email='ankitgupta.work@gmail.com',
    license='MIT',
    description='Simple Matrix Rain Terminal Screen-Saver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ankit-g/py-matrix',
)
