import time
import tkinter as tk
import pyautogui
import win32api
from PIL import ImageGrab, ImageOps
import win32clipboard
import win32con
import pytesseract


class Frame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.first_click_pos = 0, 0
        self.last_click_pos = 0, 0

    def grab_image(self):
        box = [0, 0, 0, 0]
        if self.first_click_pos[0] < self.last_click_pos[0]:
            box[0] = self.first_click_pos[0]
            box[2] = self.last_click_pos[0]
        else:
            box[2] = self.first_click_pos[0]
            box[0] = self.last_click_pos[0]

        if self.first_click_pos[1] < self.last_click_pos[1]:
            box[1] = self.first_click_pos[1]
            box[3] = self.last_click_pos[1]
        else:
            box[3] = self.first_click_pos[1]
            box[1] = self.last_click_pos[1]

        im = ImageGrab.grab(bbox=box)
        im1 = ImageOps.grayscale(im)
        string = pytesseract.image_to_string(im1, lang="eng")

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
        win32clipboard.CloseClipboard()

    def grab(self):
        pressed = False
        started = False
        win_pos = (0, 0)
        grab_screen = tk.Toplevel(self)
        grab_screen.overrideredirect(True)
        grab_screen.wm_attributes("-alpha", 0.6)
        grab_screen.geometry("50x50")
        click_state = win32api.GetKeyState(0x01)

        while True:
            current_click_state = win32api.GetKeyState(0x01)
            mouse_position = pyautogui.position()
            mouse_x, mouse_y = mouse_position.x, mouse_position.y
            if click_state != current_click_state:
                click_state = current_click_state
                if current_click_state < 0:
                    pressed = True
                else:
                    pressed = False
            if pressed:
                if not started:
                    self.first_click_pos = mouse_x, mouse_y
                started = True
                win_pos_dif = (abs(mouse_x - win_pos[0]), abs(mouse_y - win_pos[1]))
                win_size = f"{win_pos_dif[0]}x{win_pos_dif[1]}"
                grab_screen.geometry(win_size)

                if mouse_y > win_pos[1]:
                    if mouse_x > win_pos[0]:
                        pass
                    else:
                        win_icon_position = f"+{mouse_x}+{self.first_click_pos[1]}"
                        grab_screen.geometry(win_icon_position)
                else:
                    if mouse_x > win_pos[0]:
                        win_icon_position = f"+{self.first_click_pos[0]}+{mouse_y}"
                        grab_screen.geometry(win_icon_position)
                    else:
                        win_icon_position = f"+{mouse_x}+{mouse_y}"
                        grab_screen.geometry(win_icon_position)
                grab_screen.update_idletasks()
                grab_screen.update()

            else:
                if started:
                    self.last_click_pos = mouse_x, mouse_y
                    self.animation(grab_screen)
                    grab_screen.destroy()
                    self.grab_image()
                    self.destroy()
                    return
                win_icon_position = f"+{mouse_x}+{mouse_y}"
                grab_screen.geometry(win_icon_position)
                win_pos = mouse_x, mouse_y
                grab_screen.update()

    @staticmethod
    def animation(widget):
        time.sleep(0.5)
        widget.withdraw()
        time.sleep(0.1)
        widget.deiconify()
        time.sleep(0.2)


frame = Frame()
frame.grab()
frame.mainloop()
