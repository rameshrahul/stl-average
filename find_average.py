import skfmm
from stl import mesh

# Create a new plot
#figure = pyplot.figure()
#axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
#your_mesh = mesh.Mesh.from_file('C1_vertebra.stl')
#axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
#scale = your_mesh.points.flatten()
#print(your_mesh.points)
#axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
#pyplot.show()

# Load the STL files and add the vectors to the plot
mesh_1 = mesh.Mesh.from_file('C1_vertebra.stl')
mesh_2 = mesh.Mesh.from_file('C1 80% Scale.stl')

print (len(mesh_1), len(mesh_2))

#sdf_1 = skfmm.distance(mesh_1.points)
#sdf_2 = skfmm.distance(mesh_2.points)

print


