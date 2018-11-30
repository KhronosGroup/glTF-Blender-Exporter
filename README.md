
🚨 IMPORTANT: This exporter supports only Blender <2.79b. A newer project,
[glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO), provides
both export and import for Blender 2.80, and is included by default in the
[Blender 2.8 Beta](https://www.blender.org/experimental). All future development
will take place there.

[![Blender](misc/Blender_logo.png)](http://www.blender.org/) [![glTF](misc/glTF_logo.png)](https://www.khronos.org/gltf/)  

Blender glTF 2.0 Exporter
=========================

Version
-------

1.0

Introduction
------------
This is the offical Khronos Blender glTF 2.0 exporter. This repository mainly contains Python scripts to export the internal Blender data structure to glTF 2.0. Node groups are also provided, to simulate glTF Physically-Based Rendering (PBR) materials using the Cycles renderer. Finally, several Blender scenes are provided demonstrating each feature individually. 

Installation
------------
The Khronos glTF 2.0 exporter is not available in the *Add-ons* tab by default, and must be installed manually by copying the `scripts/addons/io_scene_gltf2` folder into the `scripts/addons/` directory of the Blender installation, then enabling it under the *Add-ons* tab. Read [detailed installation instructions here](scripts/).

Using the exporter
--------------
Refer to [user documentation](docs/user.md). For best results with PBR materials, use the node groups provided with the exporter.

Features
--------------

This exporter supports meshes, materials, animation (keyframes, skinning, and shape keys), and more. For a complete list of features available in glTF 2.0, see the [official specification](https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md) and [list of extensions](https://github.com/KhronosGroup/glTF/tree/master/extensions#extensions-for-gltf-20). This exporter allows the following extensions:

* [Specular-Glossiness PBR materials](https://github.com/KhronosGroup/glTF/blob/master/extensions/2.0/Khronos/KHR_materials_pbrSpecularGlossiness/README.md)
* [Unlit materials](https://github.com/KhronosGroup/glTF/tree/master/extensions/2.0/Khronos/KHR_materials_unlit/README.md)

Folders
--------------

[docs](docs/)  
Documentation about the Blender glTF 2.0 exporter and its usage.  
[environments](environments/)  
Location of environment maps used in the [scenes](scenes/).  
[misc](misc/)  
Miscellaneous files like logos and so on.  
[pbr_node](pbr_node/)  
Blender node groups for simulating the glTF 2.0 material model.  
[polly](polly/)  
Project 'Polly' Blender and glTF 2.0 scenes.  
[scenes](scenes/)  
Basic and enhanced scenes for testing the exporter.  
[scripts](scripts/)  
Blender Python scripts for exporting scenes to the glTF 2.0 format.  
[tests](tests/)  
Python scripts for testing the exporter itself.
