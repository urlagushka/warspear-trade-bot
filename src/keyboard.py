from pywinauto.keyboard import send_keys
from pyautogui import write, press


def write_message(text: str) -> None:
    words = text.split(" ")
    for word in words:
        write_word(word)
        write_space()


def write_word(text: str) -> None:
    for t in text:
        send_keys(t)


def write_space() -> None:
    write(" ")


def erase() -> None:
    press("backspace", presses=100)
