from openai import OpenAI
from utils import Agent
from cli import CLI, console, Color, CLIResponse
from witch import Witch
from wizard import Wizard
import os
import sys


class Sapphire():
    def __init__(self) -> None:
        client = self.__setup_connection()
        system = self.__detect_system()
        directory = os.getcwd()
        self.active_agent = Agent.WIZARD
        self.history = []

        self.cli = CLI(self.active_agent, self.history)
        self.wizard = Wizard(client, system, self.history, Agent.WIZARD)
        self.witch = Witch(client, directory, self.history, Agent.WITCH)

        self.start()

    def start(self) -> None:
        while True:
            cmd = self.cli.get_user_input()
            # cmd is a special command
            if cmd == CLIResponse.IGNORE:
                continue
            if cmd == CLIResponse.SWITCH:
                # TODO: figure out a way to avoid storing 2 speaking_to_wizard booleans
                self.active_agent = Agent.WITCH if self.active_agent == Agent.WIZARD \
                    else Agent.WIZARD
            # reingest documents
            elif cmd == CLIResponse.REINGEST:
                self.witch.reingest()
            elif self.active_agent == Agent.WIZARD:
                self.wizard.execute_cmd(cmd)
            else:
                self.witch.answer_question(cmd)

    def __setup_connection(self) -> OpenAI:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            console.print(f'{Color.ERROR.value}:pushpin: Make sure to add your OpenAI API KEY to your system environment as OPENAI_API_KEY. :pushpin:')
            sys.exit(0)
        return OpenAI(api_key=api_key)

    def __detect_system(self) -> str | None:
        platform = sys.platform
        if platform.startswith('linux'):
            return 'Linux'
        elif platform.startswith('darwin'):
            return "MacOS"
        elif platform .startswith('win32'):
            return 'Windows'
        else:
            console.print(
                f'{Color.ERROR.value}User platform is incompatible with Sapphire :(')
            sys.exit(0)
