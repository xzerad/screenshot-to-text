from typing import Union
import win32clipboard
import win32con
from utils.clipboard.ClipBoardInterface import ClipBoardInterface


class WindowsClipBoard(ClipBoardInterface):
    def get_content(self) -> Union[str, bytes]:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data

    def set_content(self, content: Union[str, bytes]) -> None:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, content)
        win32clipboard.CloseClipboard()
