#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='Card Kit',
    version='0.1.0',
    description='Simple framework for developing card games in Pygame',
    long_description="""This is a simple game framework for developing card games in
      Python, using the Pygame library. It has been tested with Python
      2.7.9 and Pygame 1.9.2a0.
    """,
    author='Owen D. Smith',
    author_email='ods94043@yahoo.com',
    url='https://github.com/ods94065/card-kit',
    packages=setuptools.find_packages(),
    package_data={'cardkit': ['img/*.png']},
    data_files=[
        ('share/doc/cardkit', ['LICENSE', 'README.md']),
    ],
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X :: Cocoa',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
