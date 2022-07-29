import os
import fitz
from datetime import date
from natsort import natsorted
from tqdm import tqdm


def save_to_pdf(name: str):
    """
    Generacja Pdfa z obrazow
    :param name:
    :return:
    """

    doc = fitz.open()  # PDF with the pictures
    img_dir = "./tmp"  # where the pics are
    img_list = os.listdir(img_dir)  # list of them
    img_list = natsorted(img_list)

    for i, f in tqdm(enumerate(img_list)):
        img = fitz.open(os.path.join(img_dir, f))  # open pic as document
        rect = img[0].rect  # pic dimension
        pdf_bytes = img.convert_to_pdf()  # make a PDF stream
        img.close()  # no longer needed
        imgPDF = fitz.open("pdf", pdf_bytes)  # open stream as PDF
        page = doc.new_page(width=rect.width,  # new page with ...
                            height=rect.height)  # pic dimension
        page.show_pdf_page(rect, imgPDF, 0)  # image fills the page

    doc.save("./pdf_output/{}_{}.pdf".format(name, date.today()))

    """
    clean tmp
    """
    for file in img_list:
        os.remove(os.path.join(img_dir, file))
