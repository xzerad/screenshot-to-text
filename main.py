import tkinter as tk
from utils.clipboard import WindowsClipBoard, ClipBoardInterface
from utils.input.mouse import WindowsMouse, MouseInterface
from utils.animation import WidgetAnimation
from utils.image import operations
import platform


class Box(tk.Tk):
    def __init__(self):
        super(Box, self).__init__()
        self.withdraw()

    def animation(self):
        grab_screen = tk.Toplevel(self)
        grab_screen.bind("<Escape>", lambda e: grab_screen.destroy())
        box = WidgetAnimation.WidgetAnimation.box_animation(grab_screen, WindowsMouse.WindowsMouse())
        grab_screen.destroy()
        self.destroy()
        return box


class ScreenshotToText:
    def __init__(self, clip: ClipBoardInterface.ClipBoardInterface, _mouse: MouseInterface.MouseInterface):
        super().__init__()
        self.clipboard = clip
        self.mouse = _mouse

    def capture(self):
        box = Box()
        box_pos = box.animation()
        box.mainloop()
        image = operations.grab_image(*box_pos)
        content = operations.image_to_string(operations.image_filter(image))
        self.clipboard.set_content(content)


if __name__ == '__main__':
    clipboard = None
    mouse = None
    if platform.system() == "Windows":
        clipboard = WindowsClipBoard.WindowsClipBoard()
        mouse = WindowsMouse.WindowsMouse()
    #  todo add linux and macos support
    else:
        raise OSError("Unsupported OS")

    stt = ScreenshotToText(clipboard, mouse)
    stt.capture()
