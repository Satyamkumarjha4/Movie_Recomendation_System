from setuptools import setup, find_packages
from typing import List


EXTRA = '-e .'
def get_requirements(filepath:str)->List[str]:
    # this function will get the requirements from the requirements.txt file
    requirements = []
    with open (filepath, 'r') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

        if EXTRA in requirements:
            requirements.remove(EXTRA)

setup(
    name = 'my_package',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt'),

)