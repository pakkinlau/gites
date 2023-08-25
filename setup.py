from setuptools import setup, find_packages

setup(
    name='gites',
    version='0.1.0',
    description='gites is the home of all developers. It provides bulk clone, bulk push, bulk pull etc. Contact me with my discord ID: pakkin.lau',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pak Kin LAU',
    author_email='kinlau529@gmail.com',
    url='https://github.com/pakkinlau/gites',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)