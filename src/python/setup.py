import os, sys

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

def main():
    setup(
        name='idb',
        description='iDB Library',
        long_description = open('README.txt').read(),
        version='0.0.1',
        url='http://pylib.org',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='Riceball LEE',
        author_email='snowyu.lee at gmail.com',
        classifiers=['Development Status :: 6 - Mature',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Database',
                     'Topic :: Software Development :: Libraries',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
        packages=['idb',
        ],
        zip_safe=False,
    )

if __name__ == '__main__':
    main()
