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

#
# Globals
#

#
# Functions
#

bpy.ops.export_scene.gltf(filepath="temp/01_test.gltf" + current_path, check_existing=True, export_copyright="", export_layers=False, export_tangents=True, export_skins=True, export_morph=True, export_bake_skins=False, export_embed_buffers=False, export_force_indices=False, export_colors=True, export_animations=True, export_common=False, export_texcoords=True, export_materials=True, export_embed_images=False, export_indices='UNSIGNED_SHORT', export_camera_infinite=False, export_selected=False, export_strip=False, export_normals=True, export_apply=False, export_cameras=True, export_current_frame=True, export_lights_cmn=False, export_extras=False, export_displacement=False, filter_glob="*.gltf")
