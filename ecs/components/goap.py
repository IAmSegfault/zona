from dataclasses import dataclass
from typing import Any
from abc import ABC

from game.util.search import *


class WorldState(object):
    def __init__(self, conditionname, callname, entity, tags, params, requirement):
        self.name = conditionname
        self.callname = callname
        self.entity = entity
        self.tags = tags
        self.params = params
        self.requirement = requirement

    def condition_met(self, gwk):
        if gwk.syscall(self.name, entity=self.entity, tags=self.tags, params=self.params) == self.requirement:
            return True
        else:
            return False
@dataclass
class Condition:
    name: str
    requirement: bool = True

class GOAPAction(ABC):
    def __init__(self, name, cost, cost_deprecation, failure_penalty, preconditions, effects, func, child_intent):
        self.name = name
        self.child_intent = child_intent
        self.base_cost = cost
        self.cost = cost
        self.cost_deprecation = cost_deprecation
        self.failure_penalty = failure_penalty
        self.preconditions = preconditions
        self.effects = effects
        self.failure = False
        self.action_name = func.__name__
        self.action_func = func

@dataclass
class Goal:
    action: Any
    original_intent: Any
    finished: bool = False

class GOAPBrain(object):
    def __init__(self, bored, actions):
        self.goals = []
        self.actions = actions
        self.bored_action = bored

    def emplace_action(self, action):
        intent = None
        if action.child_intent:
            intent = self.goals[-1].original_intent
        else:
            intent = len(self.goals) - 1
        goal = Goal(action, intent)
        self.goals.append(goal)

    def plan(self, gwk):
        graph = Graph()
        starting_actions = []
        final_action = self.goals[-1].action
        goal_actions = []

        for action in self.actions:
            # Check if this is an action that directly satisfies the goal
            action_effects = {condition.name for condition in action.effects if condition.requirement is True}
            required_effects = {precondition.name for precondition in final_action.preconditions if
                                type(precondition).__name__ == "Condition"}
            if action_effects == required_effects:
                goal_actions.append(action.name)

            # Check if this is a top level action that we can start from
            worldstates = [condition for condition in action.preconditions if type(condition).__name__ == 'WorldState']
            preconditions_met = True
            for worldstate in worldstates:
                if not worldstate.condition_met(gwk):
                    preconditions_met = False
                    break
            if len(worldstates) == 0:
                preconditions_met = False

            if preconditions_met:
                starting_actions.append(action.name)


            # Get all edges of the current action
            preconditions = {precondition.name for precondition in action.preconditions if type(precondition).__name__
                             == "Condition"}
            edges = []
            for edge in self.actions:
                edge_effects = {condition.name for condition in edge.effects}
                if edge_effects == preconditions:
                    edges.append(edge.name)

            # Populate the graph with the edges and cost of the current action
            graph.add_node(action.name, edges)
            graph.add_weight(action.name, action.cost)

        # Build a list of least costly chains of actions for each action that satisfies the goal
        action_list = []
        for goal_action in goal_actions:
            goal_paths = []
            for action in starting_actions:
                # Build a path
                came_from, cost_so_far = astar(graph, action, goal_action)
                action_path = reconstruct_path(came_from, action, goal_action)
                # Get the cost of the path and add it to the possible chains for the action that satisfies the goal
                totalcost = sum([v for k, v in cost_so_far.items() if k in action_path])
                goal_paths.append((totalcost, action_path))
            # Add the chain with the lowest cost to the list of chains that have low costs
            action_list.append(min(i for i in goal_paths))

        # Get the action chain with the lowest cost
        selected_action_path = min(i for i in action_list)
        selected_action_path = list(selected_action_path[1])

        # Add the chain to the GOAP
        while len(selected_action_path) > 0:
            action_name = selected_action_path.pop()
            for action in self.actions:
                if action.name == action_name:
                    self.emplace_action(action)
                    break







