bl_info = {
    "name": "GoMod",
    "author": "Miguel Angel Garcia Serrano, MAGS VFX",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > GoMod",
    "description": "Adds the GoMod panel under Tool Shelf Tab. Creates modular assets easy in Blender",
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
        
        self.report({'INFO'}, 'Conformed!')
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
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.editmode_toggle()
        
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        
        self.report({'INFO'}, 'Converted to Mesh!')
        return {'FINISHED'}


# Panels with input UI
class AssetMakerPanel(Panel):
    """VIEW for GoMod Modular Visualization"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Maker'
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
        row.scale_y = 1.5
        row.operator('my.modroller', text='Mod Roller', icon='MOD_SHRINKWRAP')
        row.scale_y = 1.5
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
        
        self.report({'INFO'}, 'Group Selected!')
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
        
        self.report({'INFO'}, 'Grid Created!')
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
        
        self.report({'INFO'}, 'Line Created!')
        return {'FINISHED'}

# Custom SNAP TO PATH operator
class SnapOpe(Operator):
    """Activates snaping to path"""
    bl_idname = 'my.snapon'
    bl_label = 'To Center'
    
    def execute(self, context):
            
        obj = context.object
    
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'MEDIAN'
        

        self.report({'INFO'}, 'Snap On!')
        return {'FINISHED'}

# Custom UNSNAP TO PATH operator
class UnSnapOpe(Operator):
    """Deactivates snaping to path"""
    bl_idname = 'my.snapoff'
    bl_label = 'To Center'
    
    def execute(self, context):
            
        obj = context.object
    
        bpy.context.scene.tool_settings.use_snap = False
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'

        

        self.report({'INFO'}, 'Snap Off!')
        return {'FINISHED'}


# Panels with input UI
class AssetBuilderPanel(Panel):
    """VIEW for GoMod Modular Assets Builder"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Builder'
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
        row.label(text="Arrange Variations:")
        row = layout.row()
        row.scale_y = 1.5
        row.operator('my.grid', text='Grid Path', icon='MOD_LATTICE')
        row.scale_y = 1.5
        row.operator('my.line', text='Line Path', icon='MAN_SCALE')
        
        row = layout.row()
        row = layout.row()
        row.label(text='Snap to Path:')
        row = layout.row(align=True)
        row.label()
        row.scale_y = 1.5
        row.operator('my.snapon', text='On', icon='SNAP_ON')
        row.scale_y = 1.5
        row.operator('my.snapoff', text='Off', icon='SNAP_OFF')
        
        row.label()



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
        

        self.report({'INFO'}, 'Edit UVs!')
        return {'FINISHED'}

# Custom  SMOOTER operator
class SmootherOpe(Operator):
    """Aplies Subssurface and Edge Split Modifiers, smooth shade"""
    bl_idname = 'my.smooth'
    bl_label = 'To Center'
    
    
    def execute(self, context):
        obj = context.object
        bpy.ops.object.shade_smooth()
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subsurf"].levels = 1
        bpy.context.object.modifiers["Subsurf"].render_levels = 1
        bpy.context.object.modifiers["Subsurf"].show_expanded = False
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].show_expanded = False
                
        self.report({'INFO'}, 'Smoother Aplyed!')
        return {'FINISHED'}

# Custom  DISK operator
class DiskOpe(Operator):
    """Converts Curve to a solid Circle"""
    bl_idname = 'my.disk'
    bl_label = 'To Center'
    
    
    def execute(self, context):
        obj = context.object
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.fill_grid(span=12)
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.3
        bpy.context.object.modifiers["Solidify"].show_expanded = False
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        self.report({'INFO'}, 'Disk Ready!')
        return {'FINISHED'}

# Panels with input UI
class AssetToolsPanel(Panel):
    """VIEW for GoMod Modular Assets Builder"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'GoMod Asset Tools'
    bl_category = 'GoMod'
    
    # Draw UI elements here
    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row(align=True)
        
    
    # Get selected object
        obj = context.object

        # Panel Layouts
        
        row.scale_y = 2.0
        row.operator('my.uvwin', text='UV Editor', icon='UV_ISLANDSEL')
        row.scale_y = 2.0
        row.operator('my.smooth', text='Smoother', icon='SCULPTMODE_HLT')
        
        row = layout.row()
        row.scale_y = 2.0
        row.operator('my.disk', text='Disk', icon='SURFACE_NCIRCLE')
        row.label()


  
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
    bpy.utils.register_class(SnapOpe)
    bpy.utils.register_class(UnSnapOpe)
    bpy.utils.register_class(UvWinOpe)
    bpy.utils.register_class(SmootherOpe)
    bpy.utils.register_class(DiskOpe)
    
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
    bpy.utils.register_class(SnapOpe)
    bpy.utils.register_class(UnSnapOpe)
    bpy.utils.register_class(UvWinOpe)
    bpy.utils.unregister_class(SmootherOpe)
    bpy.utils.register_class(DiskOpe)
    
# Run Script in text editor
if __name__ == '__main__':
    register()
    
