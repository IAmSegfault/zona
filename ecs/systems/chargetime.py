import esper
import operator
from ecs.components.metadata import MetaData
from ecs.components.actor import Actor


class CTProcessor(esper.Processor):
    def __init__(self, resolution_threshold=100):
        super().__init__()
        self.cache = []
        self.resolution_threshold = resolution_threshold

    def process(self, *args, **kwargs):
        if kwargs["render"]:
            return
        else:
            gwk = kwargs["gwk"]
            if gwk.syscall("get_state") != "ct_await":
                if gwk.syscall("get_state") != "player_at":
                    if gwk.syscall("get_state") != "npc_at":
                        self.cache.clear()
                        return

            if len(self.cache) == 0:
                at = False
                while not at:
                    for entity, (metadata, actor) in self.world.get_components(MetaData, Actor):
                        actor.ct += actor.speed
                    for entity, (metadata, actor) in self.world.get_components(MetaData, Actor):
                        if actor.ct >= self.resolution_threshold:
                            self.cache.append((entity, metadata, actor))
                            at = True

                if len(self.cache) > 0:
                    self.cache.sort(key=operator.itemgetter(0), reverse=True)
                    if gwk.syscall("get_state") == "ct_await":
                        e = self.cache.pop()
                        gwk.syscall("set_at", at=e[1])
                        if e[2].is_playercharacter:
                            gwk.syscall("state_change", state="player_at")
                            return
                        else:
                            gwk.syscall("state_change", state="npc_at")
                            return

            elif gwk.syscall("get_state") == "ct_await":
                e = self.cache.pop()
                gwk.syscall("set_at", at=e[1])
                if e[2].is_playercharacter:
                    gwk.syscall("state_change", state="player_at")
                else:
                    gwk.syscall("state_change", state="npc_at")






