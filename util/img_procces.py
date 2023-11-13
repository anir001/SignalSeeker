from PIL import Image, ImageDraw, ImageEnhance, ImageFont

WIDTH = 2800
HEIGHT = int(WIDTH * 0.7)


def total_width(arr):
    """
    Oblicza szerokosc przyszłego obrazu
    :param arr:
    :return:
    """
    # total = []
    # for w in arr:
    #     if w is not None:
    #         total.append(w.width)
    # return sum(total)
    total = sum([w.width for w in arr if w is not None])
    return total


def save_img(img, page):
    """
    Zapisuje pojedynczy obraz na dysku
    :param page:
    :param img:
    :return:
    """
    img.save('./tmp/{:d}_img.png'.format(page))


def draw_frame(img):
    """
    Rysowanie czerwonej ramki
    :param img:
    :return:
    """
    draw = ImageDraw.Draw(img)
    draw.line(((img.width, 0), (img.width, img.height)),
              fill=(255, 0, 0), width=5)
    return img


def merge_and_save(images, footer):
    """
    Laczenie pojedynczych obrazów w jeden.
    """
    images = list(list_split(images, 8))
    page_max = len(images)

    for page, arr in enumerate(images):

        width = total_width(arr)
        if width < WIDTH:
            width = WIDTH
        height = arr[0].height
        if height < HEIGHT:
            height = HEIGHT
        dst = Image.new('RGBA', (width, height), color=(255, 255, 255))

        paste_pos_x = 0
        paste_pos_y = 65
        for count, img in enumerate(arr):
            if img is not None:
                img = draw_frame(img)
                dst.paste(img, (paste_pos_x, paste_pos_y))
                paste_pos_x += img.width
        dst = contrast(dst)
        dst = add_footer(dst, page, page_max, footer)
        save_img(dst, page)


def list_split(list_a, n):
    for x in range(0, len(list_a), n):
        every_chunk = list_a[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk


def contrast(im):
    enhancer = ImageEnhance.Contrast(im)

    factor = 5  # increase contrast
    return enhancer.enhance(factor)


def add_footer(im, page, max_page, footer):
    I1 = ImageDraw.Draw(im)
    myFont = ImageFont.truetype('./font/FreeMono.ttf', 30)
    # Add Text to an image
    I1.text(
        (30, HEIGHT - 65),
        footer,
        font=myFont,
        fill=(0, 0, 0),
    )
    I1.text(
        (WIDTH - 100, HEIGHT - 52),
        f"{page + 1}/{max_page}",
        font=myFont,
        fill=(0, 0, 0),
    )
    return im
