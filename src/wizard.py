from openai import OpenAI
from cli import console, Color
import subprocess
from rich.prompt import Confirm


class Wizard():
    def __init__(self, client: OpenAI, system: str) -> None:
        self.client = client
        self.system = system
        self.msgs = [{'role': 'system', 'content':
                      'You are an intelligent assistant named Sapphire that helps the \
                      user execute command line commands to manage their desktop'}]

    def execute_cmd(self, user_cmd) -> None:
        sapphire_cmd = self.__get_sapphire_cmd(user_cmd)
        if sapphire_cmd.startswith('Invalid command'):
            console.print(f'{Color.ERROR.value}Please enter a valid command.')
        elif self.__greenlight_sapphire_cmd(sapphire_cmd):
            subprocess.call(sapphire_cmd, shell=True)
        else:
            console.print(
                f'{Color.ERROR.value}:stop_sign: Aborting :stop_sign:')

    def __greenlight_sapphire_cmd(self, sapphire_cmd) -> bool:
        greenlit = Confirm.ask(
            f':dango: Execute {Color.COMMAND.value}{sapphire_cmd}')
        return greenlit

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
