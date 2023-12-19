from enum import Enum


class Agent(Enum):
    WIZARD = ':owl: Wizard :owl:'
    WITCH = ':crystal_ball: Witch :crystal_ball:'
    TIME_MACHINE = ':hourglass: Time Machine :hourglass:'


def get_next_agent(agent: Agent) -> Agent:
    if agent == Agent.WIZARD:
        return Agent.WITCH
    return Agent.WIZARD


class CommandStatus(Enum):
    EXECUTED = 0
    ABORTED = 1
    INVALID = 2
