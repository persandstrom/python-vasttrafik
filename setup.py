""" Setup for vtjp """

from setuptools import setup

setup(
    name='vtjp',
    version='0.1.1',
    description='Västtrafik API.',
    long_description='Python implementation of Västtrafik Journy planner'
                     '(vtjp) public API.',
    url='https://github.com/persandstrom/python-vasttrafik',
    author='Per Sandström',
    author_email='per.j.sandstrom@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='vasttrafik västtrafik',
    install_requires=['requests>=2.9.1', 'tabulate>=0.7.5'],
    packages=['vasttrafik'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'vtjp=vasttrafik.__main__:main',
        ]
    })
