from dataclasses import dataclass
from game.kernel.core import SceneKernel
from gui.menu import MessageLog, GameMenu

@dataclass
class UIKernel(SceneKernel):
    message_log: MessageLog
    game_menu: GameMenu

    def syscall(self, call, **kwargs):
        if call == "log_message":
            self.message_log.add_messages(kwargs["message"])