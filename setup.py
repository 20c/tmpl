
from setuptools import find_packages, setup


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()


long_description = read_file("README.md")
version = read_file("facsimile/VERSION")
requirements = read_file("facsimile/requirements.txt").split('\n')
test_requirements = read_file("facsimile/requirements-test.txt").split('\n')


setup(
    name='tmpl',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='template abstraction and helper functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    packages=find_packages(),
    download_url = 'https://github.com/20c/twentyc.tmpl/archive/{}.zip'.format(version),
    include_package_data=True,
    url='https://github.com/20c/twentyc.tmpl',

    install_requires=requirements,
    test_requires=test_requirements,

    zip_safe=True
)
