from setuptools import setup, find_packages
from setuptools.command.install import install
from panduza_platform.conf import PLATFORM_VERSION

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

setup(
    name="panduza_platform",

    version=PLATFORM_VERSION,

    author="Panduza Team",

    author_email="panduza.team@gmail.com",

    description='Panduza Python Platform',

    long_description="Panduza service that provides support to create drivers that match Panduza specifications",

    packages=find_packages(),

    cmdclass={'install': CustomInstallCommand},

    install_requires=[
        'loguru',
        'paho-mqtt',
        'pyserial',
        'pymodbus'
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ]
)
