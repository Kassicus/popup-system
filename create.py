import PyInstaller.__main__

PyInstaller.__main__.run([
    '--clean',
    '-y',
    '-n',
    "SystemUptime24Package",
    '--add-data=assets/fonts/Roboto-Regular.ttf;assets/fonts',
    'main.py'
])