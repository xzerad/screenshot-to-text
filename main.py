import tkinter as tk
from utils.clipboard import WindowsClipBoard, ClipBoardInterface
from utils.input.mouse import WindowsMouse, MouseInterface
from utils.animation import WidgetAnimation
from utils.image import operations
import platform


class ScreenshotToText(tk.Tk):
    def __init__(self, clip: ClipBoardInterface.ClipBoardInterface, _mouse: MouseInterface.MouseInterface):
        super().__init__()
        self.withdraw()
        self.clipboard = clip
        self.mouse = _mouse

    def capture(self):
        grab_screen = tk.Toplevel(self)
        grab_screen.bind("<Escape>", lambda e: grab_screen.destroy())
        box = WidgetAnimation.WidgetAnimation.box_animation(grab_screen, WindowsMouse.WindowsMouse())
        grab_screen.destroy()
        image = operations.grab_image(*box)
        content = operations.image_to_string(operations.image_filter(image))
        self.clipboard.set_content(content)
        self.destroy()


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
    stt.mainloop()
