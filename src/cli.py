import sys
from rich.console import Console

console = Console()


class CLI():
    def __init__(self) -> None:
        self.special_cmds = {
            'h;': self.__print_help_msg,
            'e;': self.__exit_sapphire,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        start_msg = '=== Welcome! Type in your desired command, and press enter when you\'re done ===\n' \
            + ' \'h;\': help menu\n' \
            + ' \'e;\': exit'
        console.print(start_msg)

    def __print_help_msg(self) -> None:
        help_msg = '[insert help msg]'
        console.print(help_msg)

    def get_user_input(self) -> str:
        cmd = input()
        if cmd in self.special_cmds:
            self.special_cmds[cmd]()
            return None
        return cmd

    def __exit_sapphire(self) -> None:
        sys.exit(0)
