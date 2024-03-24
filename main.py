from src.window import Window
from src.config import Config, Inf
from src.interface import Interface

from src.events import chat_event, trade_event, check_for_trade
from threading import Thread, Lock
from time import sleep


mutex = Lock()


def chat_thread(win: Window, interface: Interface, inf: dict, cnf: dict):  # thread for chat
    global mutex
    backspace = False
    while True:
        for message in cnf["messages"]:
            print(win.target_window + " | waiting " + str(message[1]) + " seconds for send < " + message[0] + " >")
            sleep(message[1])
            with mutex:
                if not chat_event(win, interface, cnf, message[0], backspace):
                    backspace = True
                    break
                backspace = False


def trade_thread(win: Window, interface: Interface, inf: dict, cnf: dict):  # thread for trade
    global mutex
    while True:
        status = check_for_trade(win)
        if status:
            with mutex:
                trade_event(win, interface, inf, cnf)
        sleep(cnf["trade"]["delay"])


if __name__ == '__main__':
    cnf = Config("config/config.json")  # path for config.json, interface.json files
    inf = Inf("config/interface.json")
    print("Config is loaded")
    interface = Interface("src", r'C:\Program Files\Tesseract-OCR\tesseract.exe')  # path for tesseract.exe
    print("Interface is loaded\n")

    print("Start in 3 seconds..")
    sleep(3)

    thread_funcs = (trade_thread, chat_thread)

    wins = {}
    for window in cnf.configs.values():  # looking for windows in config
        wins[window["name"]] = Window(window["name"])

    for win in wins.values():  # create threads for every window
        for func in thread_funcs:
            thread = Thread(target=func, args=(win, interface, inf.trade, cnf.configs[str(win.target_window)]))
            thread.setDaemon(True)
            thread.start()

    sleep(cnf.timeout)  # running program for timeout
