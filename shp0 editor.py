import bpy
import struct

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

    
    
    def write_file_header(context, f, setting):
        f.write(struct.pack(">4s", b"SHP0")) # magic number
        f.write(struct.pack(">i", 0)) # placeholder for file length
        f.write(struct.pack(">i", setting.version)) # version number
        f.write(struct.pack(">i", 0)) # offset to brres file
        f.write(struct.pack(">4i", 0,0,0,0)) # placeholder for section offsets
        f.write(struct.pack(">i", 0)) #placeholder for offset to file name location in file
        
        #f.write(struct.pack(">4s", setting.filename))
        
    def write_shp0_header(context, f, setting):
        f.write(struct.pack(">i", 0))
        f.write(struct.pack(">H", setting.frame))
        f.write(struct.pack(">H", len(context.object.vertex_groups)))
        f.write(struct.pack(">i", setting.loop))    
        #need to check if works bc loop is bool => correctly translated to 0x00/0x01 ?


    def update_file_length(context, f, setting, offset_placement):
        length = f.tell()
        f.seek(offset_placement, 0)
        f.write(struct.pack(">i", length))
        offset_placement += 4
        f.seek(length, 0)
        
    
    
    def write_anim_data(context, f, setting, index):
        
        if context.object.vertex_groups.active_index != -1:
            #strange way to get the value: enable='OPT_A' (str) so enable[4]= 'A'
            #ord() to get the ascii value then -64 to get 1 => 0x02
            enable_value = 2**(ord(context.scene.animGroup[index].enable[4]) - 64)
            f.write(struct.pack(">i", enable_value)) #correct 0x0_ value ?
        else:
            f.write(struct.pack(">i", 0))
            print("No vertex group found, exported as 0")
        index += 1
        
        f.write(struct.pack(">i", 0)) #placeholder for vg name (name of the target vertex set) offset
        f.write(struct.pack(">H", index))
        f.write(struct.pack(">H", len(context.object.data.shape_keys.key_blocks)))
        
        f.write(struct.pack(">i", 0)) #placeholder for 0x0C
        f.write(struct.pack(">i", 0)) #placeholder for 0x10
        f.write(struct.pack(">i", 0))
        for i in range(len(context.object.data.shape_keys.key_blocks)):
            f.write(struct.pack(">i", 0)) #placeholder for 0x14 offsets
    
    
    
      
      
    def write_anim_entry(self, context, f, setting):
        obj = context.active_object
        #'if sk is not None:' not needed bc already checked in write_shp0_file        
        sk = obj.data.shape_keys
        anim = sk.animation_data
        if anim is not None:
            anim = anim.action
            if anim is not None:
                for fcu in anim.fcurves:
                    f.write(struct.pack(">H", 0)) #nb kf
                    f.write(struct.pack(">H", 0)) #padding?
                    f.write(struct.pack(">f", 0)) #float
                    for kf in fcu.keyframe_points:
                        f.write(struct.pack(">f", sk.key_blocks.frame)) #kf.index, surely not expected value
                        f.write(struct.pack(">f", sk.key_blocks.value)) #kf.value
                        f.write(struct.pack(">f", evaluate(kf)))
        else:
            self.report({'ERROR'}, "No animation found on active object")
            return {'CANCELLED'}

        return {'FINISHED'}
    
        #write_kf(context, f, setting)
    

    
    def write_vertex_data_names(context, f, setting):    #section 1
        Exportshp0.update_file_length(context, f, setting, 4)
        
    
    
    
    def write_shp0_file(self, context, setting):
        print("running write_shp0_file...")
        with open(self.filepath, 'wb') as f:
            nb = 4
            Exportshp0.write_file_header(context, f, setting)
            Exportshp0.write_shp0_header(context, f, setting)
            
            #Exportshp0.update_file_length(context, f, setting, nb*4+16)
            #Exportshp0.update_file_length(context, f, setting, nb*4+16)
            
            if context.object.data.shape_keys is not None:
                index = 0
                for sk in context.object.data.shape_keys.key_blocks:
                    Exportshp0.write_anim_data(context, f, setting, index)
                    Exportshp0.write_anim_entry(self, context, f, setting)
            else:
                self.report({'ERROR'}, "No shape key found on active object")
                return {'CANCELLED'}
            
            #for animations in animList
                #write anim header
                #write anim entry header
                #for kf in kfList
                    #write frame number, anim value, hermite slope interpolation
        
            Exportshp0.update_file_length(context, f, setting, 4)
        self.report({'INFO'}, ".shp0 exported successfully!")
        return {'FINISHED'}    
        
        
    def execute(self, context):
        return Exportshp0.write_shp0_file(self, context, context.scene.addonProps)



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
            for i in range (len(groups) - scene.animIndex):
                AnimManager.addAnim(self, context)
        elif(len(groups) < scene.animIndex):
            for i in range (scene.animIndex - len(groups)):
                AnimManager.removeAnim(self, context)
        return {'FINISHED'}
    
    
    def addAnim(self, context):
        scene = context.scene
        newAnim = scene.animGroup.add()
        newAnim.name = "Animation " + str(len(scene.animGroup) - 1)
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
        elif(groups.active_index > scene.animIndex):
            col.label(text="Please Update Animation first")
        else:
            col.prop(anim[groups.active_index], "enable")
        


    #how to use obj datas:
        #me = obj.data
        #groups = [obj.vertex_groups.active_index]
        #bpy.ops.object.mode_set(mode='OBJECT')
        #for v in me.vertices:
            #for g in v.groups:
                #if g.group in groups:
                    

    #def execute(self, context):
        #return write_shp0_file(context, self.filepath, self.use_setting)


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





'''
roadmap:
    + is done
    * partially done
    - needs to be done

    Priorities:
        verify is animation data/entry correctly written to file
        section 1
        update offsets

    
    section 0:
        file header (just need length of file update with                                           +
        ftell() then fseek(0x04) once all the file is written)
        
        shp0 header                                                                                 +
    
        Animation Data
            use of shape keys for animation entries
            0x00 bitflags                                                                           +
            (but still need the update animation button, hopefully find a way to get rid of it)
            and better coord between vg size and animIndex (off by 1 when size vg -1)               *
            
            0x04/8? name offset to section one vg name                                              *
            0x0A number of shape keys   (len(bpy.types.ShapeKey))                                   *
            
            0x0C-0x10-0x14 TBD                                                                      -
        
        Animation Entry
            "header"
                this shape key number of kf                                                         +
                padding                                                                             -
                1/(max kf number)                                                                   +
            followed by kf entries: (size N*12)
                frame number                                                                        +
                shape key animation value (0-1 morph)                                               +
                interpolation tangent value (f-curve or shapeKey.interpolation data struct?)        *
                
    section 1:
        list of vertex group names                                                                  -
            
        
    
    change animGroup to shape keys instead of vg ?
            
    Animation Data <=> shape keys
    Animations Entry <=> fcurve of shape key (animation data)
    keyframe <=> keyframe of fcurve (animation entry)
  
'''