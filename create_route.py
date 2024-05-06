import subprocess
import os
from config import config


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


def make_route(ips):
    '''Добавление постоянного маршрута'''
    for ip in ips:
        subprocess.Popen(
            f'route -p add {ip} mask {config.get('mask')} {get_ip()}', shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def delete_route(ips):
    '''Удаление старого постоянного маршрута'''

    for ip in ips:
        result = subprocess.Popen(
            f'route delete {ip}', shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
