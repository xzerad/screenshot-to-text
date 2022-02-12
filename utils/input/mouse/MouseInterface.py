from typing import Tuple


class MouseInterface:

    def is_left_pressed(self) -> bool:
        raise NotImplementedError

    def is_left_released(self) -> bool:
        raise NotImplementedError

    def position(self) -> Tuple[int, int]:
        raise NotImplementedError
