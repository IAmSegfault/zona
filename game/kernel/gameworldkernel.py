from dataclasses import dataclass
from game.kernel.core import SceneKernel
from ecs.entities.player import PlayerCharacter
from ecs.entities.worldmap import WorldMap
from ecs.entities.camera import AsciiCamera
from ecs.components.metadata import MetaData


from typing import Any

@dataclass
class GameWorldKernel(SceneKernel):
    player: PlayerCharacter
    world_map: WorldMap
    loaded_superchunk: MetaData
    loaded_chunk: MetaData
    loaded_map: MetaData
    world_map_camera: AsciiCamera
    local_map_camera: AsciiCamera
    scene: Any
    at: MetaData = None
    player_state: str = "local_map"

    def syscall(self, call, *args, **kwargs):

        if call == "move_local":
            direction = kwargs["direction"]
            self.scene.map_events.move_local_map_start(scene=self.scene, direction=direction)
            self.scene.map_events.move_local_map_doing(scene=self.scene, direction=direction)
            self.scene.map_events.move_local_map_end(scene=self.scene, direction=direction)

        elif call == "mob_move_local":
            direction = kwargs["direction"]
            self.scene.map_events.mob_move_local_map_start(scene=self.scene, direction=direction)
            self.scene.map_events.mob_move_local_map_doing(scene=self.scene, direction=direction)
            self.scene.map_events.mob_move_local_map_end(scene=self.scene, direction=direction)

        elif call == "get_state":
            return self.scene.state

        elif call == "state_change":
            state = kwargs["state"]
            self.scene.state_change(state)

        elif call == "set_at":
            self.at = kwargs["at"]

        elif call == "get_at":
            return self.at

        elif call == "get_player_state":
            return self.player_state

        elif call == "set_player_state":
            self.player_state = kwargs["state"]
