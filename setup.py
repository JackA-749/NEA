'''
SETUP FILE BUILT USING PYBIND11 DOCS
Compile working for Windows and Linux
'''

import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

compiler_flags = [] # create an empty list so that the specific flags for each system can be added

try:
    if sys.platform == 'win32': # if running windows
        compiler_flags = ['/O2', '/std:c++14'] # Windows MSVC flags, /O2 for optimization and /std:c++14 for C++14 standard
    elif sys.platform in ('linux', 'linux2', 'darwin'): # if running Linux or macOS
        compiler_flags = ['-O3', '-std=c++14', '-fvisibility=hidden'] # Linux/macOS flags, -O3 for optimization, -std=c++14 for C++14 standard, and -fvisibility=hidden to hide symbols

except Exception as error: # if system cannot be found
    print(f"Error determining platform or setting compiler flags: {error}")
    sys.exit(1) # Exit with an error code

# Define the Module using pybind11
ext_modules = [
    Pybind11Extension(
        "integrator",  # Module name
        ["integrator.cpp"],  # Source file
        extra_compile_args=compiler_flags, # Add the appropriate compiler flags based on the platform
        language='c++', # Specify the language to ensure correct compilation
    ),
]

setup(
    name="integrator",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,  # Important for platform-specific wheels
)