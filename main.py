import os
import sys
import time
from termcolor import colored
from seeker.engine import Engine
from util.img_procces import merge_and_save
from util.to_pdf import save_to_pdf

os.system('color')

VER = 'v1.0.2'

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


def create_directory_if_not_exists(directory):
    """Tworzy katalog, jeśli nie istnieje."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def print_header():
    """Drukuje nagłówek aplikacji."""
    print(colored(HEADER, 'cyan'))


def print_usage():
    """Drukuje informacje dotyczące poprawnej składni."""
    print("Usage: ")
    print("python main.py file to_find start_page stop_page")
    print("""        
          file        Specifies the file to search
          to_find     Specifies the signal list file to search for
          start_page  The beginning of the search
          stop_page   End of search     
    """)


def process_arguments():
    """Przetwarza argumenty wiersza poleceń."""
    if len(sys.argv) <= 1:
        print_usage()
        sys.exit(0)
    else:
        return sys.argv[1], sys.argv[2], int(sys.argv[3]) - 1, int(sys.argv[4])


def print_search_parameters(pdf_path, signal_list_path, start_page, stop_page):
    """Drukuje informacje o parametrach wyszukiwania."""
    print(f"""
     __________________________________________________________
       [+] path to pdf file          | {pdf_path}             
       [+] path to signal list file  | {signal_list_path}
       [+] start page                | {start_page}
       [+] stop page                 | {stop_page}
     __________________________________________________________
    """)


def print_searching_message():
    """Drukuje komunikat o rozpoczęciu wyszukiwania."""
    print('[!]  Searching...')


def print_pdf_creation_message():
    """Drukuje komunikat o tworzeniu pliku PDF."""
    print("[!]  PDF creating...")


def print_duplicate_signals(duplicates):
    """Drukuje komunikat o zduplikowanych sygnałach, jeśli istnieją."""
    if duplicates:
        print(colored("[!]  Found duplicate signals:", 'yellow'))
        for d in duplicates:
            print(colored(f'# {d}', 'yellow'))


def print_missing_signals(missing):
    """Drukuje komunikat o brakujących sygnałach, jeśli istnieją."""
    if missing:
        print(colored("[!]  Signals not found:", 'red'))
        for m in missing:
            print(colored(f'# {m}', 'red'))


def print_finish_message():
    """Drukuje komunikat o zakończeniu programu."""
    print(colored("[!]  Finish OK", 'green'))


def main():
    create_directory_if_not_exists(PDF_OUTPUT_DIR)
    create_directory_if_not_exists(TMP_DIR)

    print_header()

    pdf_path, signal_list_path, start_page, stop_page = process_arguments()

    engine = Engine()

    print_search_parameters(pdf_path, signal_list_path, start_page, stop_page)

    print_searching_message()
    signals = engine.run(pdf_path, signal_list_path, start_page, stop_page)

    engine.close_document()

    footer = f"Generated using SignalSeeker {VER} from a file {pdf_path}\nSignalSeeker is licensed under the GNU " \
             f"GENERAL PUBLIC LICENSE v3.0 "
    merge_and_save([x.get_screen() for x in signals], footer)

    print_pdf_creation_message()
    save_to_pdf(pdf_path)

    duplicates, missing = engine.validate()
    print_duplicate_signals(duplicates)
    print_missing_signals(missing)

    print_finish_message()


def measure_time(func):
    """Mierzy czas wykonania funkcji."""
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


if __name__ == '__main__':
    main()
