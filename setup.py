from setuptools import setup, find_packages

package_data = {
    'gites.subpackage': ['package_setup.json'],
}

setup(
    name='gites',
    version='0.4.5',
    description='gites is the home of all developers. It provides bulk clone, bulk push, bulk pull etc functions. Contact me with my discord ID: pakkin.lau',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pak Kin LAU',
    author_email='kinlau529@gmail.com',
    url='https://github.com/pakkinlau/gites',
    packages=find_packages(),
    package_data = package_data,
    include_package_data= True,  
    # ["."] or find_package(): Include all packages under the current directory 
    # before: find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gites=gites.cli:main", 
            # gites: the key is the keyword you will use to invoke the package from the command line. 
            # gites.cli: this refer to the module where the entry point function is location. 
            # cli_lpush: this is the name of function within the module that will be executed when you run gites.
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)