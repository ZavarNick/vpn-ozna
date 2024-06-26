import tkinter as tk

from create_route import *
from config import config


class App(tk.Frame):
    def __init__(self, master):

        # Создание vpn соединения
        self.create_vpn()

        # Выключение использования общего шлюза
        split_tunneling_switch()

        tk.Frame.__init__(self, master)
        self.pack()

        # Создание label для ввода данных
        self.prompt_email = tk.Label(self, text="Введите логин:", anchor="w")

        # Создание поля для ввода данных почты
        self.email = tk.Entry(self)

        # Создание label для ввода данных пароля
        self.prompt_passwd = tk.Label(self, text="Введите пароль:", anchor="w")

        # Создание поля для ввода данных пароля со скрытием
        self.passwd = tk.Entry(self, show='*')

        # Создание кнопки Ввод
        self.submit = tk.Button(self, text="Ввод", command=self.vpn_connect)

        # Создание радио кнопки показать пароль
        self.checkbox = tk.Checkbutton(self, text='показать пароль', command=self.show_passwd)

        # Поле для вывода сообщения
        self.output = tk.Label(self, text="")

        # Установка и расположение объектов на фрейме
        self.prompt_email.pack(side="top", fill="x", padx=20, pady=5)
        self.email.pack(fill="x", padx=20)
        self.prompt_passwd.pack(side="top", fill="x", padx=20, pady=5)
        self.passwd.pack(side="top", fill="x", padx=20)
        self.checkbox.place(x=15, y=100)
        self.output.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="bottom", fill="x", padx=20, pady=20)

    @staticmethod
    def create_vpn():
        '''Создание VPN соединения'''

        subprocess.call(
            f'powershell.exe -WindowStyle hidden Add-VpnConnection -Name VPN-OZNA -ServerAddress {config.get('ip')} -TunnelType "Pptp"',
            shell=True)

    def vpn_connect(self):
        '''Подключение VPN'''
        try:
            result = subprocess.run(f'powershell.exe -WindowStyle hidden rasdial VPN-OZNA {self.email.get()} {self.passwd.get()}',
                                    check=True)

            # Вывод сообщения на фрейм
            self.output.configure(text='Соединения установлено')

            # Удаления старого постоянного маршрута
            delete_route(config.get('ip_network'))

            # Создание постоянного маршрута для обхода трафика компании
            make_route(config.get('ip_network'))

            # После паузы в 3 секунды закрывается окно
            root.after(3000, root.destroy)

        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                # Вывод сообщения на фрейм
                self.output.configure(text='Ошибка подключения, проверьте логин или пароль')

    def show_passwd(self):
        '''Скрывает/показывает пароль'''
        if self.passwd.cget('show') == '*':
            self.passwd.config(show='')
        else:
            self.passwd.config(show='*')


if __name__ == '__main__':
    root = tk.Tk()

    # Устанавливаем заголовок окна
    root.title("Создание VPN подключения")

    # Устанавливаем размеры окна
    root.geometry("350x250")

    App(root).pack(fill="both", expand=True)
    root.mainloop()
