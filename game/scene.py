import esper
from abc import ABC, abstractmethod
from settings import PERSISTENT_STORAGE


class Scene(ABC):

    def __init__(self, manager):
        super().__init__()
        self.is_init = False
        self.storage = esper.World()
        self.state = "init"
        self.prev_state = "init"
        self.manager = manager
        self.persistent_storage = PERSISTENT_STORAGE
        self.console = {}
        self.input_action_queue = {}

    @abstractmethod
    def state_change(self, state):
        self.prev_state = self.state
        self.state = state
        for key, c in self.console.items():
            c.clear()

    def add_system(self, system, priority=0):
        self.storage.add_processor(system, priority)

    def delete_entity(self, entity):
        self.storage.delete_entity(entity)

    def add_component(self, id, component):
        self.storage.add_component(id, component)

    def remove_component(self, id, component):
        self.storage.remove_component(id, component)

    @abstractmethod
    def handle_input(self, key):
        pass

    @abstractmethod
    def init_scene(self):
        pass

    @abstractmethod
    def enter_scene(self):
        pass

    @abstractmethod
    def exit_scene(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

class SceneManager(object):
    def __init__(self):
        self.scenes = {}
        self.current_scene = ""

    def add_scene(self, name, scene):
        if name not in self.scenes:
            self.scenes[name] = scene

    def remove_scene(self, name):
        if name in self.scenes and self.current_scene != name:
            self.scenes[name].destroy()
            del self.scenes[name]

    def set_scene(self, name):
        if name in self.scenes and name != self.current_scene:
            if self.current_scene != "":
                self.scenes[self.current_scene].exit_scene()

            self.current_scene = name

            if not self.scenes[self.current_scene].is_init:
                self.scenes[self.current_scene].init_scene()
                self.scenes[self.current_scene].is_init = True

            self.scenes[self.current_scene].enter_scene()

