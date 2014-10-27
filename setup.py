from setuptools import setup, find_packages

setup(
    name='rider',
    version="0.0.1",
    url='https://github.com/marksplk/rider',
    license='MIT',
    author='jackWang,markShao',
    author_email='jackw@splunk.com',
    description='',
    scripts=['bin/rider'],
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='linux',
    keywords='splunk clustering docker',
    packages=find_packages(exclude=['test']),
    install_requires=[]
)