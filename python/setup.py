from distutils.core import setup

setup(
    name='DaTtSs',
    version='0.1.0',
    author='Stanislas Polu',
    author_email='polu.stanislas@gmail.com',
    packages=['dattss'],
    url='http://dattss.com',
    license='LICENSE.txt',
    description='DaTtSs Python Driver',
    long_description=open('README.txt').read(),
    install_requires=[
      "pycurl"
      ],
)
