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
import json
import struct

from .gltf2_debug import *
from .gltf2_filter import *
from .gltf2_generate import *

#
# Globals
#

#
# Functions
#

def prepare(export_settings):
    if len(bpy.context.selected_objects) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
    
    filter_apply(export_settings)
    
    export_settings['gltf_original_frame'] = bpy.context.scene.frame_current 
    
    export_settings['gltf_use_no_color'] = []
    
    if not export_settings['gltf_animations'] and not export_settings['gltf_current_frame']:
        bpy.context.scene.frame_set(0)

    
def finish(export_settings):
    if export_settings['temporary_meshes'] is not None:
        for temporary_mesh in export_settings['temporary_meshes']:
            bpy.data.meshes.remove(temporary_mesh)
            
    bpy.context.scene.frame_set(export_settings['gltf_original_frame'])  


def save(operator,
         context,
         export_settings):

    print_console('INFO', 'Starting glTF 2.0 export')
    
    #
    
    prepare(export_settings)
    
    #

    glTF = {}

    generate_glTF(operator, context, export_settings, glTF)

    #

    indent = None
    separators = separators=(',', ':')

    if export_settings['gltf_format'] == 'ASCII' and not export_settings['gltf_strip']:
        indent = 4
        separators = separators=(', ', ' : ')
    
    glTF_encoded = json.dumps(glTF, indent=indent, separators=separators, sort_keys=True)
    
    #

    if export_settings['gltf_format'] == 'ASCII':
        file = open(export_settings['gltf_filepath'], "w", encoding="utf8", newline="\n")
        file.write(glTF_encoded)
        file.write("\n")
        file.close()
        
        binary = export_settings['gltf_binary']
        if len(binary) > 0 and not export_settings['gltf_embed_buffers']:
            file = open(export_settings['gltf_filedirectory'] + export_settings['gltf_binaryfilename'], "wb")
            file.write(binary)
            file.close()
        
    else:
        file = open(export_settings['gltf_filepath'], "wb")

        glTF_data = glTF_encoded.encode()
        binary = export_settings['gltf_binary']

        length_gtlf = len(glTF_data) + 8
        zeros_gltf = 4 - (length_gtlf % 4)
        if zeros_gltf != 4:
            length_gtlf += zeros_gltf
        else:
            zeros_gltf = 0
        
        length_bin = len(binary) + 8
        zeros_bin = 4 - (length_bin % 4)
        if zeros_bin != 4:
            length_bin += zeros_bin
        else:
            zeros_bin = 0

        length = 12 + length_gtlf
        if length_bin > 0:
            length += length_bin
        
        # Header (Version 2)
        file.write('glTF'.encode())
        file.write(struct.pack("I", 2))
        file.write(struct.pack("I", length))
        
        # Chunk 0 (JSON)
        file.write(struct.pack("I", length_gtlf)) 
        file.write('JSON'.encode())
        file.write(glTF_data)
        for i in range(0, zeros_gltf):
            file.write('\0'.encode())

        # Chunk 1 (BIN)
        if length_bin > 0:
            file.write(struct.pack("I", length_bin)) 
            file.write('BIN\0'.encode())
            file.write(binary)
            for i in range(0, zeros_bin):
                file.write('\0'.encode())
            
        file.close()
        
    #
    
    finish(export_settings)
    
    #

    print_console('INFO', 'Finished glTF 2.0 export')
    print_newline()

    return {'FINISHED'}
