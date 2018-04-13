from enum import Enum


class ButtonTypes(Enum):

    WHITE_LEFT = ((0, 100), (0, 0), (20, 0), (20, 60), (30, 60), (30, 100))
    WHITE_CENTER = ((0, 100), (0, 60), (10, 60), (10, 0), (20, 0), (20, 60), (30, 60), (30, 100))
    WHITE_RIGHT = ((0, 100), (0, 60), (10, 60), (10, 0), (30, 0), (30, 100))
    BLACK = ((0, 60), (0, 0), (30, 0), (30, 60))

    @staticmethod
    def get_offset(type_):
        if type_ == ButtonTypes.WHITE_RIGHT:
            return 40
        return 20


class Button:

    COLOR_WHITE_RELEASED = (255, 255, 255)
    COLOR_BLACK_RELEASED = (0, 0, 0)
    COLOR_WHITE_PRESSED = (150, 150, 100)
    COLOR_BLACK_PRESSED = (50, 40, 30)

    def __init__(self, type_, offset, scale=1):
        self._type = type_
        self._width = max([x for x, _ in type_.value]) * scale
        self._height = max([y for _, y in type_.value]) * scale
        self._polygon = [((x + offset) * scale, y * scale) for x, y in type_.value]
        self._x, self._y = 0, 0
        self.pressed = False

    def is_black(self):
        return self._type == ButtonTypes.BLACK

    def get_polygon(self):
        return self._polygon

    def get_size(self):
        return self._width, self._height

    def get_position(self):
        return self._x, self._y

    def get_color(self):
        if self._type == ButtonTypes.BLACK:
            return Button.COLOR_BLACK_PRESSED if self.pressed else Button.COLOR_BLACK_RELEASED
        return Button.COLOR_WHITE_PRESSED if self.pressed else Button.COLOR_WHITE_RELEASED

    def set_position(self, position):
        dx, dy = position
        self._polygon = [(x + dx, y + dy) for x, y in self._polygon]
        self._x = min([x for x, _ in self._polygon])
        self._y = min([y for _, y in self._polygon])
