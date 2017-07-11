Developer Documentation
-----------------------

### Preface

In general, the main documentation for developers can be found inside the source files and its functions.
The goal of this document is to provide an understanding for the concept of the exporter.  

### Implementation Details

#### Coordinate system mapping

Blender uses a right-handed coordinate system, where `x` point right, `y` point forward and `z` up. glTF 2.0 also uses a right-handed coordinate system, but with `x` point right, `y` point up and `z` backward.  

To map from Blender to glTF 2.0, the following mapping for meshes is used:

|Blender|glTF 2.0|
|:-----:|:------:|
|x      |x       |
|y      |z       |
|z      |-y      |

Depending on this mapping, following transformation rules for nodes - not joints - exist:

|Blender|glTF 2.0|Translate|Rotate|Scale|
|:-----:|--------|:-------:|:----:|:----|
|x      |        |x        |x     |x    |
|y      |        |z        |z     |z    |
|z      |        |-y       |-y    |y    |
|w      |        |         |w     |     |

Any Euler or Angle rotation is first converted to a Quaternion rotation. For quaternions, in Blender, `w` is located at first position of the vector. During the conversion, `w` is put at the end of vector, to be compliant with glTF 2.0.

### References

#### glTF 2.0 specifications
[glTF 2.0](https://github.com/KhronosGroup/glTF)

#### Blender integration requirements
[Requirements for contributed Scripts](https://wiki.blender.org/index.php/Dev:Py/Scripts/Guidelines/Addons)  
[Addons](https://wiki.blender.org/index.php/Dev:Doc/Process/Addons)  
