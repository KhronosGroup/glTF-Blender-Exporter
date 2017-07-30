
[![Blender](misc/Blender_logo.png)](http://www.blender.org/) [![glTF](misc/glTF_logo.png)](https://www.khronos.org/gltf/)  

Blender glTF 2.0 Exporter
=========================

Version
-------

1.0 Beta

Introduction
------------
This is the offical Khronos Blender glTF 2.0 exporter. This repository mainly contains Python scripts to export the internal Blender data structure to glTF 2.0. Furthermore, node groups are provided, which do simulate the Physically-Based Rendering (PBR) materials using the Cycles renderer. Finally, several Blender scenes are provided, which do demonstrate each feature individually. 

Installation
------------
At point of writing, the Khronos glTF 2.0 exporter is not part of any offical, community or testing Blender add-on, which can be activated in the "User Preferences ..." Add-ons tab.  
Because of this, the exporter has to be added manually, which is described in the [scripts](scripts/) section.

Exporter usage
--------------
The glTF 2.0 exporter provides several export settings. At the point of writing, to export PBR materials, specific node groups have to be used.
Details about this can be found in the [docs](docs/) section.

Folders
-------

[docs](docs/)  
Documentation about the Blender glTF 2.0 exporter and its usage.  
[environments](environments/)  
Location of environment maps used in the [scenes](scenes/).  
[misc](misc/)  
Miscellaneous files like logos and so on.  
[pbr_node](pbr_node/)  
Blender node groups for simulating the glTF 2.0 material model.  
[scenes](scenes/)  
Basic and enhanced scenes for testing the exporter.  
[scripts](scripts/)  
Blender Python scripts for exporting scenes to the glTF 2.0 format.  
[tests](tests/)  
Python scripts for testing the exporter itself.
