from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-16') as f:
    requirements = f.read().splitlines()

setup(
    name="esc_simulator",
    version="1.0.0",
    description="ESC Simulator API",
    packages=find_packages(), 
    install_requires=requirements
)