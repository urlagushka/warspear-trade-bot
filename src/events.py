import cv2

from src.window import Window
from src.interface import Interface, match_text
from src.mouse import mask_click, hold_mask_click
from src.keyboard import write_message, erase
from time import sleep
import numpy as np


def crop(win: Window, offset: tuple) -> np.ndarray:  # crop image using central points
    image = win.get_image()
    w = image.shape[1] - 2
    h = image.shape[0] - 32
    cx = int(w / 2)
    cy = int(h / 2)
    return image[(cy + offset[1]):(cy + offset[3]), (cx + offset[0]):(cx + offset[2])]


def chat_event(win: Window, inf: Interface, cnf: dict, message: str, backspace: bool) -> bool:  # process message send
    for mask in ("person_mask", "chat_mask"):
        mask_click(win, inf, mask, 1, cnf)
        if check_for_trade(win):
            return False

    if backspace:
        erase()
    write_message(message)
    if check_for_trade(win):
        return False

    for mask in ("enter_mask", "close_mask"):
        mask_click(win, inf, mask, 1, cnf)
        if check_for_trade(win):
            return False
    return True


def check_for_trade(win: Window) -> bool:
    return match_text(win.get_image(), ("you", "to"))


def wait_for_trade(win: Window, cnf: dict) -> None:  # analyze image for trade
    print(win.target_window + " | waiting for trade...")
    while not match_text(win.get_image(), (
            "offers",
            "you",
            "to",
            "trade"
    )):
        sleep(cnf["trade"]["delay"])


def wait_for_player(win: Window, cnf: dict) -> None:  # analyze image for player accept
    print(win.target_window + " | waiting for player...")
    while True:
        image = win.get_image()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        status = match_text(gray, ("CANCEL"))
        if not status:
            break
        sleep(cnf["trade"]["delay"])


def trade_event(win: Window, interface: Interface, inf: dict, cnf: dict) -> None:  # process trade with player
    print(win.target_window + " | Trade started")
    mask_click(win, interface, "yes_mask", 1, cnf)
    sleep(1)

    while True:  # wait for other person
        flag = crop(win, inf["flag"])
        avg = np.average(flag, axis=0)[0]
        if avg[0] < 60:
            break

    if avg[2] > 100:  # cancel trade if red
        mask_click(win, interface, "cancel_mask", 1, cnf)
        print(win.target_window + " | Trade canceled")

    else:  # response trade
        slot = crop(win, inf["slot1"])
        print(np.average(slot, axis=0)[0])
        if not np.array_equal(slot, interface.patterns["empty_mask"]):
            mask_click(win, interface, "cancel_mask", 1, cnf)
            print(win.target_window + " | Trade canceled, slots not empty")
            return

        received = crop(win, inf["receive"])
        price = interface.font.match_price(received)
        print(win.target_window + " | Trade price ", str(price))
        print(win.target_window + " | Trade amount ", str(price / cnf["trade"]["price"]))

        if price < cnf["trade"]["price"] or price % cnf["trade"]["price"] != 0:  # cancel trade if price incorrect
            print(win.target_window + " | Trade price incorrect")
            mask_click(win, interface, "cancel_mask", 1, cnf)
            print(win.target_window + " | Trade canceled")
            return

        amount = int(price / cnf["trade"]["price"])
        if amount > cnf["trade"]["current_amount"]:  # cancel trade if not enough piece
            mask_click(win, interface, "cancel_mask", 1, cnf)
            print(win.target_window + " | Trade canceled, too much")
            return

        mask_click(win, interface, "slot_mask", 2, cnf)
        mask_click(win, interface, cnf["trade"]["mask"], 1, cnf)
        mask_click(win, interface, "add_mask", 1, cnf)

        mask_click(win, interface, "less_mask", 1, cnf)
        received = crop(win, inf["choose"])
        possible = interface.font.match_price(received)
        mask_click(win, interface, "more_mask", 1, cnf)
        if possible < int(price / cnf["trade"]["price"]):
            mask_click(win, interface, "cancel_mask", 1, cnf)
            mask_click(win, interface, "trade_close_mask", 1, cnf)
            mask_click(win, interface, "cancel_mask", 1, cnf)
            print(win.target_window + " | Trade canceled, not enough space")
            return

        amount = amount - amount % cnf["click"]["step"]
        hold_mask_click(win, interface, "more_mask", cnf["click"]["hold"][str(amount)])
        received = crop(win, inf["choose"])
        choose = interface.font.match_price(received)

        if choose < int(price / cnf["trade"]["price"]) / 10:  # scroll back if out
            received = crop(win, inf["choose"])
            cur = interface.font.match_price(received)
            while cur != int(price / cnf["trade"]["price"]):
                mask_click(win, interface, "less_mask", 1, cnf)
                received = crop(win, inf["choose"])
                cur = interface.font.match_price(received)
        else:
            diff = int(price / cnf["trade"]["price"]) - choose  # scroll for target
            if diff > 0:
                mask_click(win, interface, "more_mask", abs(diff), cnf)
            elif diff < 0:
                mask_click(win, interface, "less_mask", abs(diff), cnf)

        mask_click(win, interface, "ok_mask", 1, cnf)
        mask_click(win, interface, "ok_mask", 1, cnf)
        sleep(1)
        mask_click(win, interface, "done_mask", 1, cnf)
        sleep(1)
        wait_for_player(win, cnf)
        cnf["trade"]["current_amount"] -= int(price / cnf["trade"]["price"])
        print(win.target_window + " | Trade complete, current amount: " + str(cnf["trade"]["current_amount"]))
