from cli import CLI
from sapphire import Sapphire


def main():
    sapphire = Sapphire()
    cli = CLI()

    while True:
        cmd = cli.get_user_input()
        # cmd is a special command
        if cmd is None:
            continue
        
        sapphire.execute_cmd(cmd)

if __name__ == '__main__':
    main()
