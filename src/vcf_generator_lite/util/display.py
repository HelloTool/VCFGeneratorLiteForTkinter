"""
大部分代码来自 https://github.com/TomSchimansky/CustomTkinter/blob/master/customtkinter/windows/widgets/scaling/scaling_tracker.py
"""
import sys
from tkinter import Misc


def set_process_dpi_aware():
    """
    设置进程默认 DPI 感知级别。
    """
    pass


def get_scale_factor(misc: Misc) -> float:
    """
    获取缩放因子。

    在不同操作系统上获取缩放因子，以便在高 DPI 屏幕上正确显示界面。
    缩放因子影响如何将逻辑坐标转换为屏幕坐标。

    :param misc: Misc对象
    :return: 缩放因子，如果无法确定则默认返回 1.0。
    """
    return 1.0


if sys.platform == "win32":
    from .display_windows import *

# _default_dpi = 96
# _process_dpi_aware = False
#
#
# def _set_process_dpi_aware_win8_1():
#     from ctypes import windll
#     windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
#
#
# def _set_process_dpi_aware_win7():
#     from ctypes import windll
#     windll.user32.SetProcessDPIAware()
#
#
# def set_process_dpi_aware():
#     """
#     设置进程默认 DPI 感知级别。
#
#     该函数尝试将当前进程设置为 DPI 感知模式，以便在高 DPI 显示器上正确缩放。
#     它针对不同的 Windows 版本尝试不同的设置方法。如果在所有尝试均失败或在非 Windows 平台上运行，
#     则该函数不会产生任何影响。
#
#     https://learn.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
#     """
#     global _process_dpi_aware
#     if sys.platform == 'win32':
#         for setter in (
#             _set_process_dpi_aware_win8_1,
#             _set_process_dpi_aware_win7,
#         ):
#             try:
#                 setter()
#             except (ImportError, AttributeError, OSError):
#                 pass
#             else:
#                 _process_dpi_aware = True
#                 break
#     else:
#         # 不支持缩放，忽略操作
#         pass
#
#
# def _get_scale_factor_win8_1(misc: Misc) -> float:
#     from ctypes import windll, pointer
#     from ctypes.wintypes import HWND, DWORD, UINT
#     user32 = windll.user32
#     shcore = windll.shcore
#     dpi_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
#     window_hwnd = HWND(misc.winfo_id())
#     monitor_handle = user32.MonitorFromWindow(window_hwnd,
#                                                      DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
#     dpi_x, dpi_y = UINT(), UINT()
#     shcore.GetDpiForMonitor(monitor_handle, dpi_type, pointer(dpi_x), pointer(dpi_y))
#
#     return (dpi_x.value + dpi_y.value) / 2 / _default_dpi
#
#
# def _get_scale_factor_win2000() -> float:
#     from ctypes import windll, WinError, get_last_error
#     hdc = windll.user32.GetDC(None)
#     if not hdc:
#         raise WinError(get_last_error())
#
#     try:
#         gdi32 = windll.gdi32
#         dpi_x = gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
#         dpi_y = gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
#     finally:
#         windll.user32.ReleaseDC(None, hdc)
#
#     return (dpi_x + dpi_y) / 2 / _default_dpi
#
#
# def get_scale_factor(misc: Misc) -> float:
#     """
#     获取缩放因子。
#
#     在不同操作系统上获取缩放因子，以便在高 DPI 屏幕上正确显示界面。
#     缩放因子影响如何将逻辑坐标转换为屏幕坐标。
#
#     :param misc: Misc对象
#     :return: 缩放因子，如果无法确定则默认返回 1.0。
#     """
#     if not _process_dpi_aware:
#         return 1.0
#     if sys.platform == "win32":
#         for getter in (
#             lambda: _get_scale_factor_win8_1(misc),
#             _get_scale_factor_win2000,
#         ):
#             try:
#                 return getter()
#             except (ImportError, AttributeError, OSError):
#                 pass
#
#     # 不支持缩放，默认返回1
#     return 1.0
