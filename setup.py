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
    description='A Python client for the Ex Libris Alma web services API',
    long_description=long_description,
    url='https://github.com/andyhartland/alma-py',
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