from enum import Enum


class Model(Enum):
    THREE_FIVE_TURBO = 'gpt-3.5-turbo'
    FOUR = 'gpt-4'
    FOUR_TURBO = 'gpt-4-turbo'


class Color(Enum):
    SYSTEM = '[color(217)]'
    MENU = '[color(222)]'
    ERROR = '[color(160)]'
    PROMPT = '[color(153)]'
    COMMAND = '[black on color(217)]'
    WIZARD = '[color(36)]'
    WITCH = '[color(134)]'


class Agent(Enum):
    WIZARD = f'{Color.WIZARD.value}:owl: Wizard :owl:[/]'
    WITCH = f'{Color.WITCH.value}:crystal_ball: Witch :crystal_ball:[/]'
    TIME_MACHINE = ':hourglass: Time Machine :hourglass:'
    MODEL_SWITCHER = 'Model Switcher'


def get_next_agent(agent: Agent) -> Agent:
    if agent == Agent.WIZARD:
        return Agent.WITCH
    return Agent.WIZARD


class CommandStatus(Enum):
    EXECUTED = 0
    ABORTED = 1
    INVALID = 2
