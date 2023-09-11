from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name="ticket-control",
    version="0.0.2",
    description="BVG Ticket control LeWagon Project",
    install_requires=requirements[:-1],
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
)
