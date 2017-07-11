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
import math
import mathutils

from .gltf2_debug import *
from .gltf2_extract import *

#
# Globals
#

#
# Functions
#

def animate_get_interpolation(blender_fcurve_list):
    """
    Retrieves the glTF interpolation, depending on a fcurve list.
    Blender allows mixing and more variations of interpolations.  
    In such a case, a conversion is needed.
    """
    interpolation = 'CONVERSION_NEEDED'
    
    for blender_fcurve in blender_fcurve_list:
        if blender_fcurve is None:
            continue
        
        for blender_keyframe in blender_fcurve.keyframe_points:
            if interpolation is None:
                if blender_keyframe.interpolation == 'LINEAR': 
                    interpolation = 'LINEAR'
                elif blender_keyframe.interpolation == 'CONSTANT': 
                    interpolation = 'STEP'
                else:
                    interpolation = 'CONVERSION_NEEDED'
                    return interpolation 
            else:
                if blender_keyframe.interpolation == 'LINEAR' and interpolation != 'LINEAR': 
                    interpolation = 'CONVERSION_NEEDED'
                    return interpolation
                elif blender_keyframe.interpolation == 'CONSTANT' and interpolation != 'STEP':
                    interpolation = 'CONVERSION_NEEDED'
                    return interpolation
                elif blender_keyframe.interpolation != 'LINEAR' and blender_keyframe.interpolation != 'CONSTANT':
                    interpolation = 'CONVERSION_NEEDED'
                    return interpolation
    
    return interpolation
    

def animate_convert_rotation_axis_angle(axis_angle):
    """
    Converts an axis angle to a quaternion rotation. 
    """
    q = mathutils.Quaternion((axis_angle[1], axis_angle[2], axis_angle[3]), axis_angle[0])
    
    return [q.x, q.y, q.z, q.w]


def animate_convert_rotation_euler(euler, rotation_mode):
    """
    Converts an euler angle to a quaternion rotation. 
    """
    rotation = mathutils.Euler((euler[0], euler[1], euler[2]), rotation_mode).to_quaternion()

    return [rotation.x, rotation.y, rotation.z, rotation.w]


def animate_convert_keys(key_list):
    """
    Converts Blender key frames to glTF time keys depending on the applied frames per second. 
    """
    times = []
    
    for key in key_list:
        times.append(key / bpy.context.scene.render.fps)

    return times


def animate_gather_keys(fcurve_list, interpolation):
    """
    Merges and sorts several key frames to one set. 
    If an interpolation conversion is needed, the sample key frames are created as well.
    """
    keys = []
    
    if interpolation == 'CONVERSION_NEEDED':
        start = None
        end = None
        
        for blender_fcurve in fcurve_list:
            if blender_fcurve is None:
                continue
            
            if start == None:
                start = blender_fcurve.range()[0]
            else:
                start = min(start, blender_fcurve.range()[0])
                
            if end == None:
                end = blender_fcurve.range()[1]
            else:
                end = max(end, blender_fcurve.range()[1])

        key = start
        while key <= end:
            keys.append(key)
            key += 1.0
    else: 
        for blender_fcurve in fcurve_list:
            if blender_fcurve is None:
                continue
            
            for blender_keyframe in blender_fcurve.keyframe_points:
                if blender_keyframe.co[0] not in keys:
                    keys.append(blender_keyframe.co[0])

        keys.sort()
    
    return keys


def animate_location(export_settings, location, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for location transformations.
    """
    if not export_settings['gltf_joint_cache'].get(node_name):
        export_settings['gltf_joint_cache'][node_name] = {}
    
    keys = animate_gather_keys(location, interpolation)
    
    times = animate_convert_keys(keys)
    
    result = {}
    
    keyframe_index = 0
    for time in times:
        translation = [0.0, 0.0, 0.0]
        
        if node_type == 'JOINT':
            if export_settings['gltf_joint_cache'][node_name].get(keys[keyframe_index]):
                translation, tmp_rotation, tmp_scale = export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] 
            else:
                bpy.context.scene.frame_set(keys[keyframe_index])
                
                matrix = matrix_correction * matrix_basis 
    
                translation, tmp_rotation, tmp_scale = matrix.decompose()
                
                export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] = [translation, tmp_rotation, tmp_scale]
        else:
            channel_index = 0
            for blender_fcurve in location:
                
                if blender_fcurve is not None:
                    value = blender_fcurve.evaluate(keys[keyframe_index]) 
                    
                    translation[channel_index] = value
                
                channel_index += 1 
        
            translation = convert_swizzle_location(translation)
        
        result[time] = translation
        
        keyframe_index += 1 

    return result


def animate_rotation_axis_angle(export_settings, rotation_axis_angle, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for axis angle transformations.
    """
    if not export_settings['gltf_joint_cache'].get(node_name):
        export_settings['gltf_joint_cache'][node_name] = {}
    
    keys = animate_gather_keys(rotation_axis_angle, interpolation)
    
    times = animate_convert_keys(keys)
    
    result = {}
    
    keyframe_index = 0
    for time in times:
        axis_angle_rotation = [1.0, 0.0, 0.0, 0.0]
        
        rotation = [1.0, 0.0, 0.0, 0.0]
        
        if node_type == 'JOINT':
            if export_settings['gltf_joint_cache'][node_name].get(keys[keyframe_index]):
                tmp_location, rotation, tmp_scale = export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] 
            else:
                bpy.context.scene.frame_set(keys[keyframe_index])
                
                matrix = matrix_correction * matrix_basis 
    
                tmp_location, rotation, tmp_scale = matrix.decompose()
                
                export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] = [tmp_location, rotation, tmp_scale]
        else:
            channel_index = 0
            for blender_fcurve in rotation_axis_angle:
                if blender_fcurve is not None:
                    value = blender_fcurve.evaluate(keys[keyframe_index]) 
                    
                    axis_angle_rotation[channel_index] = value
                
                channel_index += 1 

            rotation = animate_convert_rotation_axis_angle(axis_angle_rotation)
        
            # Bring back to internal Quaternion notation. 
            rotation = convert_swizzle_rotation([rotation[3], rotation[0], rotation[1], rotation[2]])
            
        # Bring back to glTF Quaternion notation.
        rotation = [rotation[1], rotation[2], rotation[3], rotation[0]]
        
        result[time] = rotation
        
        keyframe_index += 1 

    return result


def animate_rotation_euler(export_settings, rotation_euler, rotation_mode, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for euler angle transformations.
    """
    if not export_settings['gltf_joint_cache'].get(node_name):
        export_settings['gltf_joint_cache'][node_name] = {}
    
    keys = animate_gather_keys(rotation_euler, interpolation)

    times = animate_convert_keys(keys)

    result = {}
    
    keyframe_index = 0
    for time in times:
        euler_rotation = [0.0, 0.0, 0.0]
        
        rotation = [1.0, 0.0, 0.0, 0.0]
        
        if node_type == 'JOINT':
            if export_settings['gltf_joint_cache'][node_name].get(keys[keyframe_index]):
                tmp_location, rotation, tmp_scale = export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] 
            else:
                bpy.context.scene.frame_set(keys[keyframe_index])
                
                matrix = matrix_correction * matrix_basis 
    
                tmp_location, rotation, tmp_scale = matrix.decompose()
                
                export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] = [tmp_location, rotation, tmp_scale]
        else:
            channel_index = 0
            for blender_fcurve in rotation_euler:
                if blender_fcurve is not None:
                    value = blender_fcurve.evaluate(keys[keyframe_index]) 
                    
                    euler_rotation[channel_index] = value
                
                channel_index += 1
    
            rotation = animate_convert_rotation_euler(euler_rotation, rotation_mode)
        
            # Bring back to internal Quaternion notation. 
            rotation = convert_swizzle_rotation([rotation[3], rotation[0], rotation[1], rotation[2]])
            
        # Bring back to glTF Quaternion notation.
        rotation = [rotation[1], rotation[2], rotation[3], rotation[0]]
        
        result[time] = rotation
        
        keyframe_index += 1 

    return result


def animate_rotation_quaternion(export_settings, rotation_quaternion, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for quaternion transformations.
    """
    if not export_settings['gltf_joint_cache'].get(node_name):
        export_settings['gltf_joint_cache'][node_name] = {}
    
    keys = animate_gather_keys(rotation_quaternion, interpolation)

    times = animate_convert_keys(keys)
    
    result = {}

    keyframe_index = 0
    for time in times:
        rotation = [1.0, 0.0, 0.0, 0.0]
        
        if node_type == 'JOINT':
            if export_settings['gltf_joint_cache'][node_name].get(keys[keyframe_index]):
                tmp_location, rotation, tmp_scale = export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] 
            else:
                bpy.context.scene.frame_set(keys[keyframe_index])
                
                matrix = matrix_correction * matrix_basis 
    
                tmp_location, rotation, tmp_scale = matrix.decompose()
                
                export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] = [tmp_location, rotation, tmp_scale]
        else:
            channel_index = 0
            for blender_fcurve in rotation_quaternion:
                
                if blender_fcurve is not None:
                    value = blender_fcurve.evaluate(keys[keyframe_index]) 
                    
                    rotation[channel_index] = value
                
                channel_index += 1 
        
            rotation = convert_swizzle_rotation(rotation)

        # Bring to glTF Quaternion notation.
        rotation = [rotation[1], rotation[2], rotation[3], rotation[0]]
        
        result[time] = rotation
        
        keyframe_index += 1 

    return result


def animate_scale(export_settings, scale, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for scale transformations.
    """
    if not export_settings['gltf_joint_cache'].get(node_name):
        export_settings['gltf_joint_cache'][node_name] = {}
    
    keys = animate_gather_keys(scale, interpolation)

    times = animate_convert_keys(keys)

    result = {}

    keyframe_index = 0
    for time in times:
        scale_data = [1.0, 1.0, 1.0]
        
        if node_type == 'JOINT':
            if export_settings['gltf_joint_cache'][node_name].get(keys[keyframe_index]):
                tmp_location, tmp_rotation, scale_data = export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] 
            else:
                bpy.context.scene.frame_set(keys[keyframe_index])
                
                matrix = matrix_correction * matrix_basis 
    
                tmp_location, tmp_rotation, scale_data = matrix.decompose()
                
                export_settings['gltf_joint_cache'][node_name][keys[keyframe_index]] = [tmp_location, tmp_rotation, scale_data]
        else:
            channel_index = 0
            for blender_fcurve in scale:
                
                if blender_fcurve is not None:
                    value = blender_fcurve.evaluate(keys[keyframe_index]) 
                    
                    scale_data[channel_index] = value
                
                channel_index += 1 
        
            scale_data = convert_swizzle_scale(scale_data)
        
        result[time] = scale_data
        
        keyframe_index += 1 

    return result


def animate_value(export_settings, value_parameter, interpolation, node_type, node_name, matrix_correction, matrix_basis):
    """
    Calculates/gathers the key value pairs for scalar anaimations.
    """
    keys = animate_gather_keys(value_parameter, interpolation)

    times = animate_convert_keys(keys)

    result = {}

    keyframe_index = 0
    for time in times:
        value_data = [0.0]
        
        channel_index = 0
        for blender_fcurve in value_parameter:
            
            if blender_fcurve is not None:
                value = blender_fcurve.evaluate(keys[keyframe_index]) 
                
                value_data[channel_index] = value
            
            channel_index += 1 
        
        result[time] = value_data
        
        keyframe_index += 1 

    return result
