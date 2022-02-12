from typing import Union


class ClipBoardInterface:
    def get_content(self) -> Union[str, bytes]:
        raise NotImplementedError

    def set_content(self, content: Union[str, bytes]) -> None:
        raise NotImplementedError
