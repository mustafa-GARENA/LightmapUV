import bpy
import os
import time
from bpy.props import StringProperty
from bpy.types import Operator, Panel
import struct

class GenLightmapUVsOperator(Operator):
    bl_idname = "object.gen_lightmap_uvs"
    bl_label = "Gen Lightmap UVs"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(name="Directory", subtype='DIR_PATH')

    def execute(self, context):
        # Get the directory
        bpy.context.scene.unit_settings.scale_length = 0.01
        folder_path = self.directory

        #clear the scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Iterate through all FBX files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.fbx'):
                file_path = os.path.join(folder_path, file_name)
                
                #perform a preclean
                bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

                bpy.ops.import_scene.fbx(filepath=file_path)
                
                # Get the imported objects
                imported_objects = bpy.context.selected_objects[:]
                
                # Make a mesh object the active selection to supply proper context
                for obj in imported_objects:
                    if obj.type == 'MESH':
                        bpy.context.view_layer.objects.active = obj
                        break
                
                bpy.ops.uv.textools_uv_channel_add()

                bpy.ops.object.mode_set(mode='EDIT') # switch to edit mode to perform UV operations
                
                bpy.ops.uv.smart_project(angle_limit=1.53589, margin_method='SCALED', rotate_method='AXIS_ALIGNED_Y', island_margin=0.0, area_weight=1.0, correct_aspect=True, scale_to_bounds=False)

                #UV Packer Settings
                bpy.context.scene.UVPackerProps.uvp_combine = False
                bpy.context.scene.UVPackerProps.uvp_width = 512
                bpy.context.scene.UVPackerProps.uvp_height = 512
                bpy.context.scene.UVPackerProps.uvp_engine = 'OP1'
                bpy.context.scene.UVPackerProps.uvp_padding = 4
                bpy.ops.uvpackeroperator.packbtn()

                print('Packing......')
                time.sleep(5) # time to complete packing
                print('Packing Complete')
                
                bpy.ops.object.mode_set(mode='OBJECT')

                # Export the FBX file back to the same path
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True)
                
                # Delete the imported objects
                bpy.ops.object.select_all(action='DESELECT')
                for obj in imported_objects:
                    obj.select_set(True)
                bpy.ops.object.delete()


        print('Complete!')
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
