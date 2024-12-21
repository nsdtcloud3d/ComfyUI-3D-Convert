
from .util.nsdt import upload_file_to_nsdt, convert_to_target_file
import os.path
import  uuid

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
        call NSDT API convert 3d file to target type
        """
        print(f"file_path: {file_path}, target_type: {target_type}, api_key: {api_key}")

        if file_path is None or os.path.exists(file_path) is None:
            return

        if api_key is None:
            return (file_path,)

        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        extension = extension[1:] if extension else ""

        file_hash = str(uuid.uuid4())
        
        # need fileHash 
        comment = f"""{{"convertType": "{target_type}", "from": "comfyUI-3D-Convert", "fileHash": "{file_hash}"}}"""

        directory = os.path.dirname(os.path.abspath(file_path))
        file_name = os.path.basename(file_path)
        new_file_path = os.path.join(directory, f'{file_name}.{target_type}')
        resp = upload_file_to_nsdt(file_path, extension, api_key, comment)

        if resp['done'] == 1:
            blob_id = resp['blob_id']
            print(f'file upload success: {blob_id}')
            target_path = convert_to_target_file(api_key, target_type, blob_id, new_file_path)
            if target_path is not None:
                return target_path

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
