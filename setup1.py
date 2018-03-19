from cx_Freeze import setup, Executable

base = None    

executables = [Executable("exeTest.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "LordTest",
    options = options,
    version = "1.0",
    description = 'first test exe',
    executables = executables
)
