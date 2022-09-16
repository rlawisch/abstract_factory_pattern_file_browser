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
    def clear_screen(self) -> None:
        pass

    def list_directory(self, dir_path) -> None:
        self._run(['ls', '-l', dir_path])

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
    def clear_screen(self) -> None:
        self._run(['cls'])

    def copy_file(self, file_path: Path, destination: Path) -> None:
        self._run(['copy', file_path.resolve(), destination.resolve()])

    def move_file(self, file_path: Path, destination: Path) -> None:
        self._run(['move', file_path.resolve(), destination.resolve()])

    def delete_file(self, file_path: Path) -> None:
        self._run(['del', file_path.resolve()])


class UnixCommander(CommanderFactory):
    def clear_screen(self) -> None:
        self._run(['clear'])

    def copy_file(self, file_path: Path, destination: Path) -> None:
        self._run(['cp'. file_path.resolve(), destination.resolve()])

    def move_file(self, file_path: Path, destination: Path) -> None:
        self._run(['mv', file_path.resolve(), destination.resolve()])

    def delete_file(self, file_path: Path) -> None:
        self._run(['rm', file_path.resolve()])
