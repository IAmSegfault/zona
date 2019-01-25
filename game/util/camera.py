from ecs.components.dimension import Area2D


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