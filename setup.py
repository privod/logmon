from setuptools import setup, find_packages
from os.path import join, dirname
import logmon

setup(
    name='logmon',
    version=logmon.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    install_requires=[
        'watchdog',
        'progressbar2',
        'PyQt5',
    ],

    entry_points={
        'console_scripts': [
            'logmon-start = logmon.monitor:logmon_start',
            'logmon-path = logmon.monitor:logmon_path',
        ]
    },
    include_package_data=True,
    test_suite='tests',
)
