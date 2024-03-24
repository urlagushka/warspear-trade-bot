from pyautogui import click, mouseDown, mouseUp
from src.window import Window
from src.interface import Interface

from time import sleep


def global_click(pos: tuple, amount: int, cnf: dict) -> None:  # click by global cords
    for i in range(amount):
        click(x=pos[0], y=pos[1])
        sleep(cnf["click"]["delay"])


def local_click(w_pos: tuple, t_pos: tuple, amount: int, cnf: dict) -> None:  # click by local cords
    global_click((w_pos[0] + t_pos[0] + 10 + t_pos[2] / 2, w_pos[1] + t_pos[1] + 30 + t_pos[3] / 2), amount, cnf)


def mask_click(win: Window, inf: Interface, mask: str, amount: int, cnf: dict) -> None:  # click by mask
    image = win.get_image()
    global_pos = win.get_position()
    local_pos = inf.match_mask(image, mask)
    local_click(global_pos, local_pos, amount, cnf)


def hold_mask_click(win: Window, inf: Interface, mask: str, drt: float) -> None:  # hold click by mask
    image = win.get_image()
    w_pos = win.get_position()
    t_pos = inf.match_mask(image, mask)
    mouseDown(x=(w_pos[0] + t_pos[0] + 10 + t_pos[2] / 2), y=(w_pos[1] + t_pos[1] + 30 + t_pos[3] / 2))
    sleep(drt)
    mouseUp()
