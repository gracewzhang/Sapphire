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


class CLIResponse(Enum):
    IGNORE = 0
    SWITCH = 1
    REINGEST = 2


class CLI():
    def __init__(self, speaking_to_wizard: bool) -> None:
        self.speaking_to_wizard = speaking_to_wizard
        self.special_cmds = {
            'help;': self.__print_help_msg,
            'q;': self.__quit_sapphire,
            'w;': self.__switch_speaker,
            'h;': self.__view_history,
            'r;': self.__trigger_reingest,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        start_msg = ':sparkles: Welcome! Type in your desired command, and press enter when you\'re done :sparkles:'
        console.print(f'{Color.SYSTEM.value}{start_msg}')
        self.__print_help_msg()
        return CLIResponse.IGNORE

    def __print_help_msg(self) -> None:
        options = f'{Color.MENU.value}help;[/] - help menu (what you\'re seeing right now)\n' \
            + f'{Color.MENU.value}w;[/] - switch to {self.__get_speaker(True)}\n' \
            + f'{Color.MENU.value}h;[/] - view history\n' \
            + f'{Color.MENU.value}r;[/] - update witch (aka reingest data)\n' \
            + f'{Color.MENU.value}q;[/] - quit'
        console.print(options)
        return CLIResponse.IGNORE

    def __switch_speaker(self) -> None:
        self.speaking_to_wizard = not self.speaking_to_wizard
        speaker_msg = f'Now speaking to {self.__get_speaker()}'
        console.print(f'{Color.SYSTEM.value}{speaker_msg}')
        return CLIResponse.SWITCH

    def __get_speaker(self, next_speaker=False) -> None:
        if (self.speaking_to_wizard and not next_speaker) \
            or (not self.speaking_to_wizard and next_speaker):
            return ':owl: Wizard :owl:'
        return ':crystal_ball: Witch :crystal_ball:'

    def __view_history(self) -> None:
        console.print('===Time machine===')
        idx = len(self.history) - 1
        while True and idx >= 0:
            console.print(self.history[idx])
            idx -= 1
        return CLIResponse.IGNORE

    def __trigger_reingest(self) -> None:
        return CLIResponse.REINGEST

    def get_user_input(self) -> str:
        speaker_emoji = ':owl:' if self.speaking_to_wizard else ':crystal_ball:'
        cmd = Prompt.ask(f'{Color.PROMPT.value}{speaker_emoji} Command')
        if cmd in self.special_cmds:
            return self.special_cmds[cmd]()
        return cmd

    def __quit_sapphire(self) -> None:
        sys.exit(0)
