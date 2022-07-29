"""
Represents a founded Signal
"""
import fitz
from PIL import Image


class Signal(object):
    """
    :param signature name of signal
    :param clip: Rect
    """
    def __init__(self, signature, clip, page):
        self.signature = signature
        self.clip = clip
        self.page = page

    def get_screen(self):
        """
        Wycięciecie pixmapy do utworzenia obrazka

        """
        mat = fitz.Matrix(2, 2)
        pix = self.page.get_pixmap(matrix=mat, clip=self.clip)

        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    def get_signature(self):
        return self.signature

    def get_clip(self):
        return self.clip
