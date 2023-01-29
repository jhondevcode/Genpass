#!/usr/bin/python3

import sys
from random import choice

color_module = False
try:
    from colorama import Fore, init
    color_module = True
except:
    color_module = False

def error(message):
    if color_module:
        print(f"{Fore.RED}{message}{Fore.RESET}")
    else:
        print(message)


def info(message):
    if color_module:
        print(f"{Fore.CYAN}{message}{Fore.RESET}")
    else:
        print(message)


def warning(message):
    if color_module:
        print(f"{Fore.YELLOW}{message}{Fore.RESET}")
    else:
        print(message)


def success(message):
    if color_module:
        print(f"{Fore.GREEN}{message}{Fore.RESET}")
    else:
        print(message)


def help():
    info("Help menu")
    info("-en     --enable-numbers        Enable number characters")
    info("-eu     --enable-upper          Enable uppercase characters")
    info("-es     --enable-symbols        Enables ASCII symbol characters")
    info("size    size=n                  Sets the size of the string to generate")
    info("lines   lines=n                 Sets the number of strings generated")


class ArgumentProcessor:
    """This rudimentary class is in charge of processing the command line
    arguments"""

    def __init__(self, tl: list):
        self.__list_tokens = tl

    def process(self):
        values = {}
        params = []
        for item in self.__list_tokens:
            if item.startswith("--"):
                params.append(item)
            elif item[0] == "-" and item[1] != "-":
                params.append(item)
            else:
                if "=" in item:
                    chunks = item.split("=")
                    values[chunks[0]] = chunks[1]
        return tuple(params), values


class Genpass:
    """This class is in charge of generating the text strings with random
    characters"""

    def __init__(self):
        # default types
        self.__types = {"lower": True, "upper": False,
                        "symbol": False, "number": False}
        self.__size = 10  # default size
        self.__ranges = {}  # default ranges

    def __regist_values(self, key, value):
        """Logs a range only once in memory to avoid wasting processor cycles
        unnecessarily"""
        self.__ranges[key] = value

    def __is_registered(self, key) -> bool:
        """Check if a range is registered"""
        return key in self.__ranges

    def __generate_lower(self) -> str:
        """Returns a lowercase character"""
        if not self.__is_registered("lower"):
            self.__regist_values("lower", range(97, 123))
        return choice(self.__ranges["lower"])

    def __generate_upper(self) -> str:
        """Returns a uppercase character"""
        if not self.__is_registered("upper"):
            self.__regist_values("upper", range(65, 91))
        return choice(self.__ranges["upper"])

    def __generate_symbol(self) -> str:
        """Returns an ASCII symbol"""
        if not self.__is_registered("symbol"):
            self.__regist_values(
                "symbol", [range(32, 48), range(58, 65),
                           range(91, 97), range(123, 127)]
            )
        return choice(choice(self.__ranges["symbol"]))

    def __generate_number(self) -> str:
        """Returns a number"""
        if not self.__is_registered("number"):
            self.__regist_values("number", range(48, 58))
        return choice(self.__ranges["number"])

    def __get_secure_char(self) -> int:
        enabled = False
        type = ""
        while not enabled:
            keys = list(self.__types.keys())
            type = choice(keys)
            enabled = self.__types[type]
        if type == "upper":
            return self.__generate_upper()
        elif type == "lower":
            return self.__generate_lower()
        elif type == "symbol":
            return self.__generate_symbol()
        elif type == "number":
            return self.__generate_number()
        else:
            return 32

    def set_size(self, size: int):
        self.__size = size

    def enable(self, e_type: str):
        if e_type == "uppercase":
            self.__types["upper"] = True
        elif e_type == "symbols":
            self.__types["symbol"] = True
        elif e_type == "numbers":
            self.__types["number"] = True

    def execute(self) -> str:
        string = ""
        for _ in range(self.__size):
            string += chr(self.__get_secure_char())
        return string


def main(args: list):
    if len(args) > 0:
        if args[0] == "--help" or args[0] == "-h":
            help()
        else:
            params, values = ArgumentProcessor(args).process()
            if "size" in values:
                generator = Genpass()
                if "-es" in params or "--enable-symbols" in params:
                    generator.enable("symbols")
                if "-en" in params or "--enable-numbers" in params:
                    generator.enable("numbers")
                if "-eu" in params or "--enable-uppercase" in params:
                    generator.enable("uppercase")
                generator.set_size(int(values["size"]))
                lines = 1
                if "lines" in values:
                    lines = int(values["lines"])
                if lines > 1:
                    for _ in range(lines):
                        success(generator.execute())
                else:
                    success(generator.execute())
            else:
                error("Error: a valid size was not specified")
    else:
        error("Error: no arguments specified")


if __name__ == "__main__":
    args = sys.argv
    del args[0]
    if color_module:
        init()
    main(args)
