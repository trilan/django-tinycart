import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name = 'django-tinycart',
    version = '0.1.dev',
    url = 'https://github.com/trilan/django-tinycart',
    license = 'BSD',
    description = 'Just a shopping cart for your Django projects.',
    long_description = read('README.rst'),
    author = 'Mike Yumatov',
    author_email = 'mike@yumatov.com',
    packages = find_packages(),
    test_suite = 'tests.main',
)
