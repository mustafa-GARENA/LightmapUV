import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator, Panel

class GenLightmapUVsOperator(Operator):
    bl_idname = "object.gen_lightmap_uvs"
    bl_label = "Gen Lightmap UVs"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(name="Directory", subtype='DIR_PATH')

    def execute(self, context):
        # Get the directory
        folder_path = self.directory
        
        # Iterate through all FBX files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.fbx'):
                file_path = os.path.join(folder_path, file_name)
                
                # Import the FBX file
                bpy.ops.import_scene.fbx(filepath=file_path)
                
                # Get the imported objects
                imported_objects = bpy.context.selected_objects[:]
                
                # Make a mesh object the active selection
                for obj in imported_objects:
                    if obj.type == 'MESH':
                        bpy.context.view_layer.objects.active = obj
                        break
                
                # Add UV channel
                bpy.ops.uv.textools_uv_channel_add()

                bpy.ops.object.mode_set(mode='EDIT')
                
                # Lightmap pack
                # bpy.ops.uv.lightmap_pack(
                #     PREF_CONTEXT='SEL_FACES', 
                #     PREF_PACK_IN_ONE=True, 
                #     PREF_NEW_UVLAYER=False, 
                #     PREF_MARGIN_DIV=0.5, 
                #     PREF_BOX_DIV=24
                # )

                bpy.ops.uv.smart_project()
                bpy.ops.uvpackeroperator.packbtn()
                
                bpy.ops.object.mode_set(mode='OBJECT')

                # Export the FBX file back to the same path
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True)
                
                # Delete the imported objects
                bpy.ops.object.select_all(action='DESELECT')
                for obj in imported_objects:
                    obj.select_set(True)
                bpy.ops.object.delete()

                bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(GenLightmapUVsOperator.bl_idname)

# Register the operator and add to the menu
def register():
    bpy.utils.register_class(GenLightmapUVsOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
    bpy.utils.unregister_class(GenLightmapUVsOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
    register()
