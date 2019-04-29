import cx_Freeze
import sys
import os


include_files = ["clienticon.ico","C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tcl86t.dll","C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tk86t.dll"]

# os.environ['TCL_LIBRARY'] = "C:\\Program Files\\Python35\\tcl\\tcl8.6"
os.environ['TCL_LIBRARY'] = "C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
# os.environ['TK_LIBRARY'] = "C:\\Program Files\\Python35\\tcl\\tk8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("program.py", base=base,icon="clienticon.ico")]



cx_Freeze.setup(
    name = "ProgramTest-Client",
    options = {"build_exe": {"packages": ["tkinter","pyodbc"], "include_files": include_files}},
    verion = "0.01",
    description = "plz work",
    executables = executables
)

# include_files - include any files included in the script (images)
