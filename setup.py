
from setuptools import setup

setup(
    name='twentyc.tmpl',
    version=open('config/VERSION').read().rstrip(),
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
    zip_safe=False
)
