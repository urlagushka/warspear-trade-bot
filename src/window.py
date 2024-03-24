import ctypes
from ctypes import wintypes

import win32gui
import win32ui
import numpy as np
from PIL.Image import Image as pil_image, frombuffer
from numpy import ndarray


# Class for capture target window && get target window position
class Window:  # window struct
    def __init__(self, window_name: str) -> None:
        self.target_window = window_name
        self.status = True

    def get_position(self) -> tuple:  # get window position
        hwnd = ctypes.windll.user32.FindWindowW(0, self.target_window)
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
        return rect.left, rect.top, rect.right, rect.bottom

    def get_image(self) -> ndarray:  # get window screenshot
        open_cv_image = np.array(self.invisible(self.target_window))
        return open_cv_image[:, :, ::-1].copy()

    @staticmethod
    def invisible(window_name) -> pil_image: # get window screenshot using win32api
        hwnd = win32gui.FindWindow(None, window_name)
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = wintypes.RECT()
        dwma_extended_frame_bounds = 9
        f(wintypes.HWND(hwnd), wintypes.DWORD(dwma_extended_frame_bounds), ctypes.byref(rect), ctypes.sizeof(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        hwnddc = win32gui.GetWindowDC(hwnd)
        mfcdc = win32ui.CreateDCFromHandle(hwnddc)
        savedc = mfcdc.CreateCompatibleDC()
        savebitmap = win32ui.CreateBitmap()
        savebitmap.CreateCompatibleBitmap(mfcdc, width, height)
        savedc.SelectObject(savebitmap)
        ctypes.windll.user32.PrintWindow(hwnd, savedc.GetSafeHdc(), 1)
        bmpinfo = savebitmap.GetInfo()
        bmpstr = savebitmap.GetBitmapBits(True)
        im_scr = frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(savebitmap.GetHandle())
        savedc.DeleteDC()
        mfcdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnddc)
        return im_scr
