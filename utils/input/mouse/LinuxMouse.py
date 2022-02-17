from typing import Tuple
from utils.input.mouse.MouseInterface import MouseInterface


class LinuxMouse(MouseInterface):
    def is_left_pressed(self) -> bool:
        pass

    def is_left_released(self) -> bool:
        pass

    def position(self) -> Tuple[int, int]:
        pass


if __name__ == '__main__':
    pass
