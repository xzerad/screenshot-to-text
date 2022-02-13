import time


class WidgetAnimation:
    @staticmethod
    def capture_animation(widget):
        time.sleep(0.5)
        widget.withdraw()
        time.sleep(0.1)
        widget.deiconify()
        time.sleep(0.2)

    @staticmethod
    def box_animation(widget, mouse):
        started = False
        win_pos_x, win_pos_y = (0, 0)
        widget.overrideredirect(True)
        widget.wm_attributes("-alpha", 0.6)
        widget.geometry("50x50")
        first_click_pos = (0, 0)
        last_click_pos = (0, 0)
        while True:
            mouse_x, mouse_y = mouse.position()
            if mouse.is_left_pressed():
                if not started:
                    first_click_pos = mouse_x, mouse_y
                started = True
                win_pos_dif = (abs(mouse_x - win_pos_x), abs(mouse_y - win_pos_y))
                win_size = f"{win_pos_dif[0]}x{win_pos_dif[1]}"
                widget.geometry(win_size)

                if mouse_y > win_pos_y:
                    if mouse_x > win_pos_x:
                        pass
                    else:
                        win_icon_position = f"+{mouse_x}+{first_click_pos[1]}"
                        widget.geometry(win_icon_position)
                else:
                    if mouse_x > win_pos_x:
                        win_icon_position = f"+{first_click_pos[0]}+{mouse_y}"
                        widget.geometry(win_icon_position)
                    else:
                        win_icon_position = f"+{mouse_x}+{mouse_y}"
                        widget.geometry(win_icon_position)
                widget.update_idletasks()
                widget.update()

            else:
                if started:
                    last_click_pos = mouse_x, mouse_y
                    WidgetAnimation.capture_animation(widget)
                    return first_click_pos, last_click_pos
                win_icon_position = f"+{mouse_x}+{mouse_y}"
                widget.geometry(win_icon_position)
                win_pos_x, win_pos_y = mouse_x, mouse_y
                widget.update()
