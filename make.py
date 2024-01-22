import sys
import os
import subprocess as sp


EXECUTABLE = "genpass.py"
PATH = os.path.join(os.getcwd())
VENV = "/bin/activate"


def activate():
    sp.call(["source", f"{PATH}/{VENV}"])
    # os.system(f"source {PATH}/{VENV}")


def clean():
    sp.call(["rm", "-r", "build"])
    sp.call(["rm", "-r", "dist"])
    sp.call(["rm", "-r", "__pycache__"])
    sp.call(["rm", "genpass.spec"])


def compile():
    sp.call(["pyinstaller", "-F", "-noconsole", EXECUTABLE])


def main(args: list):
    if len(args) > 0:
        if args[0] == "compile":
            compile()
        elif args[0] == "activate":
            activate()
        elif args[0] == "clean":
            clean()
        else:
            print("Task not found :(")
    else:
        print("Error:")


if __name__ == '__main__':
    args = sys.argv
    del args[0]
    main(args)

