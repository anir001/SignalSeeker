import fitz
from .seeker import Seeker
from tqdm import tqdm


class Engine:
    def __init__(self):
        self.document = None
        self.to_find = {}
        self.seeker = Seeker()
        self.signals = []

    def run(self, path_pdf, path_signal, start_page, stop_page):
        self._open_pdf(path_pdf)
        self._open_signal_list(path_signal)

        if len(self.to_find) != 0 and self.document is not None:
            for sig in tqdm(self.to_find):
                if len(sig):
                    for page in range(start_page, stop_page):
                        signal = self.seeker.search(sig, self.document[page])

                        if signal is not None:
                            self.to_find[signal.get_signature()] += 1   # dla sprawdzenia ile razy sygnał został wyszukany
                            self.signals.append(signal)
        return self.signals

    def validate(self):
        duplicates = []
        missing = []

        for s in self.to_find:
            if self.to_find[s] > 1:
                duplicates.append(s)

        for s in self.to_find:
            if self.to_find[s] == 0:
                missing.append(s)

        return duplicates, missing

    def _open_pdf(self, path_pdf):
        try:
            self.document = fitz.open(path_pdf)
        except:
            print("Błąd podczas otwierania pliku PDF")

    def _open_signal_list(self, path_signal):
        try:
            with open(path_signal) as f:
                for line in f:
                    self.to_find[line.replace('\n', '')] = 0
            # print(self.to_find)
        except:
            print("Błąd podczas otwierania pliku TXT.")
