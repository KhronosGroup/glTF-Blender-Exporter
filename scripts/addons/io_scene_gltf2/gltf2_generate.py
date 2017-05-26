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

import base64
import bpy

from .gltf2_animate import *
from .gltf2_calculate import *
from .gltf2_create import *
from .gltf2_debug import *
from .gltf2_extract import *
from .gltf2_filter import *
from .gltf2_get import *

#
# Globals
#

#
# Functions
#

def generate_asset(operator,
                  context,
                  export_settings,
                  glTF):
    asset = {}
    
    #
    #
    
    asset['version'] = '2.0'
    
    #
    
    asset['generator'] = 'Khronos Blender glTF 2.0 exporter'
    
    #
    
    # 'copyright'

    #
    #
        
    glTF['asset'] = asset


def generate_animations_parameter(operator,
                  context,
                  export_settings,
                  glTF,
                  action,
                  channels,
                  samplers,
                  blender_node_name,
                  blender_bone_name,
                  rotation_mode,
                  matrix_correction,
                  matrix_basis):
    name = blender_node_name
    
    prefix = ""
    postfix = ""
    
    node_type = 'NODE' 
    if blender_bone_name is not None:
        node_type = 'JOINT'

    #
        
    location = [None, None, None]
    rotation_axis_angle = [None, None, None, None]
    rotation_euler = [None, None, None]
    rotation_quaternion = [None, None, None, None]
    scale = [None, None, None]
    
    data = {
        'location' : location,
        'rotation_axis_angle' : rotation_axis_angle,
        'rotation_euler' : rotation_euler,
        'rotation_quaternion' : rotation_quaternion,
        'scale' : scale,
    }

    # Gather fcurves by transform
    for blender_fcurve in action.fcurves:
        node_name = get_node(blender_fcurve.data_path)
        
        if node_name is not None:
            if blender_bone_name is None:
                continue
            elif blender_bone_name != node_name:
                continue
            else:
                prefix = node_name + "_"
                postfix = "_"  + node_name
        
        data_path = get_data_path(blender_fcurve.data_path)
        
        if data_path not in ['location', 'rotation_axis_angle', 'rotation_euler', 'rotation_quaternion', 'scale']:
            continue
        
                    
        data[data_path][blender_fcurve.array_index] = blender_fcurve 
    
    #
    
    if location.count(None) < 3:
        
        sampler_name = prefix + action.name + "_translation"
        
        if get_index(samplers, sampler_name) == -1:
            
            sampler = {}
            
            #
            
            interpolation = animate_get_interpolation(location)
            
            sampler['interpolation'] = interpolation
            if interpolation == 'CONVERSION_NEEDED':
                sampler['interpolation'] = 'LINEAR'
            
            translation_data = animate_location(export_settings, location, interpolation, node_type, matrix_correction, matrix_basis)
            
            #
            
            keys = sorted(translation_data.keys())
            values = []
    
            for key in keys:
                value = translation_data[key]
                for value_element in value:
                    values.append(value_element)
    
            #
            
            componentType = "FLOAT"
            count = len(keys)
            type = "SCALAR"
            
            input = create_accessor(operator, context, export_settings, glTF, keys, componentType, count, type, "")
            
            sampler['input'] = input
            
            #
    
            componentType = "FLOAT"
            count = len(values) // 3
            type = "VEC3"
            
            output = create_accessor(operator, context, export_settings, glTF, values, componentType, count, type, "")
            
            sampler['output'] = output
            
            #
    
            sampler['name'] = sampler_name
            
            samplers.append(sampler)  

    #
    #
    
    rotation_data = None
    interpolation = None
    
    sampler_name = prefix + action.name + "_rotation"

    if get_index(samplers, sampler_name) == -1:
        if rotation_axis_angle.count(None) < 4:
            interpolation = animate_get_interpolation(rotation_axis_angle)
            rotation_data = animate_rotation_axis_angle(export_settings, rotation_axis_angle, interpolation, node_type, matrix_correction, matrix_basis)
        
        if rotation_euler.count(None) < 3:
            interpolation = animate_get_interpolation(rotation_euler)
            rotation_data = animate_rotation_euler(export_settings, rotation_euler, rotation_mode, interpolation, node_type, matrix_correction, matrix_basis)

        if rotation_quaternion.count(None) < 4:
            interpolation = animate_get_interpolation(rotation_quaternion)
            rotation_data = animate_rotation_quaternion(export_settings, rotation_quaternion, interpolation, node_type, matrix_correction, matrix_basis)
        
    if rotation_data is not None:
        
        #

        keys = sorted(rotation_data.keys())
        values = []

        for key in keys:
            value = rotation_data[key]
            for value_element in value:
                values.append(value_element)

        #

        sampler = {}

        #
        
        componentType = "FLOAT"
        count = len(keys)
        type = "SCALAR"
        
        input = create_accessor(operator, context, export_settings, glTF, keys, componentType, count, type, "")
        
        sampler['input'] = input
        
        #

        componentType = "FLOAT"
        count = len(values) // 4
        type = "VEC4"
        
        output = create_accessor(operator, context, export_settings, glTF, values, componentType, count, type, "")
        
        sampler['output'] = output
        
        #
        
        sampler['interpolation'] = interpolation
        if interpolation == 'CONVERSION_NEEDED':
            sampler['interpolation'] = 'LINEAR'
        
        #

        sampler['name'] = sampler_name
        
        samplers.append(sampler) 

        
    #
    #
    
    if scale.count(None) < 3:
        sampler_name = prefix + action.name + "_scale"
    
        if get_index(samplers, sampler_name) == -1:

            sampler = {}
            
            #
            
            interpolation = animate_get_interpolation(scale)

            sampler['interpolation'] = interpolation
            if interpolation == 'CONVERSION_NEEDED':
                sampler['interpolation'] = 'LINEAR'
            
            scale_data = animate_scale(export_settings, scale, interpolation, node_type, matrix_correction, matrix_basis)

            #

            keys = sorted(scale_data.keys())
            values = []
    
            for key in keys:
                value = scale_data[key]
                for value_element in value:
                    values.append(value_element)
    
            #
            
            componentType = "FLOAT"
            count = len(keys)
            type = "SCALAR"
            
            input = create_accessor(operator, context, export_settings, glTF, keys, componentType, count, type, "")
            
            sampler['input'] = input
            
            #

            componentType = "FLOAT"
            count = len(values) // 3
            type = "VEC3"
            
            output = create_accessor(operator, context, export_settings, glTF, values, componentType, count, type, "")
            
            sampler['output'] = output
            
            #

            sampler['name'] = sampler_name
            
            samplers.append(sampler)  

    #
    #
    
    write_transform = [False, False, False]
    
    # Gather fcurves by transform
    for blender_fcurve in action.fcurves:
        node_name = get_node(blender_fcurve.data_path)
        
        if node_name is not None:
            if blender_bone_name is None:
                continue
            elif blender_bone_name != node_name:
                continue
            else:
                prefix = node_name + "_"
                postfix = "_"  + node_name

        data_path = get_data_path(blender_fcurve.data_path)
        if data_path not in ['location', 'rotation_axis_angle', 'rotation_euler', 'rotation_quaternion', 'scale']:
            continue
        
        if data_path == 'location':
            write_transform[0] = True
        if data_path == 'rotation_axis_angle' or data_path == 'rotation_euler' or data_path == 'rotation_quaternion':
            write_transform[1] = True
        if data_path == 'scale':
            write_transform[2] = True

    write_transform_index = 0
    for path in ['translation', 'rotation', 'scale']:

        if write_transform[write_transform_index]:        
            channel = {}
            
            #
            
            sampler_name = prefix + action.name + "_" + path
            
            channel['sampler'] = get_index(samplers, sampler_name)
            
            #
            #
            
            target = {}
            
            target['path'] = path
            
            target_name = name + postfix 
            
            target['node'] = get_node_index(glTF, target_name)
            
            channel['target'] = target
            
            #
            # 
            
            channel['name'] = name + "_" + sampler_name
            
            # 
            
            channels.append(channel)
        
        write_transform_index += 1


#
# Property: animations
#
def generate_animations(operator,
                  context,
                  export_settings,
                  glTF):
    animations = []

    channels = []
    
    samplers = []

    #
    #
    
    filtered_objects = export_settings['filtered_objects']
    
    for blender_object in filtered_objects:
        if blender_object.animation_data is None:
            continue
        
        action = blender_object.animation_data.action
        
        #
        #
        
        matrix_correction = mathutils.Matrix.Identity(4)
        matrix_basis = mathutils.Matrix.Identity(4)
        
        generate_animations_parameter(operator, context, export_settings, glTF, action, channels, samplers, blender_object.name, None, blender_object.rotation_mode, matrix_correction, matrix_basis)
        
        if export_settings['gltf_skins']:
            if blender_object.type == 'ARMATURE' and len(blender_object.pose.bones) > 0:
                
                matrix_basis_change = mathutils.Matrix(((1.0, 0.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, -1.0, 0.0, 0.0) , (0.0, 0.0, 0.0, 1.0))) * blender_object.matrix_local

                for blender_bone in blender_object.pose.bones:
                    
                    matrix_basis = blender_bone.matrix_basis
                    
                    #
                    
                    matrix_correction = mathutils.Matrix.Identity(4)
                    
                    if blender_bone.parent is None:
                        matrix_correction = matrix_basis_change
                                    
                    matrix_correction = matrix_correction * blender_bone.bone.matrix_local
                                    
                    if blender_bone.parent is not None:
                        matrix_correction = blender_bone.parent.bone.matrix_local.inverted() * matrix_correction
                    
                    #
                    
                    generate_animations_parameter(operator, context, export_settings, glTF, action, channels, samplers, blender_object.name, blender_bone.name, blender_bone.rotation_mode, matrix_correction, matrix_basis)
        
    #
    #

    if len(channels) > 0 or len(samplers) > 0:
        animation = {
            'channels' : channels,
            'samplers' : samplers 
        }
        
        animations.append(animation)
    
    #
    #

    if len (animations) > 0:
        glTF['animations'] = animations


def generate_cameras(operator,
                  context,
                  export_settings,
                  glTF):
    cameras = []

    #
    #
    
    for blender_camera in bpy.data.cameras:

        #
        # Property: camera
        #

        camera = {}

        if blender_camera.type == 'PERSP':
            camera['type'] = 'perspective'
            
            perspective = {}
            
            #
            
            aspectRatio = 1.0
            if blender_camera.angle_y != 0.0:
                aspectRatio = blender_camera.angle_x / blender_camera.angle_y 

            perspective['aspectRatio'] = aspectRatio 
            perspective['yfov'] = blender_camera.angle_y

            perspective['znear'] = blender_camera.clip_start
            perspective['zfar'] = blender_camera.clip_end
            
            #
            
            camera['perspective'] = perspective
        elif blender_camera.type == 'ORTHO':
            camera['type'] = 'orthographic'

            orthographic = {}
            
            #    

            orthographic['xmag'] = blender_camera.ortho_scale
            orthographic['ymag'] = blender_camera.ortho_scale

            orthographic['znear'] = blender_camera.clip_start
            orthographic['zfar'] = blender_camera.clip_end
            
            # 
            
            camera['orthographic'] = orthographic
        else:
            continue
    
        #
        
        camera['name'] = blender_camera.name
        
        #
        #
        
        cameras.append(camera)

    #
    #

    if len (cameras) > 0:
        glTF['cameras'] = cameras


def generate_lights(operator,
                    context,
                    export_settings,
                    glTF):
    lights = []

    #
    #
    
    for blender_light in bpy.data.lamps:

        #
        # Property: light
        #

        light = {}
        
        light_type = {}
        
        if blender_light.type == 'SUN':
            light['type'] = 'directional' 
        elif blender_light.type == 'POINT':
            light['point'] = light_type
            light['type'] = 'point' 
        elif blender_light.type == 'SPOT':
            light['spot'] = light_type
            light['type'] = 'spot' 
        else:
            continue

        if blender_light.type == 'POINT' or blender_light.type == 'SPOT':
            if blender_light.falloff_type == 'CONSTANT':
                light_type['constantAttenuation'] = 1.0
            elif blender_light.falloff_type == 'INVERSE_LINEAR':
                light_type['linearAttenuation'] = 1.0
            elif blender_light.falloff_type == 'INVERSE_SQUARE':
                light_type['quadraticAttenuation'] = 1.0
            else:
                continue
            
            if blender_light.type == 'SPOT':
                light_type['fallOffAngle'] = blender_light.spot_size
                light_type['fallOffExponent'] = 128.0 * blender_light.spot_blend

        light['color'] = [blender_light.color[0] * blender_light.energy, blender_light.color[1] * blender_light.energy, blender_light.color[2] * blender_light.energy]
        
        #
        
        light['name'] = blender_light.name
        
        #
        #
        
        lights.append(light)
        
    #
    #
    #
    
    for blender_scene in bpy.data.scenes:

        #
        # Property: light
        #

        light = {}
        
        light['type'] = 'ambient' 

        light['color'] = [blender_scene.world.ambient_color[0], blender_scene.world.ambient_color[1], blender_scene.world.ambient_color[2]]
        
        #
        
        light['name'] = 'Ambient_' + blender_scene.name
        
        #
        #
        
        lights.append(light)
    
    #
    #

    if len (lights) > 0:
        create_extensionUsed(operator, context, export_settings, glTF, 'KHR_lights')
        create_extensionRequired(operator, context, export_settings, glTF, 'KHR_lights')

        if glTF.get('extensions') is None:
            glTF['extensions'] = {}
            
        extensions = glTF['extensions']
        
        extensions_lights = {}

        extensions['KHR_lights'] = extensions_lights
        
        extensions_lights['lights'] = lights


def generate_meshes(operator,
                  context,
                  export_settings,
                  glTF):
    meshes = []

    #
    #
    
    filtered_meshes = export_settings['filtered_meshes']
    
    filtered_vertex_groups = export_settings['filtered_vertex_groups']

    for name, blender_mesh in filtered_meshes.items():
        
        internal_primitives = extract_primitives(glTF, blender_mesh, filtered_vertex_groups[name], export_settings)
        
        if len(internal_primitives) == 0:
            continue
        
        #
        # Property: mesh
        #
        
        # TODO: Morph target 'weights'.
        
        mesh = {}
        
        #
        
        primitives = []
        
        for internal_primitive in internal_primitives:
            
            # TODO: Morph target 'targets'.
            
            primitive = {}
            
            #
            #
            
            if export_settings['gltf_materials']:
                material = get_material_index(glTF, internal_primitive['material'])

                if get_material_requires_texcoords(glTF, material) and not export_settings['gltf_texcoords']:
                    material = -1

                if get_material_requires_normals(glTF, material) and not export_settings['gltf_normals']:
                    material = -1

                # Meshes/primitives without material are allowed.
                if material >= 0:
                    primitive['material'] = material
                
            #
            #
            
            indices = internal_primitive['indices']

            componentType = "UNSIGNED_BYTE"
            
            max_index = max(indices)
            
            if max_index < 256:
                componentType = "UNSIGNED_BYTE"
            elif max_index < 65536:
                componentType = "UNSIGNED_SHORT"
            elif max_index < 4294967296:
                componentType = "UNSIGNED_INT"
            else:
                print_console('ERROR', 'Invalid max_index: ' + str(max_index))
                continue

            count = len(indices)
            
            type = "SCALAR"
            
            indices_index = create_accessor(operator, context, export_settings, glTF, indices, componentType, count, type, "ELEMENT_ARRAY_BUFFER")
            
            if indices_index < 0:
                print_console('ERROR', 'Could not create accessor for indices')
                continue
            
            primitive['indices'] = indices_index
            
            #
            #
            
            attributes = {}
            
            #
            
            internal_attributes = internal_primitive['attributes']
            
            #
            #
            
            internal_position = internal_attributes['POSITION']

            componentType = "FLOAT"

            count = len(internal_position) // 3
            
            type = "VEC3"
            
            position = create_accessor(operator, context, export_settings, glTF, internal_position, componentType, count, type, "ARRAY_BUFFER")
            
            if position < 0:
                print_console('ERROR', 'Could not create accessor for position')
                continue
            
            attributes['POSITION'] = position
            
            #
            
            if export_settings['gltf_normals']:            
                internal_normal = internal_attributes['NORMAL']
    
                componentType = "FLOAT"
    
                count = len(internal_normal) // 3
                
                type = "VEC3"
                
                normal = create_accessor(operator, context, export_settings, glTF, internal_normal, componentType, count, type, "ARRAY_BUFFER")
                
                if normal < 0:
                    print_console('ERROR', 'Could not create accessor for normal')
                    continue
                
                attributes['NORMAL'] = normal
            
            #

            if export_settings['gltf_tangents']:            
                internal_tangent = calculate_tangent(internal_primitive)
                
                if internal_tangent is not None:

                    componentType = "FLOAT"
        
                    count = len(internal_tangent) // 4
                    
                    type = "VEC4"
                    
                    tangent = create_accessor(operator, context, export_settings, glTF, internal_tangent, componentType, count, type, "ARRAY_BUFFER")
                    
                    if tangent < 0:
                        print_console('ERROR', 'Could not create accessor for tangent')
                        continue
                    
                    attributes['TANGENT'] = tangent
            
            #
            
            if export_settings['gltf_texcoords']:
                texcoord_index = 0
                
                process_texcoord = True
                while process_texcoord:  
                    texcoord_id = 'TEXCOORD_' + str(texcoord_index)
                    
                    if internal_attributes.get(texcoord_id) is not None:
                        internal_texcoord = internal_attributes[texcoord_id]
            
                        componentType = "FLOAT"
            
                        count = len(internal_texcoord) // 2
                        
                        type = "VEC2"
                        
                        texcoord = create_accessor(operator, context, export_settings, glTF, internal_texcoord, componentType, count, type, "ARRAY_BUFFER")
                        
                        if texcoord < 0:
                            process_texcoord = False
                            print_console('ERROR', 'Could not create accessor for ' + texcoord_id)
                            continue
                        
                        attributes[texcoord_id] = texcoord
                        
                        texcoord_index += 1
                    else:
                        process_texcoord = False
                        
            #

            if export_settings['gltf_colors']:
                color_index = 0
                
                process_color = True
                while process_color:  
                    color_id = 'COLOR_' + str(color_index)
                    
                    if internal_attributes.get(color_id) is not None:
                        internal_color = internal_attributes[color_id]
            
                        componentType = "FLOAT"
            
                        count = len(internal_color) // 4
                        
                        type = "VEC4"
                        
                        color = create_accessor(operator, context, export_settings, glTF, internal_color, componentType, count, type, "ARRAY_BUFFER")
                        
                        if color < 0:
                            process_color = False
                            print_console('ERROR', 'Could not create accessor for ' + color_id)
                            continue
                        
                        attributes[color_id] = color
                        
                        color_index += 1
                    else:
                        process_color = False

            #
            
            if export_settings['gltf_skins']:
                bone_index = 0
                
                process_bone = True
                while process_bone:  
                    joint_id = 'JOINTS_' + str(bone_index)
                    weight_id = 'WEIGHTS_' + str(bone_index)
                    
                    if internal_attributes.get(joint_id) is not None and internal_attributes.get(weight_id) is not None:
                        internal_joint = internal_attributes[joint_id]
            
                        componentType = "UNSIGNED_SHORT"
            
                        count = len(internal_joint) // 4
                        
                        type = "VEC4"
                        
                        joint = create_accessor(operator, context, export_settings, glTF, internal_joint, componentType, count, type, "ARRAY_BUFFER")
                        
                        if joint < 0:
                            process_bone = False
                            print_console('ERROR', 'Could not create accessor for ' + joint_id)
                            continue
                        
                        attributes[joint_id] = joint
                        
                        #
                        #
    
                        internal_weight = internal_attributes[weight_id]
            
                        componentType = "FLOAT"
            
                        count = len(internal_weight) // 4
                        
                        type = "VEC4"
                        
                        weight = create_accessor(operator, context, export_settings, glTF, internal_weight, componentType, count, type, "ARRAY_BUFFER")
                        
                        if weight < 0:
                            process_bone = False
                            print_console('ERROR', 'Could not create accessor for ' + weight_id)
                            continue
                        
                        attributes[weight_id] = weight
                        
                        #
                        #
                        
                        bone_index += 1
                    else:
                        process_bone = False
            
            #
            #
            
            primitive['attributes'] = attributes
            
            #
            #
            
            primitives.append(primitive)
        

        mesh['primitives'] = primitives

        #

        mesh['name'] = name

        #
        #

        meshes.append(mesh)

    #
    #

    if len (meshes) > 0:
        glTF['meshes'] = meshes


def generate_node_parameter(operator,
                  context,
                  export_settings,
                  glTF,
                  matrix,
                  node,
                  node_type):
        
    translation, rotation, scale = decompose_transition(matrix, node_type, export_settings)
    
    #
    
    if translation[0] != 0.0 or translation[1] != 0.0 or translation[2] != 0.0:
        node['translation'] = [translation[0], translation[1], translation[2]]
        
    #

    if rotation[0] != 0.0 or rotation[1] != 0.0 or rotation[2] != 0.0 or rotation[3] != 1.0:
        node['rotation'] = [rotation[0], rotation[1], rotation[2], rotation[3]]
        
    #

    if scale[0] != 1.0 or scale[1] != 1.0 or scale[2] != 1.0:
        node['scale'] = [scale[0], scale[1], scale[2]]


def generate_nodes(operator,
                  context,
                  export_settings,
                  glTF):
    
    correction_quaternion = convert_swizzle_rotation(mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0)))
    
    #
    
    nodes = []
    
    skins = []

    #
    #
    
    filtered_objects = export_settings['filtered_objects']

    for blender_object in filtered_objects:
        #
        # Property: node
        #

        node = {}
        
        #
        #
        
        generate_node_parameter(operator, context, export_settings, glTF, blender_object.matrix_local, node, 'NODE')
        
        #
        #
        
        if blender_object.type == 'MESH':
            mesh = get_mesh_index(glTF, blender_object.data.name)
            
            if mesh >= 0:
                node['mesh'] = mesh
        
        #
        #
        
        if export_settings['gltf_cameras']:
            if blender_object.type == 'CAMERA':
                camera = get_camera_index(glTF, blender_object.data.name)
                
                if camera >= 0:
                    # Add correction node for camera, as default direction is different to Blender.
                    correction_node = {}
                    
                    correction_node['name'] = 'Correction_' + blender_object.name
                    correction_node['rotation'] = [correction_quaternion[1], correction_quaternion[2], correction_quaternion[3], correction_quaternion[0]]
                    
                    correction_node['camera'] = camera
                    
                    nodes.append(correction_node)


        if export_settings['gltf_lights']:
            if blender_object.type == 'LAMP':
                light = get_light_index(glTF, blender_object.data.name)
                if light >= 0:
                    khr_lights = {'light' : light}
                    extensions = {'KHR_lights' : khr_lights}
                    
                    # Add correction node for light, as default direction is different to Blender.
                    correction_node = {}
                    
                    correction_node['name'] = 'Correction_' + blender_object.name
                    correction_node['rotation'] = [correction_quaternion[1], correction_quaternion[2], correction_quaternion[3], correction_quaternion[0]]
                    
                    correction_node['extensions'] = extensions
                    
                    nodes.append(correction_node)

        # TODO: Morph target 'weights'.

        #

        node['name'] = blender_object.name

        #
        #

        nodes.append(node)

    #
    #

    if len (nodes) > 0:
        glTF['nodes'] = nodes

    #
    #
    
    if export_settings['gltf_skins']:
        for blender_object in filtered_objects:
            if blender_object.type != 'ARMATURE' or len(blender_object.pose.bones) == 0:
                continue
    
            #
            # Property: skin and node
            #
            
            skin = {}
            
            joints = []
            
            inverse_matrices = []
            
            skin['skeleton'] = get_node_index(glTF, blender_object.name)
            
            for blender_bone in blender_object.pose.bones:
    
                node = {}
                
                #
                #
                
                axis_basis_change = mathutils.Matrix(((1.0, 0.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, -1.0, 0.0, 0.0) , (0.0, 0.0, 0.0, 1.0))) * blender_object.matrix_basis 
                
                correction_matrix = mathutils.Matrix.Identity(4)
                
                if blender_bone.parent is None:
                    correction_matrix = axis_basis_change
                    
                correction_matrix = correction_matrix * blender_bone.bone.matrix_local
                    
                if blender_bone.parent is not None:
                    correction_matrix = blender_bone.parent.bone.matrix_local.inverted() * correction_matrix
                
                generate_node_parameter(operator, context, export_settings, glTF, correction_matrix * blender_bone.matrix_basis, node, 'JOINT')
        
                #
        
                node['name'] = blender_object.name + "_" + blender_bone.name
        
                #
                #
    
                joints.append(len(nodes))
                
                #
                #
                
                inverse_bind_matrix = axis_basis_change * blender_bone.bone.matrix_local
                inverse_bind_matrix.invert()
                
                for column in range(0, 4):
                    for row in range(0, 4):
                        inverse_matrices.append(inverse_bind_matrix[row][column])
                
                #
                #
        
                nodes.append(node)
                
            skin['joints'] = joints
            
            #
             
            componentType = "FLOAT"
            count = len(inverse_matrices) // 16
            type = "MAT4"
            
            inverseBindMatrices = create_accessor(operator, context, export_settings, glTF, inverse_matrices, componentType, count, type, "")
             
            skin['inverseBindMatrices'] = inverseBindMatrices
            
            #
            
            skins.append(skin)

    #
    #

    if len (skins) > 0:
        glTF['skins'] = skins

    #
    # Resolve children etc.
    #

    for blender_object in filtered_objects:
        node_index = get_node_index(glTF, blender_object.name)
        
        node = nodes[node_index]
        
        #
        if export_settings['gltf_skins']:
            blender_armature = blender_object.find_armature()
            if blender_armature is not None:
                node['skin'] = get_skin_index(glTF, blender_armature.name)

        #

        children = []
        
        # Camera
        if export_settings['gltf_cameras']:
            if blender_object.type == 'CAMERA':
                child_index = get_node_index(glTF, 'Correction_' + blender_object.name)
                if child_index >= 0:
                    children.append(child_index)

        # Light
        if export_settings['gltf_lights']:
            if blender_object.type == 'LIGHT':
                child_index = get_node_index(glTF, 'Correction_' + blender_object.name)
                if child_index >= 0:
                    children.append(child_index)

        # Nodes
        for blender_child_node in blender_object.children:
            child_index = get_node_index(glTF, blender_child_node.name)
            
            if child_index < 0:
                continue
            
            children.append(child_index)
        
        if export_settings['gltf_skins']:
            # Joint
            if blender_object.type == 'ARMATURE' and len(blender_object.pose.bones) > 0:
                child_index = get_node_index(glTF, blender_object.name + "_" + blender_object.pose.bones[0].name)
            
                if child_index < 0:
                    continue
            
                children.append(child_index)
                
                for blender_bone in blender_object.pose.bones:
                    joint_children = []
                    for blender_bone_child in blender_bone.children:
                        child_index = get_node_index(glTF, blender_object.name + "_" + blender_bone_child.name) 
                    
                        if child_index < 0:
                            continue
                    
                        joint_children.append(child_index)
                
                    if len(joint_children) > 0:
                        node_index = get_node_index(glTF, blender_object.name + "_" + blender_bone.name)
                        
                        child_node = nodes[node_index]
                        
                        child_node['children'] = joint_children

        if len(children) > 0:
            node['children'] = children


def generate_images(operator,
                  context,
                  export_settings,
                  glTF):
    filtered_images = export_settings['filtered_images']
                  
    images = []

    #
    #

    for blender_image in filtered_images:
        #
        # Property: image
        #

        image = {}

        #

        if export_settings['gltf_format'] == 'ASCII':

            if export_settings['gltf_embed_images']:
                # Embed image as Base64.
                
                png_data = create_png_data(blender_image)

                # Required

                image['uri'] = 'data:image/png;base64,' + base64.b64encode(png_data).decode('ascii')

            else:
                # Store image external.

                uri = get_uri(blender_image.filepath)

                context.scene.render.image_settings.file_format = 'PNG'
                context.scene.render.image_settings.color_depth = '8'        
                
                blender_image.save_render(export_settings['gltf_filedirectory'] + uri, context.scene)

                # Required

                image['uri'] = uri

        else:            
            # Store image as glb.
            
            png_data = create_png_data(blender_image)
            
            bufferView = create_bufferView(operator, context, export_settings, glTF, png_data, 0)

            # Required

            image['mimeType'] = 'image/png'
            
            image['bufferView'] = bufferView

        #
        #
        
        export_settings['gltf_uri'].append(get_uri(blender_image.filepath)) 

        images.append(image)

    #
    #

    if len (images) > 0:
        glTF['images'] = images


def generate_textures(operator,
                       context,
                       export_settings,
                       glTF):
    filtered_textures = export_settings['filtered_textures']
                  
    textures = []

    #
    #

    for blenderTexture in filtered_textures:
        #
        # Property: texture
        #

        texture = {}
        
        #

        if isinstance(blenderTexture, bpy.types.ShaderNodeTexImage):
            magFilter = 9729
            if blenderTexture.interpolation == 'Closest':
                magFilter = 9728
            wrap = 10497
            if blenderTexture.extension == 'CLIP':
                wrap = 33071

            texture['sampler'] = create_sampler(operator, context, export_settings, glTF, magFilter, wrap)

            texture['source'] = get_image_index(export_settings, get_uri(blenderTexture.image.filepath))
            
            #
            #
    
            textures.append(texture)
            
        else:
            if export_settings['gltf_common'] != '-':
                magFilter = 9729
                wrap = 10497
                if blenderTexture.texture.extension == 'CLIP':
                    wrap = 33071
    
                texture['sampler'] = create_sampler(operator, context, export_settings, glTF, magFilter, wrap)
    
                texture['source'] = get_image_index(export_settings, get_uri(blenderTexture.texture.image.filepath))

                #
                #
        
                textures.append(texture)

    #
    #

    if len (textures) > 0:
        glTF['textures'] = textures


def generate_materials(operator,
                       context,
                       export_settings,
                       glTF):
    filtered_materials = export_settings['filtered_materials']
                  
    materials = []
    
    KHR_materials_common_Used = False

    #
    #
    
    for blender_material in filtered_materials:
        # 
        # Property: material
        #

        material = {}

        #
        
        if blender_material.node_tree is not None:
        
            for currentNode in blender_material.node_tree.nodes:
                if isinstance(currentNode, bpy.types.ShaderNodeGroup):
    
                    if currentNode.node_tree.name == 'glTF Metal Roughness':
                        # 
                        # Property: pbrMetallicRoughness
                        #
                        
                        material['pbrMetallicRoughness'] = {}
    
                        pbrMetallicRoughness = material['pbrMetallicRoughness']
    
                        #
                        # Base color texture
                        #
                        index = get_texture_index(export_settings, glTF, 'BaseColor', currentNode)
                        if index >= 0:
                            baseColorTexture = {
                                'index' : index
                            }
    
                            texCoord = get_texcoord_index(glTF, 'BaseColor', currentNode)
                            if texCoord > 0:
                                baseColorTexture['texCoord'] = texCoord
                            
                            pbrMetallicRoughness['baseColorTexture'] = baseColorTexture
    
                        #
                        # Base color factor
                        #
                        baseColorFactor = get_vec4(currentNode.inputs['BaseColorFactor'].default_value, [1.0, 1.0, 1.0, 1.0])
                        if baseColorFactor[0] != 1.0 or baseColorFactor[1] != 1.0 or baseColorFactor[2] != 1.0 or baseColorFactor[3] != 1.0:
                            pbrMetallicRoughness['baseColorFactor'] = baseColorFactor
    
                        #
                        # Metallic factor
                        #
                        metallicFactor = get_scalar(currentNode.inputs['MetallicFactor'].default_value, 1.0)
                        if metallicFactor != 1.0:
                            pbrMetallicRoughness['metallicFactor'] = metallicFactor
    
                        #
                        # Roughness factor
                        #
                        roughnessFactor = get_scalar(currentNode.inputs['RoughnessFactor'].default_value, 1.0)
                        if roughnessFactor != 1.0:
                            pbrMetallicRoughness['roughnessFactor'] = roughnessFactor
    
                        #
                        # Metallic roughness texture
                        #
                        index = get_texture_index(export_settings, glTF, 'MetallicRoughness', currentNode)
                        if index >= 0:
                            metallicRoughnessTexture = {
                                'index' : index
                            }
                            
                            texCoord = get_texcoord_index(glTF, 'MetallicRoughness', currentNode)
                            if texCoord > 0:
                                metallicRoughnessTexture['texCoord'] = texCoord
    
                            pbrMetallicRoughness['metallicRoughnessTexture'] = metallicRoughnessTexture
                            
                    if currentNode.node_tree.name == 'glTF Specular Glossiness':
                        # TODO: Specular Glossiness
                        print_console('DUMMY', 'Specular Glossiness Store Material')
    
                    #
                    # Emissive texture
                    #
                    index = get_texture_index(export_settings, glTF, 'Emissive', currentNode)
                    if index >= 0:
                        emissiveTexture = {
                            'index' : index
                        }
    
                        texCoord = get_texcoord_index(glTF, 'Emissive', currentNode)
                        if texCoord > 0:
                            emissiveTexture['texCoord'] = texCoord
    
                        material['emissiveTexture'] = emissiveTexture
    
                    #
                    # Emissive factor
                    #
                    emissiveFactor = get_vec3(currentNode.inputs['EmissiveFactor'].default_value, [0.0, 0.0, 0.0])
                    if emissiveFactor[0] != 0.0 or emissiveFactor[1] != 0.0 or emissiveFactor[2] != 0.0:
                        material['emissiveFactor'] = emissiveFactor
    
                    #
                    # Normal texture
                    #
                    index = get_texture_index(export_settings, glTF, 'Normal', currentNode)
                    if index >= 0:
                        normalTexture = {
                            'index' : index
                        }
    
                        texCoord = get_texcoord_index(glTF, 'Normal', currentNode)
                        if texCoord > 0:
                            normalTexture['texCoord'] = texCoord
    
                        scale = get_scalar(currentNode.inputs['NormalScale'].default_value, 1.0)
    
                        if scale != 1.0:
                            normalTexture['scale'] = scale
    
                        material['normalTexture'] = normalTexture
    
                    #
                    # Occlusion texture
                    #
                    if len(currentNode.inputs['Occlusion'].links) > 0:
                        index = get_texture_index(export_settings, glTF, 'Occlusion', currentNode)
                        if index >= 0:
                            occlusionTexture = {
                                'index' : index
                            }
    
                            texCoord = get_texcoord_index(glTF, 'Occlusion', currentNode)
                            if texCoord > 0:
                                occlusionTexture['texCoord'] = texCoord
    
                            strength = get_scalar(currentNode.inputs['OcclusionStrength'].default_value, 1.0)
    
                            if strength != 1.0:
                                occlusionTexture['strength'] = strength
    
                            material['occlusionTexture'] = occlusionTexture
    
                    #
                    # Alpha
                    #
                    index = get_texture_index(export_settings, glTF, 'Alpha', currentNode)
                    if index >= 0:
                        alphaMode = 'BLEND'
                        if get_scalar(currentNode.inputs['AlphaMode'].default_value, 0.0) >= 0.5:
                            alphaMode = 'MASK'
    
                            material['alphaCutoff'] = get_scalar(currentNode.inputs['AlphaCutoff'].default_value, 0.5)
    
                        material['alphaMode'] = alphaMode
                        
                    #
                    # Double sided
                    #
                    if get_scalar(currentNode.inputs['DoubleSided'].default_value, 0.0) >= 0.5:
                        material['doubleSided'] = True
                    
                    #
                    # Use Color_0
                    #
                    
                    if get_scalar(currentNode.inputs['Use COLOR_0'].default_value, 0.0) < 0.5:
                        export_settings['gltf_use_no_color'].append(blender_material.name)

                    #
            
                    material['name'] = blender_material.name
            
                    #
                    #
            
                    materials.append(material)

        else:
            if export_settings['gltf_common'] != '-':
                KHR_materials_common_Used = True
                
                # 
                # Property: Common Material
                #
    
                common = { 'type' : export_settings['gltf_common'] }
                
                material['extensions'] = { 'KHR_materials_common' : common }
                
                common['ambientFactor'] = [blender_material.ambient, blender_material.ambient, blender_material.ambient]
                
                alpha = 1.0
                if blender_material.use_transparency:
                    alpha = blender_material.alpha 

                if export_settings['gltf_common'] != 'commonConstant':
                    common['diffuseFactor'] = [blender_material.diffuse_color[0] * blender_material.diffuse_intensity, blender_material.diffuse_color[1] * blender_material.diffuse_intensity, blender_material.diffuse_color[2] * blender_material.diffuse_intensity, alpha]
        
                    if export_settings['gltf_common'] != 'commonLambert':
                        common['specularFactor'] = [blender_material.specular_color[0] * blender_material.specular_intensity, blender_material.specular_color[1] * blender_material.specular_intensity, blender_material.specular_color[2] * blender_material.specular_intensity]
            
                        shininessFactor = 128.0 * (float(blender_material.specular_hardness) - 1.0) / 510.0
            
                        common['shininessFactor'] = shininessFactor
    
                #
                
                material['emissiveFactor'] = [blender_material.emit * blender_material.diffuse_color[0], blender_material.emit * blender_material.diffuse_color[1], blender_material.emit * blender_material.diffuse_color[2]]
                
                #
                
                for texture_slot in blender_material.texture_slots:
                    if texture_slot and texture_slot.texture and texture_slot.texture.type == 'IMAGE' and texture_slot.texture.image is not None:
                        if export_settings['gltf_common'] != 'commonConstant':
                            #
                            # Diffuse texture
                            #
                            if texture_slot.use_map_color_diffuse:
                                index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                                if index >= 0:
                                    diffuseTexture = {
                                        'index' : index
                                    }
                                    common['diffuseTexture'] = diffuseTexture
                            if export_settings['gltf_common'] != 'commonLambert':                                #
                                # Specular texture
                                #
                                if texture_slot.use_map_color_spec:
                                    index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                                    if index >= 0:
                                        specularTexture = {
                                            'index' : index
                                        }
                                        common['specularTexture'] = specularTexture
                                #
                                # Shininess texture
                                #
                                if texture_slot.use_map_hardness:
                                    index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                                    if index >= 0:
                                        shininessTexture = {
                                            'index' : index
                                        }
                                        common['shininessTexture'] = shininessTexture
                        #
                        # Ambient texture
                        #
                        if texture_slot.use_map_ambient:
                            index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                            if index >= 0:
                                ambientTexture = {
                                    'index' : index
                                }
                                common['ambientTexture'] = ambientTexture
                        #
                        # Emissive texture
                        #
                        if texture_slot.use_map_emit:
                            index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                            if index >= 0:
                                emissiveTexture = {
                                    'index' : index
                                }
                                material['emissiveTexture'] = emissiveTexture
                        #
                        # Normal texture
                        #
                        if texture_slot.use_map_normal:
                            index = get_texture_index_by_filepath(export_settings, glTF, texture_slot.texture.image.filepath)
                            if index >= 0:
                                normalTexture = {
                                    'index' : index
                                }
                                material['normalTexture'] = normalTexture

                #
        
                material['name'] = blender_material.name
        
                #
                #
        
                materials.append(material)

    #
    #

    if len (materials) > 0:
        if KHR_materials_common_Used:
            create_extensionUsed(operator, context, export_settings, glTF, 'KHR_materials_common')
            create_extensionRequired(operator, context, export_settings, glTF, 'KHR_materials_common')

        glTF['materials'] = materials


def generate_scenes(operator,
                    context,
                    export_settings,
                    glTF):
    scenes = []

    #

    for blender_scene in bpy.data.scenes:
        # 
        # Property: scene
        #

        scene = {}

        #
        
        nodes = []
            
        for object in blender_scene.objects:
            if object.parent is None:
                node_index = get_node_index(glTF, object.name)
                
                if node_index < 0:
                    continue
                
                nodes.append(node_index)

        if len(nodes) > 0:
            scene['nodes'] = nodes
                
        #

        if export_settings['gltf_lights']:
            light = get_light_index(glTF, 'Ambient_' + blender_scene.name)
            if light >= 0:
                khr_lights = {'light' : light}
                extensions = {'KHR_lights' : khr_lights}
                scene['extensions'] = extensions

        #

        scene['name'] = blender_scene.name

        #
        #
        
        scenes.append(scene)

    #
    #

    if len (scenes) > 0:
        glTF['scenes'] = scenes


def generate_scene(operator,
                    context,
                    export_settings,
                    glTF):
    index = get_scene_index(glTF, bpy.context.screen.scene.name)
    
    #
    #

    if index >= 0:
        glTF['scene'] = index


def generate_glTF(operator,
                  context,
                  export_settings,
                  glTF):
    generate_asset(operator, context, export_settings, glTF)
    
    #

    if export_settings['gltf_materials']:
        generate_images(operator, context, export_settings, glTF)
    
        generate_textures(operator, context, export_settings, glTF)
    
        generate_materials(operator, context, export_settings, glTF)
    
    #

    if export_settings['gltf_cameras']:
        generate_cameras(operator, context, export_settings, glTF)
        
    if export_settings['gltf_lights']:
        generate_lights(operator, context, export_settings, glTF)        
    
    #
    
    generate_meshes(operator, context, export_settings, glTF)
    
    #

    generate_nodes(operator, context, export_settings, glTF)
    
    #
    
    if export_settings['gltf_animations']:
        generate_animations(operator, context, export_settings, glTF)
    
    #
    
    generate_scenes(operator, context, export_settings, glTF)
    
    generate_scene(operator, context, export_settings, glTF)
    
    #
    
    byteLength = len(export_settings['gltf_binary']) 
    
    if byteLength > 0:
        glTF['buffers'] = []

        buffer = {
            'byteLength' : byteLength
        }
        
        if export_settings['gltf_format'] == 'ASCII':        
            uri = export_settings['gltf_binaryfilename']
            
            if export_settings['gltf_embed_buffers']:
                uri = 'data:application/octet-stream;base64,' + base64.b64encode(export_settings['gltf_binary']).decode('ascii')
                
            buffer['uri'] = uri
        
        glTF['buffers'].append(buffer)
