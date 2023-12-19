import sys
from rich.console import Console
from rich.prompt import Prompt
from enum import Enum
from utils import Agent, CommandStatus

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
    def __init__(self, active_agent, history: list) -> None:
        self.active_agent = active_agent
        self.history = history
        self.special_cmds = {
            'help;': self.__print_help_msg,
            'q;': self.__quit_sapphire,
            'w;': self.__switch_agent,
            'h;': self.__view_history,
            'u;': self.__trigger_reingest,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        start_msg = ':sparkles: Welcome! Type in your desired command, and press enter when you\'re done :sparkles:'
        console.print(f'{Color.SYSTEM.value}{start_msg}')
        self.__print_help_msg()
        return CLIResponse.IGNORE

    def __print_help_msg(self) -> None:
        options = f'{Color.MENU.value}help;[/] - help menu (what you\'re seeing right now)\n' \
            + f'{Color.MENU.value}w;[/] - switch to {self.__get_next_agent().value}\n' \
            + f'{Color.MENU.value}h;[/] - view history\n' \
            + f'{Color.MENU.value}u;[/] - update witch (aka reingest data)\n' \
            + f'{Color.MENU.value}q;[/] - quit'
        console.print(options)
        return CLIResponse.IGNORE

    def __get_next_agent(self) -> None:
        if self.active_agent == Agent.WIZARD:
            return Agent.WITCH
        return Agent.WIZARD

    def __switch_agent(self) -> None:
        self.active_agent = self.__get_next_agent()
        agent_msg = f'Now speaking to {self.active_agent.value}'
        console.print(f'{Color.SYSTEM.value}{agent_msg}')
        return CLIResponse.SWITCH

    def __view_history(self) -> None:
        prev_agent = self.active_agent
        self.active_agent = Agent.TIME_MACHINE
        console.print(':hourglass_not_done: Time Machine :hourglass_not_done:')
        time_machine_msg = f'Press {Color.MENU.value}enter[/] to view an earlier ' \
            + f'exchange or {Color.MENU.value}q;[/] to exit the time machine'
        console.print(time_machine_msg)

        idx = len(self.history) - 1
        while idx >= 0:
            record = self.history[idx]
            agent, user_req = record[0], record[1]
            console.print(f'{Color.PROMPT.value}User: {user_req}')

            if agent == Agent.WIZARD:
                wizard_cmd, cmd_status = record[2], record[3]
                if cmd_status == CommandStatus.EXECUTED:
                    console.print(f'{agent.value}: Executed {Color.COMMAND.value}{wizard_cmd}')
                elif cmd_status == CommandStatus.ABORTED:
                    console.print(f'{agent.value}: Aborted {wizard_cmd}')
                elif cmd_status == CommandStatus.INVALID:
                    console.print(f'{agent.value}: Invalid request')
            elif agent == Agent.WITCH:
                witch_ans = record[2]
                console.print(f'{agent.value}: {witch_ans}')

            idx -= 1
            response = self.get_user_input()
            if response == 'q;':
                self.active_agent = prev_agent
                return CLIResponse.IGNORE
        console.print(':hourglass_done: Reached the beginning of time :hourglass_done:')
        self.active_agent = prev_agent
        return CLIResponse.IGNORE

    def __trigger_reingest(self) -> None:
        return CLIResponse.REINGEST

    def get_user_input(self) -> str:
        if self.active_agent == Agent.TIME_MACHINE:
            cmd = Prompt.ask()
        else:
            if self.active_agent == Agent.WIZARD:
                cmd = Prompt.ask(f'{Color.PROMPT.value}:owl: Request')
            elif self.active_agent == Agent.WITCH:
                cmd = Prompt.ask(f'{Color.PROMPT.value}:crystal_ball: Question')

            if cmd in self.special_cmds:
                return self.special_cmds[cmd]()
        return cmd

    def __quit_sapphire(self) -> None:
        sys.exit(0)
