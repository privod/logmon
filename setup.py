from setuptools import setup, find_packages
from os.path import join, dirname
import logmonitor

setup(
    name='logmonitor',
    version=logmonitor.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    install_requires=[
        'watchdog'
    ],

    entry_points={
        'console_scripts':
            ['logmonitor = logmonitor.core:main']
    },
    include_package_data=True,
    test_suite='tests',
)
