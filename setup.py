import codecs
import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(this_dir, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()

about = {}
with open(os.path.join(this_dir, 'uberfare', '__version__.py')) as f:
        exec(f.read(), about)

setup(
    name='uberfare',
    version=about['__version__'],
    description='A simple tool for periodically collecting Uber fares.',
    long_description=long_description,
    author='Kevin Lloyd Bernal',
    author_email='kevinlloydbernal@gmail.com',
    url='https://github.com/BurnzZ/uberfare',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    py_modules=['uberfare'],
    install_requires=[
        'Click',
        'uber-rides'
    ],
    entry_points={
        'console_scripts': ['uberfare=uberfare:cli']
    },
    classifiers={
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development'
    }
)
