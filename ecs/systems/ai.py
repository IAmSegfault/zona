import esper
from ecs.components.goap import *

class GOAPSystem(esper.Processor):
    def __init__(self, gwk, uik):
        self.gwk = gwk
        self.uik = uik


    def take_action(self, brain):
        if len(brain.goals) > 0:
            while len(brain.goals) > 0 and brain.goals[-1].finished:
                brain.goals.pop()
        else:
            brain.goals.append(brain.bored_goal)
            brain.plan(self.gwk)

        brain.goals[-1].action.action_func(brain=brain, goal=brain.goals[-1], gwk=self.gwk)
        if brain.goals[-1].action.failure:
            brain.goals[-1].action.cost += brain.goals[-1].action.failure_penalty
            brain.goals[-1].action.failure = False
            failed_goal = brain.goals.pop()
            while len(brain.goals) - 1 > failed_goal.original_intent:
                brain.goals.pop()

    def process(self, *args, **kwargs):
        if kwargs["render"]:
            return
        else:
            if self.gwk.syscall("get_state") == "npc_at":
                mob_metadata = self.gwk.syscall("get_at")
                brain = self.world.component_for_entity(mob_metadata.entity_id, GOAPBrain)

                for action in brain.actions:
                    if action.cost > action.base_cost:
                        action.cost -= action.cost_deprecation
                    else:
                        action.cost = action.base_cost
                self.take_action(brain)

            
