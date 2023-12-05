from openai import OpenAI
from cli import console
import os
import sys
import subprocess


class Sapphire():
    def __init__(self) -> None:
        self.__setup_connection()
        self.__detect_system()
        self.msgs = [{'role': 'system', 'content':
                      'You are an intelligent assistant named Sapphire that helps the \
                      user execute command line commands to manage their desktop'}]

    def __setup_connection(self) -> None:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            console.print(
                'Make sure to add your OpenAI API KEY to your system environment as OPENAI_API_KEY.')
            sys.exit(0)
        self.client = OpenAI(api_key=api_key)

    def __detect_system(self) -> None:
        platform = sys.platform
        if platform.startswith('linux'):
            self.system = 'Linux'
        elif platform.startswith('darwin'):
            self.system = "MacOS"
        elif platform .startswith('win32'):
            self.system = 'Windows'
        else:
            console.print('User platform is incompatible with Sapphire :(')
            sys.exit(0)

    def execute_cmd(self, user_cmd) -> None:
        sapphire_cmd = self.__get_sapphire_cmd(user_cmd)
        if sapphire_cmd.startswith('Invalid command'):
            console.print('Please enter a valid command.')
        elif self.__greenlight_sapphire_cmd(sapphire_cmd):
            subprocess.call(sapphire_cmd, shell=True)
        else:
            console.print('=== Aborting ===')

    def __greenlight_sapphire_cmd(self, sapphire_cmd) -> bool:
        console.print(f'Executing {sapphire_cmd}... [Y/N]')
        res = input()
        if res == 'Y' or res == 'y':
            return True
        return False

    def __get_sapphire_cmd(self, user_cmd) -> str:
        cmd = f'What is the script in a {self.system} environment to execute the following command:' \
            + f'"{user_cmd}". Reply with just the command and no additional text.' \
            + 'If it is not possible to answer with a command line command, reply with' \
            + '"Invalid command"'
        self.msgs.append({'role': 'user', 'content': cmd})
        chat = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.msgs
        )
        reply = chat.choices[0].message.content
        self.msgs.append({'role': 'assistant', 'content': reply})
        return reply
