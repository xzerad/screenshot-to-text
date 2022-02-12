from typing import Tuple
from utils.input.mouse.MouseInterface import MouseInterface
import win32api


class WindowsMouse(MouseInterface):

    def position(self) -> Tuple[int, int]:
        return win32api.GetCursorPos()

    def is_left_pressed(self) -> bool:
        click_state = win32api.GetKeyState(0x01)
        return click_state < 0

    def is_left_released(self) -> bool:
        click_state = win32api.GetKeyState(0x01)
        return click_state > 0

