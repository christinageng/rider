from setuptools import setup, find_packages
from rider.version import version_number

setup(
    name='rider',
    version=version_number(),
    url='https://github.com/marksplk/rider',
    license='MIT',
    author='jackWang,markShao',
    author_email='jackw@splunk.com',
    description='',
    scripts=['bin/knight'],
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='any',
    keywords='splunk clustering docker',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    package_data={
        'package': [
            '*.sh',
            'Dockerfile'
        ],
    },
    install_requires=["docker-py",
                      "tabulate",
                      "colorama"]
)