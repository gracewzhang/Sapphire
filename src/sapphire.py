from openai import OpenAI
from cli import CLI, console, Color
from witch import Witch
from wizard import Wizard
import os
import sys


class Sapphire():
    def __init__(self) -> None:
        self.cli = CLI()
        client = self.__setup_connection()
        system = self.__detect_system()
        self.wizard = Wizard(client, system)
        self.witch = Witch(client)
        self.speaking_to_wizard = True

        self.start()

    def start(self) -> None:
        while True:
            cmd = self.cli.get_user_input()
            # cmd is a special command
            if cmd is None:
                continue
            if self.speaking_to_wizard:
                self.wizard.execute_cmd(cmd)
            else:
                self.witch.answer_question(cmd)

    def __setup_connection(self) -> OpenAI:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            console.print(
                f'{Color.ERROR.value}:pushpin: Make sure to add your OpenAI API KEY to your system environment as OPENAI_API_KEY. :pushpin:')
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
