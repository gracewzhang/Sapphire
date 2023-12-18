import sys
from rich.console import Console
from rich.prompt import Prompt
from enum import Enum

console = Console()


class Color(Enum):
    SYSTEM = '[color(217)]'
    MENU = '[color(222)]'
    ERROR = '[color(160)]'
    PROMPT = '[color(153)]'
    COMMAND = '[black on color(217)]'


class CLI():
    def __init__(self, speaking_to_wizard: bool) -> None:
        self.speaking_to_wizard = speaking_to_wizard
        self.special_cmds = {
            'h;': self.__print_help_msg,
            'e;': self.__exit_sapphire,
            'w;': self.__switch_speaker,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        start_msg = ':sparkles: Welcome! Type in your desired command, and press enter when you\'re done :sparkles:'
        options = f'{Color.MENU.value}h;[/] - help menu\n' \
            + f'{Color.MENU.value}w;[/] - switch to {self.__get_speaker(True)}\n' \
            + f'{Color.MENU.value}e;[/] - exit'
        console.print(f'{Color.SYSTEM.value}{start_msg}')
        console.print(options)
        return None

    # TODO: write help message
    def __print_help_msg(self) -> None:
        help_msg = '[insert help msg]'
        console.print(help_msg)
        return None

    def __switch_speaker(self) -> None:
        self.speaking_to_wizard = not self.speaking_to_wizard
        speaker_msg = f'Now speaking to {self.__get_speaker()}'
        console.print(f'{Color.SYSTEM.value}{speaker_msg}')
        return 0

    def __get_speaker(self, next_speaker=False) -> None:
        if (self.speaking_to_wizard and not next_speaker) \
            or (not self.speaking_to_wizard and next_speaker):
            return ':owl: Wizard :owl:'
        return ':crystal_ball: Witch :crystal_ball:'

    def get_user_input(self) -> str:
        cmd = Prompt.ask(f'{Color.PROMPT.value}Command')
        if cmd in self.special_cmds:
            return self.special_cmds[cmd]()
        return cmd

    def __exit_sapphire(self) -> None:
        sys.exit(0)
