import subprocess
import os


def get_ip():
    '''Узнаем локальный IP адрес VPN подключения '''
    result = subprocess.Popen(
        f'powershell.exe (Get-NetIPAddress -InterfaceAlias "VPN-OZNA" -AddressFamily IPv4).IPAddress', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return result.stdout.read().decode("utf-8").strip()


def split_tunneling_switch():
    '''Отключаем использование общего шлюза'''
    result = subprocess.Popen(
        f'powershell.exe Set-VpnConnection -Name "VPN-OZNA" -SplitTunneling $True', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def make_route():
    '''Добавление постоянного маршрута'''
    result = subprocess.Popen(
        f'route -p add {os.getenv('IP_NETWORK')} mask {os.getenv('MASK')} {get_ip()}', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def delete_route():
    '''Удаление старого постоянного маршрута'''
    result = subprocess.Popen(
        f'route delete {os.getenv('IP_NETWORK')}', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
