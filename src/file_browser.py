from pathlib import Path

from commander_factory import CommanderFactory


class FileBrowser:
    __esc = chr(27)
    __options = ['1', '2', '3', '4', '5', __esc]

    def __init__(self) -> None:
        self.__commander = CommanderFactory.get_os_specific_commander()
        self.__curr_path = Path(__file__).parent.resolve()

    def __print_menu(self):
        self.__commander.list_directory(self.__curr_path)
        print("\n1 - Change directory")
        print("2 - Copy file")
        print("3 - Move/rename file")
        print("4 - Delete file")
        print("ESC - Quit")

    def __get_menu_option(self) -> str:
        while (not (option := self.__commander.get_next_key_press())
                in self.__options):
            pass

        return option

    def __execute_menu_option(self, option):
        match option:
            case '1':
                print("\n1 - Change directory")
                self.__change_directory()

            case '2':
                print("\n2 - Copy file")
                self.__copy_file()

            case '3':
                print("\n3 - Move/rename file")
                self.__move_rename_file()

            case '4':
                print("\n4 - Delete file")
                self.__delete_file()

    def __get_file_path(self, input_message) -> Path:
        file_name = input(f"{input_message}\n")

        if (relative := self.__curr_path / file_name).is_file():
            return relative
        elif (absolute := Path(file_name)).is_file():
            return absolute
        else:
            raise ValueError(f"Invalid file name: {file_name}")

    def __get_free_file_path(self, input_message) -> Path:
        file_name = input(f"{input_message}\n")

        if ((relative := self.__curr_path / file_name).is_file()
                or (absolute := Path(file_name)).is_file()):
            raise ValueError(f"Path {file_name} is taken")

        if '/' in file_name or '\\' in file_name:
            return absolute
        else:
            return relative

    def __change_directory(self) -> None:
        nav_path = input("Enter the path where to navigate:\n")

        match nav_path:
            case '.':
                pass

            case '..':
                parent = self.__curr_path.parent.resolve()
                self.__curr_path = parent
                print("\nNavigated to parent directory")

            case _:
                if (relative := self.__curr_path / nav_path).is_dir():
                    self.__curr_path = relative
                    print(f"\nNavigated to {self.__curr_path.as_posix()}")
                elif (absolute := Path(nav_path)).is_dir():
                    self.__curr_path = absolute
                    print(f"\nNavigated to {self.__curr_path.as_posix()}")
                else:
                    print(f"\nInvalid directory: {nav_path}")

    def __copy_file(self) -> None:
        try:
            file_path = self.__get_file_path("Enter the name of the file to copy:")
        except ValueError as err:
            print(err)
            return

        try:
            destination = self.__get_free_file_path("Enter the path to destination:")
        except ValueError as err:
            print(err)
            return

        self.__commander.copy_file(file_path, destination)

    def __move_rename_file(self) -> None:
        try:
            file_path = self.__get_file_path("Enter the name of the file to move/rename:")
        except ValueError as err:
            print(err)
            return

        try:
            destination = self.__get_free_file_path("Enter the path to destination:")
        except ValueError as err:
            print(err)
            return

        self.__commander.move_file(file_path, destination)

    def __delete_file(self) -> None:
        try:
            file_path = self.__get_file_path("Enter the name of the file to delete:")
        except ValueError as err:
            print(err)
            return

        self.__commander.delete_file(file_path)

    def run(self):
        while True:
            self.__print_menu()
            option = self.__get_menu_option()

            if option == self.__esc:
                break

            self.__execute_menu_option(option)
