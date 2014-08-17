# import subprocess
import pyperclip
import os

# def cp2Clip(txt):
# cmd='echo ' + txt.strip() + '|clip'
# subprocess.check_call(cmd, shell=True)

pyperclip.copy(os.getcwd().replace('\\', '/'))
print(pyperclip.paste())