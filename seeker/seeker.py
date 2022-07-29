import fitz
from .signal import Signal


class Seeker(object):
    def __init__(self):
        self.rect = None

        self.shift_x_right = 35
        self.shift_x_left = 70
        self.shift_y_up = 110
        self.shift_y_down = 520

    def search(self, signal, page: fitz.Page):
        rects = page.search_for(signal)
        if len(rects) != 0:  # jeżeli brak wyników return None
            for rect in rects:
                if rect[1] < 200:  # szukamy wyniku który jest na górze strony
                    self.rect = rect
                    self._shift_coord()

                    return Signal(signal, self.rect, page)
        else:
            return None

    def _shift_coord(self):
        """
        Ustawienie prostokąta zawierającego sygnał i listwe.
        :return:
        """
        self.rect.x0 -= self.shift_x_left
        self.rect.x1 += self.shift_x_right
        self.rect.y0 -= self.shift_y_up
        self.rect.y1 += self.shift_y_down

    def _search_terminal_name(self, page):
        """
        TO DO
        """
        pass
