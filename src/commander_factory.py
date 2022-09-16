import platform
import subprocess
from abc import ABCMeta, abstractmethod
from pathlib import Path


class CommanderFactory(metaclass=ABCMeta):
    @staticmethod
    def get_os_specific_commander():
        match platform.system():
            case 'Windows':
                return WinNTCommander()

            case 'Darwin' | 'Linux':
                return UnixCommander()

            case _:
                raise SystemError("Unsupported OS")

    def _run(self, args) -> None:
        subprocess.run(args, shell=True)

    @abstractmethod
    def get_next_key_press(self) -> str:
        pass

    @abstractmethod
    def clear_screen(self) -> None:
        pass

    @abstractmethod
    def list_directory(self, dir_path) -> None:
        pass

    @abstractmethod
    def copy_file(self, file_path: Path, destination: Path) -> None:
        pass

    @abstractmethod
    def move_file(self, file_path: Path, destination: Path) -> None:
        pass

    @abstractmethod
    def delete_file(self, file_path: Path) -> None:
        pass


class WinNTCommander(CommanderFactory):
    def get_next_key_press(self) -> str:
        from msvcrt import getch

        return getch().decode()

    def clear_screen(self) -> None:
        self._run(['cls'])

    def list_directory(self, dir_path) -> None:
        self._run(['ls', '-la', dir_path])

    def copy_file(self, file_path: Path, destination: Path) -> None:
        self._run(['copy', file_path.resolve(), destination.resolve()])

    def move_file(self, file_path: Path, destination: Path) -> None:
        self._run(['move', file_path.resolve(), destination.resolve()])

    def delete_file(self, file_path: Path) -> None:
        self._run(['del', file_path.resolve()])


class UnixCommander(CommanderFactory):
    def get_next_key_press(self) -> str:
        import termios
        import tty
        from sys import stdin

        file_descriptor = stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)
        tty.setraw(stdin.fileno())

        read_char = stdin.read(1)

        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)

        return read_char

    def clear_screen(self) -> None:
        self._run(['clear'])

    def list_directory(self, dir_path) -> None:
        self._run([f'ls "{dir_path.as_posix()}" -la'])

    def copy_file(self, file_path: Path, destination: Path) -> None:
        self._run([f'cp -u "{file_path.resolve()}" "{destination.resolve()}"'])

    def move_file(self, file_path: Path, destination: Path) -> None:
        self._run([f'mv "{file_path.resolve()}" "{destination.resolve()}"'])

    def delete_file(self, file_path: Path) -> None:
        self._run([f'rm "{file_path.resolve()}"'])
