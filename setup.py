from setuptools import setup

__version__ = '0.22'

setup(
    name='eulerian-magnification',
    version=__version__,
    author='Bryce Drennan',
    author_email='eulerian-magnify@brycedrennan.com',
    url='https://github.com/brycedrennan/eulerian-magnification',
    download_url='https://github.com/brycedrennan/eulerian-magnification/tarball/' + __version__,
    keywords=['eulerian magnification', 'opencv', 'motion amplification', 'video'],
    packages=['eulerian_magnification'],
    license='MIT',
    description='Amplify tiny movements in video.',
    long_description='Amplify tiny movements in video.',
    install_requires=['numpy>=1.11.0', 'requests>=2.10.0', 'scipy>=0.17.0', 'matplotlib'],
)
