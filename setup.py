from setuptools import setup

setup(
    name='pymatrixrain',
    version='0.1',
    py_modules=['pymatrixrain'],
    install_requires=[
        'numpy==1.24.1',
        'blessed==1.19.1',
        'six==1.16.0',
        'wcwidth==0.2.6'
    ],
    entry_points={
        'console_scripts': [
            'pymatrixrain = pymatrixrain:main'
        ]
    },
    author='Ankit Gupta',
    author_email='ankitgupta.work@gmail.com',
    license='MIT',
    description='Simple Matrix Rain',
)
