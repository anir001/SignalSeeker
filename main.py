import sys
import os
from seeker.engine import Engine
from util.img_procces import merge_and_save
from util.to_pdf import save_to_pdf
from termcolor import colored

import time

os.system('color')

VER = 'v1.0.1'

PDF_OUTPUT_DIR = 'pdf_output'
TMP_DIR = 'tmp'
HEADER = f"""
  #####                                    #####                                     
 #     # #  ####  #    #   ##   #         #     # ###### ###### #    # ###### ##### 
 #       # #    # ##   #  #  #  #         #       #      #      #   #  #      #    # 
  #####  # #      # #  # #    # #          #####  #####  #####  ####   #####  #    # 
       # # #  ### #  # # ###### #               # #      #      #  #   #      ##### 
 #     # # #    # #   ## #    # #         #     # #      #      #   #  #      #   # 
  #####  #  ####  #    # #    # ######     #####  ###### ###### #    # ###### #    # {VER}                                                                             
"""


def main():
    if not os.path.exists(PDF_OUTPUT_DIR):
        os.makedirs(PDF_OUTPUT_DIR)

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    print(colored(HEADER, 'cyan'))

    if len(sys.argv) <= 1:
        print("python main.py file to_find start_page stop_page")
        print("""
    file        Specifies the file to search
    to_find     Specifies the signal list file to search for
    start_page  The beginning of the search
    stop_page   End of search
        """)
        sys.exit(0)
    else:
        PATH_PDF = sys.argv[1]

        PATH_TO_FIND = sys.argv[2]

        START_PAGE = int(sys.argv[3]) - 1  # strony zaczynaja sie od 0!
        STOP_PAGE = int(sys.argv[4])  # ostatnia strona

        engine = Engine()

        print('Searching...')
        signals = engine.run(PATH_PDF, PATH_TO_FIND, START_PAGE, STOP_PAGE)

        """
        Zapis obrazów na dysku
        """
        footer = f"Generated using SignalSeeker {VER} from a file {PATH_PDF}\nSignalSeeker is licensed under the GNU " \
                 f"GENERAL PUBLIC LICENSE v3.0 "
        merge_and_save([x.get_screen() for x in signals], footer)
        """
        Generacja PDF
        """
        print("PDF creating")
        save_to_pdf(PATH_PDF)
        """
        Validate
        """
        duplicates, missing = engine.validate()
        if duplicates:
            print(colored("Found duplicate signals:", 'yellow'))
            for d in duplicates:
                print(colored(f'# {d}', 'yellow'))
        if missing:
            print(colored("Signals not found:", 'red'))
            for m in missing:
                print(colored(f'# {m}', 'red'))

        """
        Finish
        """
        print(colored("Finish OK", 'green'))


def measure_time(func):
    """
    Funkcja mierząca czas wykonania funkcji.

    Parametry:
    - func: funkcja do zmierzenia czasu
    Zwraca:
    - Czas wykonania funkcji w sekundach
    """
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time

if __name__ == '__main__':
    steps = 1
    elapsed_time = 0
    for _ in range(steps):
        elapsed_time += measure_time(main)

    print(f"sredni czas wykonania: {elapsed_time / steps} sekundy")