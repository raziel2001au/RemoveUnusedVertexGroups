bl_info = {
    "name": "Remove unused Vertex Groups",
    "author": "CoDEmanX (ported to Blender 2.8 by raziel2001au)",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "Properties Editor > Object data > Vertex Groups > Specials menu",
    "description": "Delete the Vertex Groups with no assigned weights from the active object",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"
}

import bpy
from bpy.types import Operator

class OBJECT_OT_vertex_group_remove_unused(Operator):
    bl_idname = "object.vertex_group_remove_unused"
    bl_label = "Remove unused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def execute(self, context):

        ob = context.object
        ob.update_from_editmode()
        
        vgs = ob.vertex_groups
        vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
        
        for v in ob.data.vertices:
            for g in v.groups:
                if g.weight > 0.0:
                    vgroup_used[g.group] = True
                    g_name = vgs[g.group].name
                    if g_name.endswith(".L"):
                        vgroup_used[vgs.find(g_name[0:-1] + "R")] = True
                    if g_name.endswith(".R"):
                        vgroup_used[vgs.find(g_name[0:-1] + "L")] = True
                    if g_name.endswith(".l"):
                        vgroup_used[vgs.find(g_name[0:-1] + "r")] = True
                    if g_name.endswith(".r"):
                        vgroup_used[vgs.find(g_name[0:-1] + "l")] = True
        
        for i, used in sorted(vgroup_used.items(), reverse=True):
            if not used:
                ob.vertex_groups.remove(ob.vertex_groups[i])
                
        return {'FINISHED'}


def draw_func(self, context):
    self.layout.operator(
        OBJECT_OT_vertex_group_remove_unused.bl_idname,
        icon='X'
    )


def register():
    from bpy.utils import register_class
    register_class(OBJECT_OT_vertex_group_remove_unused)
    bpy.types.MESH_MT_vertex_group_context_menu.prepend(draw_func)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(OBJECT_OT_vertex_group_remove_unused)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(draw_func)


if __name__ == "__main__":
    register()
