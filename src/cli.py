import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from enum import Enum
from utils import Agent, CommandStatus, Model, Color, get_next_agent

console = Console()


class CLIResponse(Enum):
    IGNORE = 0
    REINGEST = 1


class CLI():
    def __init__(self, history: {}, get_agent, set_agent, get_model, set_model) -> None:
        self.history = history
        self.get_agent = get_agent
        self.set_agent = set_agent
        self.get_model = get_model
        self.set_model = set_model
        self.special_cmds = {
            'help;': self.__print_help_msg,
            'q;': self.__quit_sapphire,
            'w;': self.__switch_agent,
            'h;': self.__view_history,
            'm;': self.__switch_model,
            'r;': self.__trigger_reingest,
        }
        self.__print_start_msg()

    def __print_start_msg(self) -> None:
        logo = '''
  ______                   _     _
 / _____)                 | |   (_)
( (____  _____ ____  ____ | |__  _  ____ _____
 \____ \(____ |  _ \|  _ \|  _ \| |/ ___) ___ |
 _____) ) ___ | |_| | |_| | | | | | |   | ____|
(______/\_____|  __/|  __/|_| |_|_|_|   |_____)
              |_|   |_|
'''
        start_msg = ':sparkles: Welcome! Type in your desired command, and press enter when you\'re done :sparkles:'
        logo = Align.center(f'{Color.MENU.value}{logo}')
        console.print(logo)
        console.print(f'{Color.SYSTEM.value}{start_msg}')
        self.__print_help_msg()
        return CLIResponse.IGNORE

    def __print_help_msg(self) -> None:
        next_agent_str = get_next_agent(self.get_agent()).value
        model = self.get_model().value
        options = \
            f'{Color.MENU.value}help;[/] - help menu (what you\'re seeing right now)\n' \
            + f'{Color.MENU.value}w;[/] - switch to the {next_agent_str}\n' \
            + f'{Color.MENU.value}h;[/] - view history\n' \
            + f'{Color.MENU.value}r;[/] - reingest data\n' \
            + f'{Color.MENU.value}m;[/] - switch OpenAI model (currently using {model})\n' \
            + f'{Color.MENU.value}q;[/] - quit'
        console.print(Panel(options))
        return CLIResponse.IGNORE

    def __switch_agent(self) -> None:
        self.set_agent(get_next_agent(self.get_agent()))
        agent_msg = f'Now speaking to {self.get_agent().value}'
        console.print(f'{Color.SYSTEM.value}{agent_msg}')
        return CLIResponse.IGNORE

    def __view_history(self) -> None:
        agent = self.get_agent()
        history = self.history[agent]
        time_machine_msg = \
            f'{Color.SYSTEM.value}Viewing chat history with the[/] {self.get_agent().value}\n' \
            + f'Press {Color.MENU.value}enter[/] to view an earlier ' \
            + f'exchange or {Color.MENU.value}q;[/] to exit the time machine'
        console.print('─' * os.get_terminal_size().columns)
        console.print(time_machine_msg)

        idx = len(history) - 1
        while idx >= 0:
            record = history[idx]
            user_req = record[0]
            exchange = f'{Color.PROMPT.value}User:[/] {user_req}\n'

            if agent == Agent.WIZARD:
                wizard_cmd, cmd_status = record[1], record[2]
                if cmd_status == CommandStatus.EXECUTED:
                    exchange += f'Executed {Color.COMMAND.value}{wizard_cmd}'
                elif cmd_status == CommandStatus.ABORTED:
                    exchange += f'Aborted {wizard_cmd}'
                elif cmd_status == CommandStatus.INVALID:
                    exchange += 'Invalid request'
            elif agent == Agent.WITCH:
                witch_ans = record[1]
                exchange += witch_ans

            console.print(Panel(exchange, title=agent.value))
            response = self.get_user_input(Agent.TIME_MACHINE)
            if response == 'q;':
                break
            idx -= 1

        if idx < 0:
            console.print(
                f'{Color.SYSTEM.value}Reached the beginning of time with the {agent.value}')

        console.print('─' * os.get_terminal_size().columns)
        return CLIResponse.IGNORE

    def __trigger_reingest(self) -> None:
        #        return CLIResponse.REINGEST
        # TODO: https://github.com/langchain-ai/langchain/issues/14872
        console.print(f'{Color.SYSTEM.value}At the time, you can manually reingest ' \
                      + 'by deleting the .sapphire directory in your current path.')
        return CLIResponse.IGNORE

    def __switch_model(self) -> None:
        new_model_str = self.get_user_input(Agent.MODEL_SWITCHER)
        new_model = Model(new_model_str)
        self.set_model(new_model)
        switch_msg = f'Successfully switched to {new_model_str}'
        console.print(f'{Color.SYSTEM.value}{switch_msg}')
        return CLIResponse.IGNORE

    def get_user_input(self, agent: Agent) -> str:
        if agent == Agent.TIME_MACHINE:
            cmd = input()
        elif agent == Agent.MODEL_SWITCHER:
            choices = [x.value for x in Model]
            cmd = Prompt.ask('Select your model of choice', choices=choices)
        else:
            if agent == Agent.WIZARD:
                cmd = Prompt.ask(f'{Color.PROMPT.value}:owl: Request')
            elif agent == Agent.WITCH:
                cmd = Prompt.ask(f'{Color.PROMPT.value}:crystal_ball: Question')

            if cmd in self.special_cmds:
                return self.special_cmds[cmd]()
        return cmd

    def __quit_sapphire(self) -> None:
        sys.exit(0)
