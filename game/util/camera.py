from ecs.components.dimension import Area2D, Volume3D


def camera_center_move_east(viewport, player_world_pos, world_map_area=Area2D(64, 64)):
    if player_world_pos.x < world_map_area.width - 1:
        player_world_pos.x += 1
        viewport.x1 += 1
        viewport.x2 += 1
        return True
    return False


def camera_center_move_west(viewport, player_world_pos):
    if player_world_pos.x > 0:
        player_world_pos.x -= 1
        viewport.x1 -= 1
        viewport.x2 -= 1
        return True
    return False


def camera_center_move_north(viewport, player_world_pos):
    if player_world_pos.y > 0:
        player_world_pos.y -= 1
        viewport.y1 -= 1
        viewport.y2 -= 1
        return True
    return False


def camera_center_move_south(viewport, player_world_pos, world_map_area=Area2D(64, 64)):
    if player_world_pos.y < world_map_area.height - 1:
        player_world_pos.y += 1
        viewport.y1 += 1
        viewport.y2 += 1
        return True
    return False


def camera_center_move_northwest(viewport, player_world_pos):
    if player_world_pos.x > 0 and player_world_pos.y > 0:
        camera_center_move_north(viewport, player_world_pos)
        camera_center_move_west(viewport, player_world_pos)
        return True
    return False

def camera_center_move_northeast(viewport, player_world_pos, world_map_area=Area2D(64, 64)):
    if player_world_pos.y > 0 and player_world_pos.x < world_map_area.width - 1:
        camera_center_move_north(viewport, player_world_pos)
        camera_center_move_east(viewport, player_world_pos, world_map_area)
        return True
    return False

def camera_center_move_southwest(viewport, player_world_pos, world_map_area=Area2D(64, 64)):
    if player_world_pos.y < world_map_area.height - 1 and player_world_pos.x > 0:
        camera_center_move_south(viewport, player_world_pos, world_map_area)
        camera_center_move_west(viewport, player_world_pos)
        return True
    return False


def camera_center_move_southeast(viewport, player_world_pos, world_map_area=Area2D(64, 64)):
    if player_world_pos.y < world_map_area.height - 1 and player_world_pos.x < world_map_area.width - 1:
        camera_center_move_south(viewport, player_world_pos, world_map_area)
        camera_center_move_east(viewport, player_world_pos, world_map_area)
        return True
    return False


def local_camera_center_move_east(viewport, player_local_pos, local_map_volume=Volume3D(128, 64, 128)):
    if player_local_pos.x < local_map_volume.width - 1:
        player_local_pos.x += 1
        viewport.x1 += 1
        viewport.x2 += 1
        return True
    return False


def local_camera_center_move_west(viewport, player_local_pos):
    if player_local_pos.x > 0:
        player_local_pos.x -= 1
        viewport.x1 -= 1
        viewport.x2 -= 1
        return True
    return False


def local_camera_center_move_north(viewport, player_local_pos):
    if player_local_pos.z > 0:
        player_local_pos.z -= 1
        viewport.y1 -= 1
        viewport.y2 -= 1
        return True
    return False


def local_camera_center_move_south(viewport, player_local_pos, local_map_volume=Volume3D(128, 64, 128)):
    if player_local_pos.z < local_map_volume.length - 1:
        player_local_pos.z += 1
        viewport.y1 += 1
        viewport.y2 += 1
        return True
    return False


def local_camera_center_move_northwest(viewport, player_local_pos):
    if player_local_pos.x > 0 and player_local_pos.z > 0:
        local_camera_center_move_north(viewport, player_local_pos)
        local_camera_center_move_west(viewport, player_local_pos)
        return True
    return False


def local_camera_center_move_northeast(viewport, player_local_pos, local_map_volume=Volume3D(128, 64, 128)):
    if player_local_pos.z > 0 and player_local_pos.x < local_map_volume.width - 1:
        local_camera_center_move_north(viewport, player_local_pos)
        local_camera_center_move_east(viewport, player_local_pos, local_map_volume)
        return True
    return False


def local_camera_center_move_southwest(viewport, player_local_pos, local_map_volume=Volume3D(128, 64, 128)):
    if player_local_pos.z < local_map_volume.length - 1 and player_local_pos.x > 0:
        local_camera_center_move_south(viewport, player_local_pos, local_map_volume)
        local_camera_center_move_west(viewport, player_local_pos)
        return True
    return False


def local_camera_center_move_southeast(viewport, player_local_pos, local_map_volume=Volume3D(128, 64, 128)):
    if player_local_pos.z < local_map_volume.length - 1 and player_local_pos.x < local_map_volume.width - 1:
        local_camera_center_move_south(viewport, player_local_pos, local_map_volume)
        local_camera_center_move_east(viewport, player_local_pos, local_map_volume)
        return True
    return False