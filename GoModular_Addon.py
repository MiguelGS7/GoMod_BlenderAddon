bl_info = {
    "name": "GoMod",
    "author": "Miguel Angel Garcia Serrano, MAGS VFX",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > GoMod",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
from bpy.types import Panel, Operator
from rna_prop_ui import PropertyPanel

#________________________ GOMOD ASSET MAKER ________________________
# Custom CONFORM operator
class ConformOpe(Operator):
    """Prepare selected object for modular"""
    bl_idname = 'my.conform'
    bl_label = 'To Center'
    
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.location_clear(clear_delta=False)
        bpy.ops.object.rotation_clear(clear_delta=False)
        bpy.ops.object.scale_clear(clear_delta=False)
        
        self.report({'INFO'}, 'Conform Ready!')
        return {'FINISHED'}
    
# Custom MODULAR ROLLER operator
class ModRollerOpe(Operator):
    """Visualizes selected object in a modular roller"""
    bl_label = 'Roller'
    bl_idname = 'my.modroller'
    
    def execute(self, context):
        obj = context.object
        
        a = bpy.context.active_object.name
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].show_expanded = False
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array.001"].count = 3
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        bpy.context.object.modifiers["Array.001"].show_expanded = False
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.ops.curve.primitive_bezier_circle_add(radius=5)
        
        b = bpy.context.active_object.name
        
        bpy.context.scene.objects.active = bpy.data.objects[a]
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects[b]
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects[b]
        bpy.ops.transform.resize(value=(1.01922, 1.01922, 1.01922))

        
        bpy.context.object.modifiers["Curve"].show_expanded = False
        
        self.report({'INFO'}, 'Modular Finished!')
        return {'FINISHED'}

# Custom MODULAR WALL operator
class ModWallOpe(Operator):
    """Visualizes selected object in a modular wall"""
    bl_label = 'Wall'
    bl_idname = 'my.modwall'
    
    def execute(self, context):
        obj = context.object
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 10
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1
        bpy.context.object.modifiers["Array"].show_expanded = False
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array.001"].count = 4
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        bpy.context.object.modifiers["Array.001"].show_expanded = False
        
        self.report({'INFO'}, 'Modular Finished!')
        return {'FINISHED'}

# Custom CONVER TO PIECES operator
class ConvPiecesOpe(Operator):
    """Convert modular visualization to individual objects"""
    bl_idname = 'my.convpieces'
    bl_label = 'To Center'
    
    def execute(self, context):
        obj = context.object
        bpy.context.object.show_wire = False
        bpy.context.object.show_bounds = False
        bpy.ops.object.convert(target='MESH')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        
        self.report({'INFO'}, 'Converted to Pieces!')
        return {'FINISHED'}

# Custom CONVER TO MESH operator
class ConvMeshOpe(Operator):
    """Convert modular visualization to single object"""
    bl_idname = 'my.convmesh'
    bl_label = 'To Center'
    
    def execute(self, context):
        obj = context.object
        bpy.context.object.show_wire = False
        bpy.context.object.show_bounds = False
        bpy.ops.object.convert(target='MESH')
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        
        self.report({'INFO'}, 'Converted to Mesh!')
        return {'FINISHED'}


# Panels with input UI
class AssetMakerPanel(Panel):
    """VIEW for GoMod Modular Visualization"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Maker'
    bl_context = 'objectmode'
    bl_category = 'GoMod'
    
    # Draw UI elements here
    def draw(self, context,):
        layout = self.layout
        

        # Get selected object
        obj = context.object
        
        # Panel Layouts
        row = layout.row()
        row.label(text="Active object: " + obj.name, icon='SOLO_ON')
        
        row = layout.row()
        row.operator('my.conform', text='Conform Object', icon='BBOX')
        row = layout.row()     
        row.operator('my.modroller', text='Mod Roller', icon='MOD_SHRINKWRAP')
        row.operator('my.modwall', text='Mod Wall', icon='MOD_BUILD')
        
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.prop(obj, "show_wire", text="Wire")
        row.prop(obj, "show_bounds", text="Bounds")
        layout.row().column().prop(context.object, "scale")
        row = layout.row()
        row = layout.row()
        
        row.label(text="Convert to: ")
        row = layout.row()
        
        row.scale_y = 2.0
        row.operator('my.convpieces', text='Pieces', icon='OUTLINER_OB_FORCE_FIELD')
        
        row.scale_y = 2.0
        row.operator('my.convmesh', text='Mesh', icon='OUTLINER_OB_GROUP_INSTANCE')
        row = layout.row()
        



#________________________ GOMOD ASSET BUILDER ________________________
# Custom GROUP operator
class GroupOpe(Operator):
    """Creates an object group from selected objects"""
    bl_idname = 'my.group'
    bl_label = 'To Center'
    
    def execute(self, context):
        obj = context.object
        bpy.ops.group.create()
        
        self.report({'INFO'}, 'Group Created!')
        return {'FINISHED'}

# Custom SELECT GROUP operator
class SelecGroupOpe(Operator):
    """Select all objects in group"""
    bl_idname = 'my.selecgr'
    bl_label = 'To Center'
    
    def execute(self, context):
        obj = context.object
        bpy.ops.object.select_grouped(type='GROUP')
        
        self.report({'INFO'}, 'Group Created!')
        return {'FINISHED'}

# Custom GRID operator
class GridOpe(Operator):
    """Creates a mesh grid, align selected mesh variations"""
    bl_idname = 'my.grid'
    bl_label = 'To Center'
    
    def execute(self, context):
        obj = context.object
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=6, y_subdivisions=5, radius=12, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, 'Group Created!')
        return {'FINISHED'}

# Custom LINE operator
class LineOpe(Operator):
    """Creates a mesh line, align selected mesh variations"""
    bl_idname = 'my.line'
    bl_label = 'To Center'
    
    
    def execute(self, context):
        obj = context.object
        bpy.ops.curve.primitive_nurbs_path_add(radius=30, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.object.convert(target='MESH')
        
        self.report({'INFO'}, 'Group Created!')
        return {'FINISHED'}

# Custom RANDOMIZE operator
class RandomOpe(Operator):
    """Randomize Transform, for selected object"""
    bl_idname = 'my.random'
    bl_label = 'To Center'
    
    
    def execute(self, context):
        obj = context.object
        bpy.ops.object.randomize_transform()
        
        self.report({'INFO'}, 'Randomize!')
        return {'FINISHED'}


# Panels with input UI
class AssetBuilderPanel(Panel):
    """VIEW for GoMod Modular Assets Maker"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Builder'
    bl_context = 'objectmode'
    bl_category = 'GoMod'
    
    # Draw UI elements here
    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row(align=True)
        
        
    
    # Get selected object
        obj = context.object

        # Panel Layouts
        row.operator('my.group', text='Group Selected', icon='FILE_TICK')
        row = layout.row()
        
        # Displays selected GROUP Name
        obj_name = obj.name
        for group in bpy.data.groups:
            group_objects = group.objects
            if obj_name in group.objects and obj in group_objects[:]:
                col = layout.column(align=True)

                col.context_pointer_set("group", group)
                
                row = col.box().row()
                row.prop(group, "name", text="", icon='GROUP')
                row.operator("object.group_remove", text="", icon='X', emboss=False)
                row.operator('my.selecgr', text='Select', icon='RESTRICT_SELECT_OFF')
        
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.label(text="Arranged Variations:")
        row = layout.row()
        row.scale_y = 2.0
        row.operator('my.grid', text='Grid Path', icon='MOD_LATTICE')
        row.scale_y = 2.0
        row.operator('my.line', text='Line Path', icon='MAN_SCALE')
        row = layout.row()
        row.operator('my.random', text='Randomize', icon='RNDCURVE')

        
#________________________ GOMOD ASSET TOOLS ________________________        

# Custom UV WINDOW operator
class UvWinOpe(Operator):
    """Split area and opens UV Maps Editor"""
    bl_idname = 'my.uvwin'
    bl_label = 'To Center'
    
    def execute(self, context):
            
        obj = context.object
    
        bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
        bpy.context.area.type = 'IMAGE_EDITOR'
        

        self.report({'INFO'}, 'Group Created!')
        return {'FINISHED'}

# Panels with input UI
class AssetToolsPanel(Panel):
    """VIEW for GoMod Modular Assets Builder"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Tools'
    bl_context = 'objectmode'
    bl_category = 'GoMod'
    
    # Draw UI elements here
    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row(align=True)
        
        
    
    # Get selected object
        obj = context.object

        # Panel Layouts
        row.label()
    
        sub = row.row()
        sub.scale_y = 2.0
        sub.scale_x = 5.0
        sub.operator('my.uvwin', text='UV Editor', icon='UV_VERTEXSEL')
        
        row.label()
        row = layout.row()

  
# Register
class register():
    bpy.utils.register_class(AssetMakerPanel)
    bpy.utils.register_class(AssetBuilderPanel)
    bpy.utils.register_class(AssetToolsPanel)
    bpy.utils.register_class(ConformOpe)
    bpy.utils.register_class(ModRollerOpe)
    bpy.utils.register_class(ModWallOpe)
    bpy.utils.register_class(ConvPiecesOpe)
    bpy.utils.register_class(ConvMeshOpe)
    bpy.utils.register_class(GroupOpe)
    bpy.utils.register_class(GridOpe)
    bpy.utils.register_class(LineOpe)
    bpy.utils.register_class(SelecGroupOpe)
    bpy.utils.register_class(RandomOpe)
    bpy.utils.register_class(UvWinOpe)
    
# Unregister
def unregister():
    bpy.utils.unregister_class(AssetMakerPanel)
    bpy.utils.unregister_class(AssetBuilderPanel)
    bpy.utils.unregister_class(AssetToolsPanel)
    bpy.utils.unregister_class(ConformOpe)
    bpy.utils.unregister_class(ModRollerOpe)
    bpy.utils.unregister_class(ModWallOpe)
    bpy.utils.unregister_class(ConvPiecesOpe)
    bpy.utils.unregister_class(ConvMeshOpe)
    bpy.utils.unregister_class(GroupOpe)
    bpy.utils.unregister_class(GridOpe)
    bpy.utils.unregister_class(LineOpe)
    bpy.utils.unregister_class(SelecGroupOpe)
    bpy.utils.unregister_class(RandomOpe)
    bpy.utils.register_class(UvWinOpe)
    
# Run Script in text editor
if __name__ == '__main__':
    register()
    