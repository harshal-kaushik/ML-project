from setuptools import find_packages,setup
from  typing import List
hypen_E_dot = "-e ."
def get_requirements(file_path : str)-> List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readline()
        requirements = [req.replace("\n","") for req in requirements]
        if hypen_E_dot in requirements:
            requirements.remove(hypen_E_dot)


    return requirements


setup(
name = 'mlproject',
version = '0.0.1',
author = 'Harshal',
author_email = 'kaushikharshal02@gmail.com',
install_requires = get_requirements('requirement.txt')

)