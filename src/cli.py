import sys


class CLI():
    def __init__(self) -> None:
        self.special_cmds = {
            'h;': self.print_help_msg,
            'e;': self.exit_sapphire,
        }
        self.print_start_msg()

    def print_start_msg(self) -> None:
        start_msg = '=== Welcome! Type in your desired command, and press enter when you\'re done ===\n' \
            + ' \'h;\': help menu\n' \
            + ' \'e;\': exit'
        print(start_msg)

    def print_help_msg(self) -> None:
        help_msg = '[insert help msg]'
        print(help_msg)

    def get_user_input(self) -> str:
        cmd = input()
        if cmd in self.special_cmds:
            self.special_cmds[cmd]()
        return cmd

    def exit_sapphire(self) -> None:
        sys.exit(0)
