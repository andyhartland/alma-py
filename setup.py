from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='alma-py',
    version='0.1.0',
    author='Digital Innovation, Lancaster University Library',
    author_email='library.dit@lancaster.ac.uk',
    description='Python tools for working with Alma Analytics data',
    long_description=long_description,
    url='https://github.com/lulibrary/alma-analytics-py',
    packages=find_packages(exclude=['docs', 'test*']),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Library Systems :: Alma :: Analytics',
        'License :: OSI Approved :: MIT Licence',
        'Programming Language :: Python :: 3'
    ],
    keywords='alma analytics obiee',
    install_requires=[
        'python-dotenv',
        'lxml',
        'requests'
    ],
    py_modules=[
        'alma'
    ]
)