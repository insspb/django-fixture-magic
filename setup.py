from setuptools import setup, find_packages


setup(
    name='django-fixture-magic',
    version='0.1.5',
    description='A few extra management tools to handle fixtures.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Dave Dash',
    author_email='dd+pypi@davedash.com',
    url='http://github.com/davedash/django-fixture-magic',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0'
        'Framework :: Django :: 3.1'
        'Framework :: Django :: 3.2'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
