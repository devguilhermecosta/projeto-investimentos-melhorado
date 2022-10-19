import sys

from cx_Freeze import Executable, setup

build_exe_options: dict = {'packages': ['sqlite3',
                                        'abc',
                                        'time',
                                        'tkinter',
                                        'ttkthemes',
                                        ]
                           }

base: str = ''

if sys.platform == 'win32':
    base = "Win32GUI"

executables: str = (
    [
        Executable("app.py",
                   base=base,
                   icon='images/logo.ico',
                   )
        ]
    )

setup(
    name = 'PyInvest',
    version = '1.0.0',
    description = 'Aplicativo para controle de investimentos',
    options = {'build_exe': build_exe_options},
    executables = executables,
)

# command line para compilar -> python setup.py build
