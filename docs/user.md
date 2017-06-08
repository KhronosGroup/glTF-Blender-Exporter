User Documentation
------------------

### Materials

### PBR Materials
At point of writing, the PBR materials are simulated with Cycles using a specific node tree encapsulated in a node group.
Two node groups are provided, one for the metallic roughness and one for the specular glossiness workflow.

Even possible in the Cycles node editor, specific requirements have to be fulfilled, that all parameters
are exported to the glTF 2.0 file format successfully.
TODO: Further explain.

All PBR materials share the same input parameters, which are listed in the following table.

|Material parameter export   |Node group only|Texture input only|Comments                               |
|----------------------------|:-------------:|:----------------:|---------------------------------------|
|Normal texture              |               |X                 |                                       |
|Normal strength             |X              |                  |                                       |
|Normal texture coordinate   |               |                  |'UV Map' input                         |
|Occlusion texture           |               |X                 |                                       |
|Occlusion strength          |X              |                  |                                       |
|Occlusion texture coordinate|               |                  |'UV Map' input                         |
|Emissive texture            |               |X                 |                                       |
|Emissive factor             |X              |                  |                                       |
|Emissive texture coordinate |               |                  |'UV Map' input                         |
|Alpha texture channel       |X              |                  |                                       |
|Alpha cutoff                |X              |                  |                                       |
|Alpha mode                  |X              |                  |                                       |
|Double sided                |X              |                  |                                       |
|COLOR_0                     |X              |                  |'Vertex Colors' name has to be 'COLOR_0|

![glTF Material Node](glTF_Material_Node_Part.png)

#### PBR Metallic Roughness

![glTF Metallic Roughness Node](glTF_Metallic_Roughness_Node.png)

#### PBR Specular Glossiness

#### Common Constant, Lmabert, Blinn and Phong
