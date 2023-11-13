"""
Represents a founded Signal
"""
import fitz
from PIL import Image, ImageFont, ImageDraw


class Signal(object):
    """
    :param signature name of signal
    :param clip: Rect
    """

    def __init__(self, signature, clip, page, no_page):
        self.signature = signature
        self.clip = clip
        self.page = page
        self.no_page = no_page

    def get_screen(self):
        """
        Wycięciecie pixmapy do utworzenia obrazka

        """
        mat = fitz.Matrix(2, 2)
        pix = self.page.get_pixmap(matrix=mat, clip=self.clip)
        im = Image.frombytes(
            "RGB", [pix.width, pix.height], pix.samples)

        I1 = ImageDraw.Draw(im)

        myFont = ImageFont.truetype('./font/FreeMono.ttf', 30)
        # Add Text to an image
        I1.text(
            (30, 0),
            f"on page: {self.no_page + 1}",
            font=myFont,
            fill=(0, 0, 0),
        )

        return im

    def get_signature(self):
        return self.signature

    def get_clip(self):
        return self.clip
