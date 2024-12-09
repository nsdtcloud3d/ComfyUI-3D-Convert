

class ConvertTo3DFormat:
    """
    target_type suppoet : 'gltf, obj, glb, ply, stl, xyz, off, dae, amf, 3mf, step, iges, fbx'
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)

    FUNCTION = "main_func"
    CATEGORY = "3DConvert"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"forceInput": True, "multiline": True}),
                "file_path": ("STRING",{"forceInput":True,"multiline": False}),
                "target_type": (["gltf", "glb", "obj", "ply", "stl", "xyz", "off", "dae", "amf", "3mf", "step", "iges", "fbx"],),
            }
        }

    def main_func(self, file_path, target_type, api_key):
        """
        TODO call NSDT API convert 3d file to target type 
        """
        print(f"file_path: {file_path}, target_type: {target_type}, api_key: {api_key}")
        return (file_path,)

class Load3DFile:
    """
    load 3d file. 
    import file format support  'glb, gltf, ply, stl, obj, off, dae, fbx, dxf, ifc, xyz, pcd, las, laz, stp, step, 3dxml, iges, igs, shp, geojson, xaml, pts, asc, brep, fcstd, bim, usdz, pdb, vtk, svg, wrl, 3dm, 3ds, amf, 3mf, dwg, json, rfa, rvt'
    """
     
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)

    FUNCTION = "main_func"
    CATEGORY = "3DConvert"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"multiline": True})
            }
        }

    def main_func(self, file_path):
        """
        TODO check file type 
        """
        print(f"##########convert Load3DFile  {file_path}")
        return (file_path,)


class Load3DConvertAPIKEY:
    """
    3D convert need a apikey , Get your API KEY from: https://3dconvert.nsdt.cloud/
    """

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_key",)
    FUNCTION = "main_func"
    CATEGORY = "3DConvert"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"default": "Get your API KEY from: https://3dconvert.nsdt.cloud/", "multiline": True})
            },
        }

    def main_func(self, api_key):
        return (api_key,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ConvertTo3DFormat": ConvertTo3DFormat,
    "Load3DConvertAPIKEY": Load3DConvertAPIKEY,
    "Load3DFile": Load3DFile
}
