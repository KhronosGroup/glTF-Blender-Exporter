# Copyright (c) 2017 The Khronos Group Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Imports
#

import bpy

from .gltf2_get import *

#
# Globals
#

#
# Functions
#

def filter_apply(export_settings):
    filtered_objects = []
    implicit_filtered_objects = []

    for blender_object in bpy.data.objects:
        if export_settings['gltf_selected'] and not blender_object.select:
            continue
        
        filtered_objects.append(blender_object)
        
        if export_settings['gltf_selected']:
            current_parent = blender_object.parent
            while current_parent:
                if current_parent not in filtered_objects and current_parent not in implicit_filtered_objects:
                    implicit_filtered_objects.append(current_parent)
                
                current_parent = current_parent.parent

    export_settings['filtered_objects'] = filtered_objects
    
    #
    
    filtered_meshes = {}
    filtered_vertex_groups = {}
    temporary_meshes = []
    
    for blender_mesh in bpy.data.meshes:
        
        current_blender_mesh = blender_mesh
        
        skip = True
        
        for blender_object in filtered_objects:
            if blender_object.type != 'MESH':
                continue
            
            if blender_object.data == current_blender_mesh:
                skip = False
                
                if export_settings['gltf_apply']:
                    current_blender_mesh = blender_object.to_mesh(bpy.context.scene, True, 'PREVIEW')
                    temporary_meshes.append(current_blender_mesh)
                
                break
        
        if skip:
            continue
            
        filtered_meshes[blender_mesh.name] = current_blender_mesh
        filtered_vertex_groups[blender_mesh.name] = blender_object.vertex_groups 
            
    export_settings['filtered_meshes'] = filtered_meshes
    export_settings['filtered_vertex_groups'] = filtered_vertex_groups
    export_settings['temporary_meshes'] = temporary_meshes
    
    #

    filtered_materials = []

    for blender_material in get_used_materials():
        for mesh_name, blender_mesh in filtered_meshes.items():
            for compare_blender_material in blender_mesh.materials:
                if compare_blender_material == blender_material and blender_material not in filtered_materials:
                    filtered_materials.append(blender_material)
                    
    export_settings['filtered_materials'] = filtered_materials                

    #

    filtered_textures = []

    for currentMaterial in filtered_materials:
        if currentMaterial.node_tree:
            for currentNode in currentMaterial.node_tree.nodes:
                if isinstance(currentNode, bpy.types.ShaderNodeTexImage) and currentNode.image is not None and currentNode not in filtered_textures:
                    filtered_textures.append(currentNode)
        else:
            for currentTextureSlot in currentMaterial.texture_slots:
                if currentTextureSlot and currentTextureSlot.texture and currentTextureSlot.texture.type == 'IMAGE' and currentTextureSlot.texture.image is not None:
                    if currentTextureSlot not in filtered_textures:
                        accept = False
                        if currentTextureSlot.use_map_color_diffuse:
                            accept = True
                        if currentTextureSlot.use_map_color_spec:
                            accept = True
                        if currentTextureSlot.use_map_hardness:
                            accept = True
                        if currentTextureSlot.use_map_ambient:
                            accept = True

                        if currentTextureSlot.use_map_emit:
                            accept = True
                        if currentTextureSlot.use_map_normal:
                            accept = True
                            
                        if accept:
                            filtered_textures.append(currentTextureSlot) 
 
    export_settings['filtered_textures'] = filtered_textures                

    #

    filtered_images = []

    for blender_texture in filtered_textures:
        if isinstance(blender_texture, bpy.types.ShaderNodeTexImage) and blender_texture.image not in filtered_images:
            filtered_images.append(blender_texture.image)
        else:
            filtered_images.append(blender_texture.texture.image)
                    
    export_settings['filtered_images'] = filtered_images                
    
    #
    #
    
    filtered_objects.extend(implicit_filtered_objects)
    
    #
    #
    #
    
    group_index = {}
    
    if export_settings['gltf_skins']:
        for blender_object in filtered_objects:
            if blender_object.type != 'ARMATURE' or len(blender_object.pose.bones) == 0:
                continue
            for blender_bone in blender_object.pose.bones:
                group_index[blender_bone.name] = len(group_index)

    export_settings['group_index'] = group_index
