#!/usr/bin/env python

from distutils.core import setup


setup(
    name="django-extdirect-rpc",
    version="0.2.0",
    description="A simple Ext.Direct server stack implementation for Django",
    long_description="",
    author="Obraztsov Ilia, Max Vyaznikov",
    author_email="ilia.obraztsov@gmail.com,vmn@siterra.org",
    license="Apache 2.0",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['extdirectrpc'],
    zip_safe = False,
    install_requires=['Django>=1.0'],
    package_data={'jsonrpc': ['']}
 )
