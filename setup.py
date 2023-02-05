from setuptools import setup

setup(
    name='pyneorain',
    version='1.0.0',
    py_modules=['pyneorain'],
    install_requires=[
        'numpy',
        'blessed',
        'six',
        'wcwidth'
    ],
    entry_points={
        'console_scripts': [
            'pyneorain = pyneorain:main'
        ]
    },
    author='Ankit Gupta',
    author_email='ankitgupta.work@gmail.com',
    license='MIT',
    description='Simple Matrix Rain',
)
