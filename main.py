import time
import tkinter as tk
from typing import Tuple
from PIL import ImageGrab, ImageOps
from PIL.Image import Image
from utils.clipboard import WindowsClipBoard, ClipBoardInterface
from utils.input.mouse import WindowsMouse, MouseInterface
import pytesseract
import platform


class Frame(tk.Tk):
    def __init__(self, clip: ClipBoardInterface.ClipBoardInterface, _mouse: MouseInterface.MouseInterface):
        super().__init__()
        self.withdraw()
        self.clipboard = clip
        self.mouse = _mouse

    @staticmethod
    def grab_image(first_click: Tuple[int, int], last_click: Tuple[int, int]) -> Image:
        box = [0, 0, 0, 0]
        if first_click[0] < last_click[0]:
            box[0] = first_click[0]
            box[2] = last_click[0]
        else:
            box[2] = first_click[0]
            box[0] = last_click[0]

        if first_click[1] < last_click[1]:
            box[1] = first_click[1]
            box[3] = last_click[1]
        else:
            box[3] = first_click[1]
            box[1] = last_click[1]

        im = ImageGrab.grab(bbox=box)
        return im

    @staticmethod
    def image_to_string(image: Image) -> str:
        im1 = ImageOps.grayscale(image)
        content = pytesseract.image_to_string(im1, lang="eng")
        return content

    def box_animation(self):
        started = False
        win_pos_x, win_pos_y = (0, 0)
        grab_screen = tk.Toplevel(self)
        grab_screen.overrideredirect(True)
        grab_screen.wm_attributes("-alpha", 0.6)
        grab_screen.geometry("50x50")
        first_click_pos = (0, 0)
        last_click_pos = (0, 0)
        while True:
            mouse_x, mouse_y = self.mouse.position()
            if self.mouse.is_left_pressed():
                if not started:
                    first_click_pos = mouse_x, mouse_y
                started = True
                win_pos_dif = (abs(mouse_x - win_pos_x), abs(mouse_y - win_pos_y))
                win_size = f"{win_pos_dif[0]}x{win_pos_dif[1]}"
                grab_screen.geometry(win_size)

                if mouse_y > win_pos_y:
                    if mouse_x > win_pos_x:
                        pass
                    else:
                        win_icon_position = f"+{mouse_x}+{first_click_pos[1]}"
                        grab_screen.geometry(win_icon_position)
                else:
                    if mouse_x > win_pos_x:
                        win_icon_position = f"+{first_click_pos[0]}+{mouse_y}"
                        grab_screen.geometry(win_icon_position)
                    else:
                        win_icon_position = f"+{mouse_x}+{mouse_y}"
                        grab_screen.geometry(win_icon_position)
                grab_screen.update_idletasks()
                grab_screen.update()

            else:
                if started:
                    last_click_pos = mouse_x, mouse_y
                    self.capture_animation(grab_screen)
                    grab_screen.destroy()
                    self.destroy()
                    return first_click_pos, last_click_pos
                win_icon_position = f"+{mouse_x}+{mouse_y}"
                grab_screen.geometry(win_icon_position)
                win_pos_x, win_pos_y = mouse_x, mouse_y
                grab_screen.update()

    @staticmethod
    def capture_animation(widget):
        time.sleep(0.5)
        widget.withdraw()
        time.sleep(0.1)
        widget.deiconify()
        time.sleep(0.2)

    def capture(self):
        box = self.box_animation()
        image = self.grab_image(*box)
        content = self.image_to_string(image)
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

    frame = Frame(clipboard, mouse)
    frame.capture()
    frame.mainloop()
