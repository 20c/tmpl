
from setuptools import find_packages, setup


version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
test_requirements = open('facsimile/requirements-test.txt').read().split("\n")


setup(
    name='twentyc.tmpl',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='template abstraction and helper functions',
    long_description='',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    namespace_packages=['twentyc'],
    packages=['twentyc.tmpl'],
    download_url = 'https://github.com/20c/twentyc.tmpl/archive/{}.zip'.format(version),
    include_package_data=True,
    url='https://github.com/20c/twentyc.tmpl',

    install_requires=requirements,
    test_requires=test_requirements,

    zip_safe=True
)
