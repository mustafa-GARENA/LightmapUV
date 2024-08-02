import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator, Panel

class ImportUnwrapExportOperator(Operator):
    bl_idname = "object.import_unwrap_export"
    bl_label = "Import, Unwrap, Export"
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
                
                # Lightmap pack
                bpy.ops.uv.lightmap_pack(
                    PREF_CONTEXT='SEL_FACES', 
                    PREF_PACK_IN_ONE=True, 
                    PREF_NEW_UVLAYER=False, 
                    PREF_MARGIN_DIV=0.5, 
                    PREF_BOX_DIV=24
                )
                
                # Export the FBX file back to the same path
                bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True)
                
                # Delete the imported objects
                bpy.ops.object.select_all(action='DESELECT')
                for obj in imported_objects:
                    obj.select_set(True)
                bpy.ops.object.delete()

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(ImportUnwrapExportOperator.bl_idname)

# Register the operator and add to the menu
def register():
    bpy.utils.register_class(ImportUnwrapExportOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ImportUnwrapExportOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
    register()
