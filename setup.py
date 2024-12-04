import os
from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirement_lst: List[str] = []
    file_path = os.path.join(os.getcwd(), 'requirements.txt')  # 获取绝对路径
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            ## Process each line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and '-e .'
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_lst


setup(
    name = "NetworkSecurityAnalysis",
    version = "0.0.1",
    author = "Xiaolong Song",
    author_email = "andrewsong93@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)

print(get_requirements())
