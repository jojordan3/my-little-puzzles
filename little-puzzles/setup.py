'''
Package setup/installation and metadata for my-little-puzzles
'''

import setuptools

REQUIRED = [
    'numpy'
]

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='little-puzzles',
    version='0.0.1',
    author='jojordan3',
    description='A collection of fun little number puzzles.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/jojordan3/my-little-puzzles/tree/master/\
         little-puzzles',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=REQUIRED,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
