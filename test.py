import setup2 #importing the setup file for linking using pybind11

# call the setup function to build the module using pybind11
setup2.setup(
    name="integrator_with_pybind",
    version="0.1",
    ext_modules=setup2.ext_modules,
    cmdclass={"build_ext": setup2.build_ext},
)   

'''import integrator_with_pybind #import the c++ module built using pybind11

x = integrator_with_pybind.velocity_verlet([1,1], [5,0], [5,5], 10, 0.1)

print(x)

'''

print("Module built successfully!")