rd /s /q lib
C:\Python310\python.exe -m pip install pyinstaller

C:\Python310\python.exe -m PyInstaller --name Printer --onefile src/main.py


mkdir dist\config
copy config\* dist\config\

mkdir dist\files
copy files\* dist\files\

pause
