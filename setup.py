#!/usr/bin/env python
from setuptools import setup, find_packages


dev_requires = [
    'Sphinx==1.2.2',
]

tests_requires = [
    'mock>=1.0.1',
]


install_requires = [
    'waldur-core>=0.151.0',
]


setup(
    name='waldur-auth-social',
    version='0.7.6',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://waldur.com',
    description='Waldur plugin for authentication with social networks such as Facebook, Google Plus.',
    long_description=open('README.rst').read(),
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=install_requires,
    zip_safe=False,
    extras_require={
        'test': tests_requires,
        'dev': dev_requires,
    },
    entry_points={
        'waldur_extensions': (
            'waldur_auth_social = waldur_auth_social.extension:AuthSocialExtension',
        ),
    },
    tests_require=tests_requires,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
