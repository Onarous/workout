import pygetwindow as gw
import time
import os
import ast
import ctypes
import psutil
import tkinter as tk
# Список браузеров для проверки открытых сайтов
browser_list = ["browser.exe", "msedge.exe", "firefox.exe", "chrome.exe", "opera.exe", "brave.exe", "chromium.exe"]


file_path = "settings.txt" # Создание файла настроек, если он не существует
if not os.path.isfile(file_path):
    with open(file_path, 'w', encoding="UTF8") as file:
        wr = {"mode": "whitelist",
              "app_list": {"explorer.exe", "Taskmgr.exe", "ShellExperienceHost.exe", "ApplicationFrameHost.exe", "pycharm64.exe"},
              "sites_list": {"Youtube"}}
        file.write(str(wr))


def get_active_window_pid(): # получение активного процесса
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


# def please_close():
#     root.title("")
#     root.attributes("-topmost", True)
#     root.attributes("-alpha", 0.85)
#     root.attributes("-toolwindow", True)
#     root.resizable(False, False)
#     w = root.winfo_screenwidth()
#     h = root.winfo_screenheight()
#     w = w // 2  # середина экрана
#     h = h // 2
#     w = w - 200  # смещение от середины
#     h = h - 200
#     root.geometry(f'400x130+{w}+{h}')
#     label = tk.Label(root, text="Вернитесь к работе", font=40)
#     label.pack(pady=50)


def whitelist_check_window(l_name):
    in_list = False
    with open(file_path, "r", encoding="UTF8") as f:  # Открытия файла с настройками
        d = ast.literal_eval(f.read())
        if l_name in browser_list:  # Если процесс является браузером
            l_name = gw.getActiveWindow().title
            for i in d["sites_list"]:  # Проверка, есть ли сайт в списке
                if i.lower() in l_name.lower():
                    in_list = True
        else:  # Если процесс не является браузером
            for i in d["app_list"]:  # Проверка, есть ли программа в списке
                if i.lower() in l_name.lower():
                    in_list = True
    return in_list


# root = tk.Tk()
while True:
    # Получаем активное окно
    active_pid = get_active_window_pid()
    process = psutil.Process(active_pid)
    name = process.name()
    print(process.name())

    with open(file_path, "r", encoding="UTF8") as f: # Открытия файла с настройками
        d = ast.literal_eval(f.read())
        if d["mode"] == "whitelist": # Выбор режима белого списка
            in_list = whitelist_check_window(name)

    if not in_list:
        print("Закройте окно")
        # please_close()
        # root.protocol("WM_DELETE_WINDOW", please_close)
        # root.mainloop()
    else:
        # root.destroy()
        # root = tk.Tk()
        print("ok")



    time.sleep(10)