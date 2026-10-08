import os
import argparse


class Node:
    def __init__(self, file_type, data=""):
        self.file_type = file_type
        self.data = data


def execute_command(command_line):
    command_line = command_line.replace("$HOME", os.getcwd())
    command_line = os.path.expandvars(command_line)

    args = command_line.split()

    if not args:
        return True

    command = args[0]
    arguments = args[1:]

    if command == "exit":
        if arguments:
            print("Ошибка: exit не принимает аргументы")
            return True
        print("Выход из VFS...")
        return False

    elif command == "echo":
        print(arguments[0])

    elif command == "ls":
        if arguments:
            print("Ошибка: ls не принимает аргументы")
        else:
            print("ls")

    elif command == "cd":
        if len(arguments) == 0:
            print("Ошибка: cd требует один аргумент")
        elif len(arguments) > 1:
            print("Ошибка: cd требует ровно один аргумент")
        else:
            print("cd", arguments[0])

    else:
        print(f"Ошибка: неизвестная команда {command}")

    return True


def execute_script(script_path):
    try:
        with open(script_path, "r", encoding="utf-8") as script:
            for line_number, line in enumerate(script, start=1):
                command_line = line.strip()

                if not command_line:
                    continue
                print(f"> {command_line}")
                should_continue = execute_command(command_line)
                if not should_continue:
                    break

    except FileNotFoundError:
        print(f"Ошибка: стартовый скрипт не найден: {script_path}")


def repl(vfs_path, vfs_name="VFS"):
    while True:
        command_line = input(f"{vfs_name}:/> ")

        if not command_line.strip():
            continue

        should_continue = execute_command(command_line)

        if not should_continue:
            return


def parse_arguments():
    parser = argparse.ArgumentParser(
    )

    parser.add_argument(
        "--vfs-path",
        default="./vfs",
        help="Путь к физическому расположению VFS"
    )

    parser.add_argument(
        "--script",
        default="./startup.txt",
        help="Путь к стартовому скрипту"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    vfs_path = os.path.expandvars(args.vfs_path)
    script_path = os.path.expandvars(args.script)

    vfs_path = os.path.abspath(vfs_path)
    script_path = os.path.abspath(script_path)

    vfs_name = os.path.basename(os.path.normpath(vfs_path))

    if not os.path.exists(vfs_path):
        print(f"Предупреждение: VFS не существует: {vfs_path}")
        print("Будет создан VFS.")

        os.makedirs(vfs_path)

    if not os.path.isdir(vfs_path):
        print(f"Ошибка: путь VFS не является каталогом: {vfs_path}")
        return


    print("--- Параметры запуска эмулятора ---")
    print(f"Физический путь VFS: {vfs_path}")
    print(f"Стартовый скрипт:     {script_path}")
    print(f"Имя VFS:              {vfs_name}")
    print("-----------------------------------")

    root = Node("dir", {})

    print()
    print("--- Выполнение стартового скрипта ---")

    execute_script(script_path)

    print("--- Стартовый скрипт завершён ---")
    print()
    repl(vfs_path, vfs_name)


if __name__ == "__main__":
    main()