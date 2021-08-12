import sys
from colorama import Fore, init
from random import choice


def error(message):
    print(f"{Fore.RED}{message}{Fore.RESET}")


def info(message):
    print(f"{Fore.CYAN}{message}{Fore.RESET}")


def warning(message):
    print(f"{Fore.YELLOW}{message}{Fore.RESET}")


def success(message):
    print(f"{Fore.GREEN}{message}{Fore.RESET}")


def help():
    info("Help menu")
    info("-en     --enable-numbers        Enable number characters")
    info("-eu     --enable-upper          Enable uppercase characters")
    info("-es     --enable-symbols        Enables ASCII symbol characters")
    info("size    size=n                  Sets the size of the string to generate")


class ArgumentProcessor:

    def __init__(self, tl: list):
        self.__list_tokens = tl

    def process(self):
        values = {}
        params = []
        for item in self.__list_tokens:
            if item.startswith("--"):
                params.append(item)
            elif item[0] == '-' and item[1] != '-':
                params.append(item)
            else:
                if '=' in item:
                    chunks = item.split("=")
                    values[chunks[0]] = chunks[1]
        return tuple(params), values


class Genpass:

    def __init__(self):
        # default size
        self.__types = {'lower': True, 'upper': False, 'symbol': False, 'number': False}
        self.__size = 10

    def __generate_lower(self) -> str:
        return choice(range(97, 123))

    def __generate_upper(self) -> str:
        return choice(range(65, 91))

    def __generate_symbol(self) -> str:
        symbol_list = [range(32, 48), range(58, 65), range(91, 97), range(123, 127)]
        return choice(choice(symbol_list))

    def __generate_number(self) -> str:
        return choice(range(48, 58))

    def __get_secure_char(self) -> int:
        enabled = False
        type = ""
        while not enabled:
            keys = list(self.__types.keys())
            type = choice(keys)
            enabled = self.__types[type]
        if type == 'upper':
            return self.__generate_upper()
        elif type == 'lower':
            return self.__generate_lower()
        elif type == 'symbol':
            return self.__generate_symbol()
        elif type == 'number':
            return self.__generate_number()
        else:
            return 32

    def set_size(self, size: int):
        self.__size = size

    def enable(self, e_type: str):
        if e_type == 'uppercase':
            self.__types['upper'] = True
        elif e_type == 'symbols':
            self.__types['symbol'] = True
        elif e_type == 'numbers':
            self.__types['number'] = True

    def execute(self) -> str:
        string = ""
        for index in range(self.__size):
            string += chr(self.__get_secure_char())
        return string


def main(args: list):
    if len(args) > 0:
        if args[0] == '--help' or args[0] == '-h':
            help()
        else:
            params, values = ArgumentProcessor(args).process()
            if "size" in values:
                generator = Genpass()
                if '-es' in params or '--enable-symbols' in params:
                    generator.enable('symbols')
                if '-en' in params or '--enable-numbers' in params:
                    generator.enable('numbers')
                if '-eu' in params or '--enable-uppercase' in params:
                    generator.enable('uppercase')
                generator.set_size(int(values['size']))
                success(generator.execute())
            else:
                error("Error: a valid size was not specified")
    else:
        error("Error: no arguments specified")


if __name__ == '__main__':
    args = sys.argv
    del args[0]
    init()
    main(args)
