from dataclasses import dataclass

@dataclass
class SceneKernel(object):
    userspace: dict
    program_count: int
