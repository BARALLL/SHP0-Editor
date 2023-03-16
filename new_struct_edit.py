import bpy

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator




class Exportshp0(bpy.types.Operator, ExportHelper):
    """Export SHP0"""
    bl_idname = "export.shp0"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export shp0"
    filename_ext = ".shp0"

    def execute(self, context):
        return write_shp0_file(context, self.filepath, self.setting)
    
    
    
    def write_shp0_file(context, filepath, setting):
        print("running write_shp0_file...")
        file = open(filepath, 'w', encoding='utf-8')
        
        write_shp0_header(context, file, setting)
        
        #for animations in animList
            #write anim header
            #write anim entry header
            #for kf in kfList
                #write frame number, anim value, hermite slope interpolation
        
        file.close()

        return {'FINISHED'}
    
    
    
    def write_shp0_header(context, file, setting):
        f.write(struct.pack("<4s", b"SHP0")) # magic number
        f.write(struct.pack("<i", 0)) # placeholder for file length
        f.write(struct.pack("<i", setting.version)) # SHP0 version number
        f.write(struct.pack("<i", 0)) # offset to BRRES file
        f.write(struct.pack("<4i", 0)) # placeholder for section offsets
        f.write(struct.pack("<4s", setting.filename))



class Anim(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Name")
    lock : bpy.props.BoolProperty(name='Lock', default=False, description="So that you don't accidentally delete your animation (even if UNDO works)")
    enable: bpy.props.EnumProperty(name="Enable", description="Enable Update",
    items=(
        ('OPT_A', "Enable position update", "0x02"),
        ('OPT_B', "Enable normal update", "0x04"),
        ('OPT_C', "Enable vertex color update", "0x08"),
    ),
    default='OPT_A')
    

    

class settings(bpy.types.PropertyGroup):

    #File variables
    
    filename: bpy.props.StringProperty(name="File Name", description="name under which the file will be exported")
    loop : bpy.props.BoolProperty(name='Loop', default=False, description="Does the animation should loop?")
    version: bpy.props.IntProperty(name='Version', min = 1, max = 15, default=4,  description="Version number. It is recommended to leave it at 4, other versions are unknown")
    frame: bpy.props.IntProperty(name='Number of frames', default=58,  description="Number of frames of the animation")


     
      
      
      
      
class AnimManager(bpy.types.Operator):
    bl_idname = "anim.update"
    bl_label = "Update Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        groups = context.object.vertex_groups
        
        if(len(groups) > scene.animIndex):
            AnimManager.addAnim(self, context)
        elif(len(groups) < scene.animIndex):
            AnimManager.removeAnim(self, context)
        return {'FINISHED'}
    
    
    def addAnim(self, context):
        scene = context.scene
        newAnim = scene.animGroup.add()
        newAnim.name = "Animation " + str(len(scene.animGroup) - 1)
        newAnim.enable
        scene.animIndex = len(scene.animGroup) - 1
        return {'FINISHED'}
    
    
    def removeAnim(self, context):
        scene = context.scene
        animIndex = scene.animIndex
        if(animIndex >= 0 and not scene.animGroup[animIndex].lock):
            scene.animGroup.remove(animIndex)
            scene.animIndex = min(animIndex, len(scene.animGroup) - 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

            
            

class EditorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "SHP0 Editor"
    bl_idname = "OBJECT_PT_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SHP0 Editor"
    

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        layout.label(text="Vertex Morph Editor", icon='RENDER_ANIMATION')
        layout.label(text="Active object is: " + obj.name)
        
        param = scene.addonProps
        anim = scene.animGroup
        groups = obj.vertex_groups

        
        layout.prop(param, "filename")
        row = layout.row()
        row.prop(param, "version")
        row.prop(param, "loop")
        col = layout.column()
        col.prop(param, "frame")
                  
        col.label(text="Current Vertex Group : " + str(groups.active_index))
        
        layout.operator('export.shp0')
        layout.operator('anim.update')
        if(groups.active_index == -1):
            col.label(text="Please add a vertex group first")
        else:
            col.prop(anim[groups.active_index], "enable")

    #how to use obj datas:
        #me = obj.data
        #groups = [obj.vertex_groups.active_index]
        #bpy.ops.object.mode_set(mode='OBJECT')
        #for v in me.vertices:
            #for g in v.groups:
                #if g.group in groups:
                    

    def execute(self, context):
        return write_shp0_file(context, self.filepath, self.use_setting)


classes = [AnimManager, Exportshp0, Anim, settings, EditorPanel]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)
    
    bpy.types.Scene.addonProps = bpy.props.PointerProperty(type=settings)
    bpy.types.Scene.animGroup = bpy.props.CollectionProperty(type=Anim)
    bpy.types.Scene.animIndex = bpy.props.IntProperty()


def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)

    del bpy.types.Scene.addonProps
    
    del bpy.types.Scene.animGroup
    del bpy.types.Scene.animIndex


if __name__ == "__main__":
    register()
