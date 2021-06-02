
from setuptools import setup


setup(
   name='find_stl_average',
   version='1.0',
   description='A useful module',
   license="MIT",
   author='Rahul Ramesh, Trent Lau',
   author_email='rahulrameshaz@gmail.com',
   packages=['find_stl_average'],  #same as name
   install_requires=['trimesh', 'mesh_to_sdf', 'numpy',
                     'skimage'], #external packages as dependencies
)
