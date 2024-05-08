### Установка зависимостей
```shell
pip install -r requirements.txt
```
### Компиляция в exe
```shell
pyinstaller --onefile --windowed --icon=icon.ico --add-data="icon.ico":"icon.ico" -n "vpn-ozna-arp" vpn-ozna.py
```
