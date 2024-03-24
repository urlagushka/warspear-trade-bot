import cv2
from os import listdir
from os.path import isfile, join
import pytesseract
import numpy as np


class Font:  # font numbers struct
    def __init__(self, path: str) -> None:
        self.numbers = load_font(path)

    def match_price(self, src: np.ndarray) -> int:  # analyze image and get price
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        numbers = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            numbers += [thresh[y:y + h, x:x + w]]

        result = ""
        for num in numbers:
            for i in "0123456789":
                if np.array_equal(num, self.numbers[i]):
                    result += i

        if result == "":
            return -1

        return int(result[::-1])


class Interface:  # game interface struct
    def __init__(self, path: str, ocr_path: str) -> None:
        self.patterns = load_masks(path + "/masks")
        self.font = Font(path + "/font")
        pytesseract.pytesseract.tesseract_cmd = ocr_path

    def match_mask(self, source: np.ndarray, mask_name: str) -> tuple:  # match mask on image
        result = cv2.matchTemplate(source, self.patterns[mask_name], cv2.TM_SQDIFF_NORMED)
        mn, _, loc, _ = cv2.minMaxLoc(result)
        x, y = loc
        w, h = self.patterns[mask_name].shape[:2]
        return x, y, h, w


def load_font(path: str) -> dict:  # load font masks from path
    files = [f for f in listdir(path) if isfile(join(path, f))]
    result = {}
    for file in files:
        name = file.replace(".png", "")
        image = cv2.imread(path + "/" + file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result[name] = gray
    return result


def load_masks(path: str) -> dict:  # load masks from path
    files = [f for f in listdir(path) if isfile(join(path, f))]
    result = {}
    for file in files:
        name = file.replace(".png", "")
        image = cv2.imread(path + "/" + file)
        result[name] = image
    return result


def match_text(source: np.ndarray, words: tuple) -> bool:  # match target text
    st = pytesseract.image_to_string(source, lang="eng")
    for word in words:
        if word not in st:
            return False
    return True
