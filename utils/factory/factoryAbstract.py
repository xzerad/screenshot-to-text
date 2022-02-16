import platform
from typing import Optional
from utils.input.mouse.MouseInterface import MouseInterface
from utils.input.mouse.WindowsMouse import WindowsMouse
from utils.clipboard.WindowsClipBoard import WindowsClipBoard
from utils.clipboard.ClipBoardInterface import ClipBoardInterface


class MouseFactory:
    @staticmethod
    def create_mouse() -> Optional[MouseInterface]:
        if platform.system() == "Windows":
            return WindowsMouse()
        else:
            return None


class ClipBoardFactory:
    @staticmethod
    def create_clipboard() -> Optional[ClipBoardInterface]:
        if platform.system() == "Windows":
            return WindowsClipBoard()
        else:
            return None
