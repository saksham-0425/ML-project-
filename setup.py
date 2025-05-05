# setup.py will make this file to be donloaded or installed like we can install seaborn from pip install seaborn 

from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
    '''This function will return the list of requirements'''
    requirements = []
    with open(file_path) as file_obj:
        for line in file_obj:
            line = line.strip()
            if line and not line.startswith('-e'):
                requirements.append(line)
    return requirements

    

setup(
    name='ML Project',
    version='0.0.1',
    author='Saksham',
    author_email='guptasaksham2510@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)