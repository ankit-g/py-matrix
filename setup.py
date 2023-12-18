from setuptools import setup

setup(
    name='pyneorain',
    version='2.1.1',
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
    url='https://github.com/ankit-g/py-matrix',
)
