
from setuptools import setup

version = open('config/VERSION').read().strip()

setup(
    name='twentyc.tmpl',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='template abstraction and helper functions',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['twentyc.tmpl'],
    namespace_packages=['twentyc'],
    download_url = 'https://github.com/20c/twentyc.tmpl/tarball/%s' % version,
    url = 'https://github.com/20c/twentyc.tmpl',
    zip_safe=False
)
