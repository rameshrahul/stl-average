from mesh_to_sdf import get_surface_point_cloud, mesh_to_voxels
import trimesh
import skimage, skimage.measure
import numpy as np
from tkinter.filedialog import askopenfilenames
import math


scale_based_on_volume = True
centroid_on_bounding_box = False
    

def get_scale_factor(mesh):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()

    if scale_based_on_volume:
        return math.pow(mesh.volume, 1/3)
    else:
        vertices = mesh.vertices - mesh.centroid
        distances = np.linalg.norm(vertices, axis=1)
        return np.max(distances)

def center_and_scale(mesh, scale_factor):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()
    if centroid_on_bounding_box:
        vertices = mesh.vertices - mesh.bounding_box.centroid
    else:
        vertices = mesh.vertices - mesh.centroid
    new_mesh = trimesh.Trimesh(vertices=vertices, faces=mesh.faces)
    new_mesh.apply_scale(scale_factor)
    return new_mesh

def remove_extraneous_surfaces(mesh):
    meshes = trimesh.graph.split(mesh)
    if len(meshes) == 0:
        return mesh
    max_vol = 0
    max_mesh = None
    for mesh in meshes:
        if mesh.volume > max_vol:
            max_mesh = mesh
            max_vol = mesh.volume
    return max_mesh

# method in case certain meshes need to be rotated, flipped, etc.
def apply_adjustment(mesh, file):
    if 'cbi_skull' in file:
        mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, trimesh.transformations.rotation_matrix(180*math.pi/180, [0, 0, 1]))
    
    if 'Heel 3adsfasdfsa' in file:
        reflection_mat = trimesh.transformations.reflection_matrix([0, 0, 0], [1, 0, 0])
        mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, reflection_mat)
        
        
    if 'Orientation' in file:
        rotation_mat_1 = trimesh.transformations.rotation_matrix(-72*math.pi/180, [1, 0, 0])
        rotation_mat_2 = trimesh.transformations.rotation_matrix(-20*math.pi/180, [0, 0, 1])
        mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, rotation_mat_1)
        mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, rotation_mat_2)
        
    if 'Right Ear 1' in file:
        reflection_mat = trimesh.transformations.rotation_matrix(-45*math.pi/180, [0, 1, 0])
        mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, reflection_mat)
        mesh.export('right ear reflection.stl')
        
    
voxel_resolution = 100

#inputs = ['bones/Bone1.stl', 'bones/Bone2.stl', 'bones/Bone3.stl', 'bones/Bone4.stl', 'bones/Bone5.stl']
#inputs = ['bones/Bone1.stl']
#inputs = ['spheres/20 mm sphere.stl', 'spheres/30 mm sphere.stl']
#inputs = askopenfilenames()
#inputs = ['skulls/Half Skull 1.stl', 'skulls/Half Skull 3.stl']
#inputs = ['skulls/CT Cleaned.stl', 'skulls/wfu_cbi_skull-clean.stl', 'skulls/Half Skull 1.stl']
#inputs = ['vertebrae/c1.stl', 'vertebrae/c1_80.stl']
#inputs = ['heels/Heel 1.stl', 'heels/Heel 2.stl', 'heels/Out of Orientation Heel.stl', 'heels/Heel 3.stl', 'heels/Diseased Heel.stl']
#inputs = ['heels/Heel 1.stl', 'heels/Heel 2.stl', 'heels/Heel 3.stl']
#inputs = ['spines/trent_spine.stl', 'spines/double_cut_spine.stl']
inputs = ['inputs/cubes/Test Cube 50 mm.stl', 'inputs/cubes/25 mm cube.stl', 'inputs/cubes/Test Cube 15mm.stl']
#inputs = ['cubes/Test Cube 50 mm.stl', 'cubes/25 mm cube.stl']
#inputs = ['curved_bodies/Curved solid 1.stl', 'curved_bodies/Curved solid 2.stl']
#inputs = ['ears/Right Ear 1.stl', 'ears/Right Ear 2.stl', 'ears/Right Ear 3.stl', 'ears/Right Ear 4.stl',]
#inputs = ['ears/Right Ear 2.stl', 'ears/Right Ear 3.stl', 'ears/Right Ear 1.stl']
#inputs = ['cylinders/cyl_45.stl', 'cylinders/cyl_50.stl', 'cylinders/cyl_55.stl']
weights = []
#weights = [.66, .34]
#weights = [.22, .22, .22, .22, .12]
#weights = [.45, .45, .1]

if len(weights) == 0:
    weights = [1/len(inputs) for x in inputs]
    

if len(inputs) != len(weights):
    print("error, length of weights doesn't match length of inputs")
    exit(0)
    


def main ():
    scale_factors = []
    
    output_file_name = "outputs/average_cube_new_output.stl"
    
    mesh_list = []
    
    for file in inputs:
        mesh = trimesh.load(file)
        mesh.convert_units('mm', guess=True)
        mesh.apply_scale(1/25.4)
        scale_factors.append(get_scale_factor(mesh))
        
        apply_adjustment(mesh, file)
        mesh_list.append(mesh)
        
    max_transform = 1/max(scale_factors)
    avg_inverse_transform = len(scale_factors)/ (sum([1/x for x in scale_factors]))
    
    
    print("transforms", scale_factors)
    print("avg inverse trasnform:", avg_inverse_transform)
    
    voxels_list = []
    for mesh in mesh_list:
        print("volume before voxelizing, before scaling: {}".format(mesh.volume))
        mesh = center_and_scale(mesh, max_transform)
        print("volume before voxelizing, after scaling: {}".format(mesh.volume))
        #cloud = get_surface_point_cloud(mesh, surface_point_method='scan',scan_count=100, scan_resolution=400, sample_point_count=10000000) #scan_count=20, scan_resolution=400)
        #voxels = cloud.get_voxels(128, use_depth_buffer=True) #normal voxel resolution: 128
        voxels = mesh_to_voxels(mesh, voxel_resolution, pad=True)
        voxels_list.append(voxels)
        
    voxels_avg = 0
    
    for x in range(len(voxels_list)):
        voxels = voxels_list[x]
        voxels_avg += weights[x] * voxels
        
    
    
    print("Creating a mesh using Marching Cubes...")
    vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels_avg, level=0, step_size=1, 
                                                                         allow_degenerate=False)
    
    
    average_mesh_trimesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
    average_mesh_trimesh.convert_units('mm', guess=True)
    
    
    average_mesh_trimesh = remove_extraneous_surfaces(average_mesh_trimesh)
    
    
    
    #apply the inverse average trasnformatino from each object
    average_mesh_trimesh = center_and_scale(average_mesh_trimesh, 1/get_scale_factor(average_mesh_trimesh))
    print(average_mesh_trimesh.volume)
    average_mesh_trimesh.apply_scale(avg_inverse_transform)  
        
    print("volume after averaging and scaling: {}".format(average_mesh_trimesh.volume))
    
    #scale by taking the average of the inverse transforms of each object
    
    
    #average_mesh_trimesh.apply_scale(1/voxel_resolution)
    #average_mesh_trimesh = center_and_scale(average_mesh_trimesh, 1/max_transform)
    
    #average_mesh_trimesh = center_and_scale(average_mesh_trimesh, 1/max_transform / get_scale_factor(average_mesh_trimesh))
    #average_mesh_trimesh.apply_scale(1/max_transform / get_scale_factor(average_mesh_trimesh))
    
    
    
    #print("Saving to file")
    average_mesh_trimesh.export(output_file_name)
    
    
    print("finished")

if __name__ == "__main__":
    main()
