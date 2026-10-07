import os


class Node:
    def __init__(self, file_type, data=''):
        self.file_type = file_type
        self.data = data


def repl(node, vfs_name='VFS'):
    while True:
        command_line = input(f'{vfs_name}:/> ')
        if not command_line.strip():
            continue
        command_line = os.path.expandvars(command_line)
        args = command_line.split()
        if not args:
            continue
        command = args[0]
        arguments = args[1:]

        if command == "exit":
            if arguments:
                print("Ошибка: exit не принимает аргументы")
            else:
                print("Выход из VFS...")
                return

        elif command == "echo":
            print(*arguments)
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


root = Node('dir', {})
repl(root, 'VFS')