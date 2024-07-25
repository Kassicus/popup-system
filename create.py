import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--clean',
    '-y',
    '-n',
    "TestPopup",
    '--add-data=assets/fonts/Roboto-Regular.ttf;assets/fonts',
    '--add-data=assets/images/nexus_logo.png;assets/images',
    '--add-data=assets/sounds/test.wav;assets/sounds',
    'main.py'
])