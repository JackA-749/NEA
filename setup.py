'''
SETUP FILE BUILT USING PYBIND11 DOCS
'''

from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "integrator",  # Module name
        sorted(glob("*.cpp")),  # Source files
    ),
]

setup(
    name="integrator",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)