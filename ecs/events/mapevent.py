import events
from ecs.components.position import MapPosition3D
from ecs.components.actor import Actor
from ecs.components.vicinity import Vicinity
from ecs.components.dimension import Rectangle
from game.util.camera import *


class MapEvents(events.Events):
    __events__ = ('move_chunk_start', 'move_chunk_doing', 'move_chunk_end', 'move_superchunk_start',
                  'move_superchunk_doing', 'move_superchunk_end', 'move_local_map_start', 'move_local_map_doing',
                  'move_local_map_end', 'mob_move_local_map_start', 'mob_move_local_map_doing', 'mob_move_local_map_end')


def m_local_move(local_pos, volume3d, direction):
    if direction == "east":
        if local_pos.x < volume3d.width - 1:
            local_pos.x += 1
            return True
        return False
    elif direction == "west":
        if local_pos.x > 0:
            local_pos.x -= 1
            return True
        return False
    elif direction == "north":
        if local_pos.z > 0:
            local_pos.z -= 1
            return True
        return False
    elif direction == "south":
        if local_pos.z < volume3d.length - 1:
            local_pos.z += 1
            return True
        return False
    elif direction == "northwest":
        if local_pos.z > 0 and local_pos.x > 0:
            local_pos.x -= 1
            local_pos.z -=1
            return True
        return False
    elif direction == "northeast":
        if local_pos.z > 0 and local_pos.x < volume3d.width - 1:
            local_pos.x += 1
            local_pos.z -=1
            return True
        return False
    elif direction == "southwest":
        if local_pos.z < volume3d.length - 1 and local_pos.x > 0:
            local_pos.x -= 1
            local_pos.z += 1
            return True
        return False

    elif direction == "southeast":
        if local_pos.z < volume3d.length - 1 and local_pos.x < volume3d.width - 1:
            local_pos.x += 1
            local_pos.z += 1
            return True
        return False

def mob_local_map_walk(**kwargs):
    scene = kwargs["scene"]
    direction = kwargs["direction"]
    is_walkable, vicinity = local_map_is_walkable(scene, direction)
    if is_walkable and is_walkable != "oob":
        local_map = scene.gwk.loaded_map
        a = scene.gwk.syscall("get_at")
        local_pos = scene.storage.component_for_entity(a.entity_id, MapPosition3D)
        volume3d = scene.storage.component_for_entity(local_map.entity_id, Volume3D)
        scene.graphics_dirty = m_local_move(local_pos, volume3d, direction)

def local_map_walk(**kwargs):
    scene = kwargs["scene"]
    direction = kwargs["direction"]
    is_walkable, vicinity = local_map_is_walkable(scene, direction)
    if is_walkable and is_walkable != "oob":
        camera = scene.gwk.local_map_camera.metadata
        local_map = scene.gwk.loaded_map
        player = scene.gwk.player
        player_local_pos = scene.storage.component_for_entity(player.metadata.entity_id, MapPosition3D)
        volume3d = scene.storage.component_for_entity(local_map.entity_id, Volume3D)
        viewport = scene.storage.component_for_entity(camera.entity_id, Rectangle)
        if direction == "east":
            scene.graphics_dirty = local_camera_center_move_east(viewport, player_local_pos, volume3d)

        elif direction == "west":
            scene.graphics_dirty = local_camera_center_move_west(viewport, player_local_pos)

        elif direction == "north":
            scene.graphics_dirty = local_camera_center_move_north(viewport, player_local_pos)

        elif direction == "south":
            scene.graphics_dirty = local_camera_center_move_south(viewport, player_local_pos, volume3d)

        elif direction == "northeast":
            scene.graphics_dirty = local_camera_center_move_northeast(viewport, player_local_pos, volume3d)

        elif direction == "northwest":
            scene.graphics_dirty = scene.graphics_dirty = local_camera_center_move_northwest(viewport, player_local_pos)

        elif direction == "southeast":
            scene.graphics_dirty = local_camera_center_move_southeast(viewport, player_local_pos, volume3d)

        elif direction == "southwest":
            scene.graphics_dirty = local_camera_center_move_southwest(viewport, player_local_pos, volume3d)

        walk_energy_deplete(scene=scene)

    elif not is_walkable and not vicinity.walkable:
        messages = ["OUCH! You bump into the %s." % vicinity.supertype]
        scene.uik.syscall("log_message", message=messages)

def walk_energy_deplete(**kwargs):
    scene = kwargs["scene"]
    a = scene.gwk.syscall("get_at")
    actor = scene.storage.component_for_entity(a.entity_id, Actor)
    actor.ct = actor.ct - 80
    if actor.ct > 60:
        actor.ct = 60
    if actor.ct < 0:
        actor.ct = 0

def local_map_is_walkable(scene, direction):
    map3d_metadata = scene.gwk.loaded_map
    a = scene.gwk.syscall("get_at")
    local_map_position = scene.storage.component_for_entity(a.entity_id, MapPosition3D)
    shape = map3d_metadata.containers["map_tiles"].shape
    posX = local_map_position.x
    posY = local_map_position.y
    posZ = local_map_position.z

    if direction == "east":
        posX += 1

    elif direction == "west":
        posX -= 1

    elif direction == "north":
        posZ -= 1

    elif direction == "south":
        posZ += 1

    elif direction == "northeast":
        posX += 1
        posZ -= 1

    elif direction == "northwest":
        posX -= 1
        posZ -= 1

    elif direction == "southeast":
        posX += 1
        posZ += 1

    elif direction == "southwest":
        posX -= 1
        posZ += 1

    if posX < 0 or posZ < 0 or posX > shape[0] - 1 or posZ > shape[2] - 1:
        return "oob", None
    target_map_tile_metadata = map3d_metadata.containers["map_tiles"][posX][posY][posZ]
    target_id = target_map_tile_metadata.entity_id
    vicinity = scene.storage.component_for_entity(target_id, Vicinity)
    if vicinity.walkable and len(target_map_tile_metadata.containers["actors"]) == 0:
        return True, None
    else:
        return False, vicinity