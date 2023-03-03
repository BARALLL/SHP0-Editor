import bpy


from bpy_extras.io_utils import ExportHelper


class settings(bpy.types.PropertyGroup):

    #File variables
    filename: bpy.props.StringProperty(name="File Name", description="name under which the file will be exported")
    loop : bpy.props.BoolProperty(name='Loop', default=False, description="Does the animation should loop?")
    version: bpy.props.IntProperty(name='Version', min = 1, max = 15, default=4,  description="Version number. It is recommended to leave it at 4, other versions are unknown")
    frame: bpy.props.IntProperty(name='Number of frames', default=58,  description="Number of frames of the animation")


class KeyFrameData(bpy.types.PropertyGroup):
    #Key frame variables
    name : bpy.props.StringProperty(name="Name")
    currFrame: bpy.props.IntProperty(name='Current frame', min = 0, default=0,  description="Current frame number")
    value: bpy.props.FloatProperty(name='Animation value', min = 0, max = 1, default=0,  description="How far the target vertices have to be morphed into the destination vertices")
    slope: bpy.props.FloatProperty(name='Slope', default=0,  description="Hermite interpolation slope value")
    

class AnimEntry(bpy.types.PropertyGroup):
    #Animation entry variables
    name : bpy.props.StringProperty(name="Name")
    kfGroup : bpy.props.CollectionProperty(type=KeyFrameData)
    kfIndex: bpy.props.IntProperty()
    dest: bpy.props.StringProperty(name="Set of destination vertices", description="Name of the set of destination vertices (name of the Shape Key)")



class Anim(bpy.types.PropertyGroup):
    #Animation variables
    name : bpy.props.StringProperty(name="Name")
    lock : bpy.props.BoolProperty(name='Lock', default=False, description="So that you don't accidentally delete your animation (even if UNDO works)")
    source: bpy.props.StringProperty(name="Set of source vertices", description="Name of the set of source vertices (usually Basis)")
    enable: bpy.props.EnumProperty(name="Enable", description="Enable Update",
    items=(
        ('OPT_A', "Enable position update", "0x02"),
        ('OPT_B', "Enable normal update", "0x04"),
        ('OPT_C', "Enable vertex color update", "0x08"),
    ),

    default='OPT_A')    

    #Animation entry variables
    entryGroup : bpy.props.CollectionProperty(type=AnimEntry)
    entryIndex: bpy.props.IntProperty()


    




class AnimList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            if not item:
                row.label(text="", translate=False)
                return
            row.prop(item, "name", text="", emboss=False)







class AnimAdd(bpy.types.Operator):
    bl_idname = "anim.add"
    bl_label = "Add Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        newAnim = scene.animGroup.add()
        newAnim.name = "Animation " + str(len(scene.animGroup) - 1)
        scene.animIndex = len(scene.animGroup) - 1
        return {'FINISHED'}

class AnimRemove(bpy.types.Operator):
    bl_idname = "anim.remove"
    bl_label = "Remove Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        animIndex = scene.animIndex
        if(animIndex >= 0 and not scene.animGroup[animIndex].lock):
            scene.animGroup.remove(animIndex)
            scene.animIndex = min(animIndex, len(scene.animGroup) - 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}




class EntryAdd(bpy.types.Operator):
    bl_idname = "entry.add"
    bl_label = "Add Animation Entry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        animGroup = scene.animGroup[scene.animIndex]
        newAnim = animGroup.entryGroup.add()
        newAnim.name = "Animation Entry " + str(len(animGroup.entryGroup) - 1)
        animGroup.entryIndex = len(animGroup.entryGroup) - 1
        return {'FINISHED'}

class EntryRemove(bpy.types.Operator):
    bl_idname = "entry.remove"
    bl_label = "Remove Animation Entry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        animGroup = scene.animGroup[scene.animIndex]
        entryIndex = animGroup.entryIndex
        if(entryIndex >= 0):
            animGroup.entryGroup.remove(entryIndex)
            animGroup.entryIndex = min(entryIndex, len(animGroup.entryGroup) - 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}




class KeyFrameAdd(bpy.types.Operator):
    bl_idname = "kf.add"
    bl_label = "Add Key Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        animGroup = scene.animGroup[scene.animIndex]
        entryGroup = scene.animGroup[scene.animIndex].entryGroup[animGroup.entryIndex]
        newAnim = entryGroup.kfGroup.add()
        newAnim.name = "Key Frame " + str(len(entryGroup.kfGroup) - 1)
        entryGroup.kfIndex = len(entryGroup.kfGroup) - 1
        return {'FINISHED'}

class KeyFrameRemove(bpy.types.Operator):
    bl_idname = "kf.remove"
    bl_label = "Remove Key Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        animGroup = scene.animGroup[scene.animIndex]
        entryGroup = scene.animGroup[scene.animIndex].entryGroup[animGroup.entryIndex]

        kfIndex = entryGroup.kfIndex
        if(kfIndex >= 0):
            entryGroup.kfGroup.remove(kfIndex)
            entryGroup.kfIndex = min(kfIndex, len(entryGroup.kfGroup) - 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}




    
    

def write_shp0_header(context, file):
    pass
    

def write_shp0_file(context, filepath, setting):
    print("running write_shp0_file...")
    file = open(filepath, 'w', encoding='utf-8')
    
    write_shp0_header(context, file)
    
    #for animations in animList
        #write anim header
        #write anim entry header
        #for kf in kfList
            #write frame number, anim value, hermite slope interpolation
    
    file.write("Hello World %s" % setting)
    
    file.close()

    return {'FINISHED'}






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
        
        layout.prop(param, "filename")
        row = layout.row()
        row.prop(param, "version")
        row.prop(param, "loop")
        col = layout.column()
        col.prop(param, "frame")
        
        layout.operator('export.shp0')
        

class AnimationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Animation Panel"
    bl_idname = "OBJECT_PT_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SHP0 Editor"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        

        row = layout.row()
        col = row.column()
        col.template_list("AnimList", "", context.scene, "animGroup", context.scene, "animIndex")
        col = row.column(align=True)
        col.operator("anim.add", icon='ADD', text="")
        col.operator("anim.remove", icon='REMOVE', text="")

        currentIndex = context.scene.animIndex
        
        if(currentIndex >= 0):
            currentGroup = context.scene.animGroup[currentIndex]
            if(currentGroup.lock):
                col.prop(currentGroup, "lock", icon='PINNED', text="")
            else:
                col.prop(currentGroup, "lock", icon='UNPINNED', text="")
            layout.prop(currentGroup, "source")
            layout.prop(currentGroup, "enable")
            col = layout.column(align=True)
        else:
            layout.label(text='Start by adding a Animation')
                  
            

class AnimEntryPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Animation Entry Panel"
    bl_idname = "OBJECT_PT_entry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SHP0 Editor"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        
        if(len(context.scene.animGroup) > 0):
            
            currentAnimGroup = scene.animGroup[scene.animIndex]
            
            row = layout.row()
            col = row.column()
            col.template_list("AnimList", "", currentAnimGroup, "entryGroup", currentAnimGroup, "entryIndex")
            col = row.column(align=True)
            col.operator("entry.add", icon='ADD', text="")
            col.operator("entry.remove", icon='REMOVE', text="")
        
            if(len(currentAnimGroup.entryGroup) > 0):
                col = layout.column(align=True)
                col.prop(currentAnimGroup.entryGroup[currentAnimGroup.entryIndex], "dest")    
            else:
                layout.label(text='Start by adding a Animation Entry')
        else:
            layout.label(text='Start by adding a Animation')




class KeyFramePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Key Frame Panel"
    bl_idname = "OBJECT_PT_kf"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SHP0 Editor"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
    

        if(len(context.scene.animGroup) > 0):
            
            currentAnimGroup = scene.animGroup[scene.animIndex]

            if(len(currentAnimGroup.entryGroup) > 0):

                currentGroup = currentAnimGroup.entryGroup[currentAnimGroup.entryIndex]

                row = layout.row()
                col = row.column()
                col.template_list("AnimList", "", currentGroup, "kfGroup", currentGroup, "kfIndex")
                col = row.column(align=True)
                col.operator("kf.add", icon='ADD', text="")
                col.operator("kf.remove", icon='REMOVE', text="")

                if(len(currentGroup.kfGroup) > 0):
                    col = layout.column(align=True)
                    col.prop(currentGroup.kfGroup[currentGroup.kfIndex], "dest")
                    col.prop(currentGroup.kfGroup[currentGroup.kfIndex], "currFrame")
                    col.prop(currentGroup.kfGroup[currentGroup.kfIndex], "value")
                else:
                    layout.label(text='Start by adding a Key Frame')
            else:
                layout.label(text='Start by adding a Animation Entry')
        else:
            layout.label(text='Start by adding a Animation')





class Exportshp0(bpy.types.Operator, ExportHelper):
    """Export SHP0"""
    bl_idname = "export.shp0"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export shp0"
    filename_ext = ".shp0"

    def execute(self, context):
        return write_shp0_file(context, self.filepath, self.str)






classes = [Exportshp0, EditorPanel, AnimationPanel, AnimEntryPanel, KeyFramePanel, settings, 
            KeyFrameData, AnimEntry, Anim, AnimList, AnimAdd, AnimRemove, EntryAdd, EntryRemove, KeyFrameAdd, KeyFrameRemove]

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
