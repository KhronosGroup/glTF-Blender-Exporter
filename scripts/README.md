Scripts
-------
There are two possibilities, how to integrate and enable the glTF 2.0 exporter into Blender: 

One possibility is to set this folder as the `Scripts` folder.
For this, open the `User Preferences...` dialog in Blender.

![Blender User Preferences](Blender_user_preferences.png)  

Switch to the `File` tab and set the `Scripts` entry to this folder.  

![Blender User Preferences File](Blender_file.png)  

Advantage is, that any update/pull to the exporter is automatically visible by Blender. Drawback is, that the `Scripts` folder is just used for the glTF 2.0 Python modules.

Otherwise, copy the `io_scene_gltf2` folder to the `scripts/addons` folder of your Blender installation.

![Blender Explore](Blender_explorer.png)  

In both cases, enable the glTF 2.0 exporter under the `Add-ons` tab. 

![Blender Enable](Blender_enable.png)  
