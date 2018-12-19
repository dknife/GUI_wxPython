# run this code
# to build executable
#    % python setup.py build
# to build installer
#    % python setup.py bdist_msi
import sys
from cx_Freeze import setup, Executable

setup(  name = "scheduler",
        version = "0.5",
        description = "scheduler",
        author = "dknife",
        executables = [Executable("TUScheduler.py", base="Win32GUI")])

