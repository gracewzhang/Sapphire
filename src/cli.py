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
    def __init__(self) -> None:
        self.special_cmds = {
            'h;': self.__print_help_msg,
            'e;': self.__exit_sapphire,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        start_msg = ':sparkles: Welcome! Type in your desired command, and press enter when you\'re done :sparkles:'
        options = f'{Color.MENU.value}h;[/] - help menu\n' \
            + f'{Color.MENU.value}e;[/] - exit'
        console.print(f'{Color.SYSTEM.value}{start_msg}')
        console.print(options)

    # TODO: write help message
    def __print_help_msg(self) -> None:
        help_msg = '[insert help msg]'
        console.print(help_msg)

    def get_user_input(self) -> str:
        cmd = Prompt.ask(f'{Color.PROMPT.value}Command')
        if cmd in self.special_cmds:
            self.special_cmds[cmd]()
            return None
        return cmd

    def __exit_sapphire(self) -> None:
        sys.exit(0)
