'''
PYBIND11 SETUP FILE BUILD USING EXTERNAL TUTORIAL
'''

"""! THIS IS A PYTHON FILE TO SETUP THE BUILD SYSTEM FOR PYBIND11 !"""

from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "integrator_with_pybind",  # Module name
        ["integrator_with_pybind.cpp"],  # Source file
        include_dirs=[pybind11.get_include()],  # Include Pybind11 headers
        language="c++"  # specify c++ as module language
    )
]

setup(
    name = "integrator_with_pybind", 
    version = "0.1", 
    ext_modules=ext_modules,
)