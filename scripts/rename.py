import os
import pandas as pd
import subprocess

def index(path = "./", suffix = "trj"):
    files = [nm for nm in os.listdir(path) if suffix in nm]
    files.sort()
    return files

def rename(files, old_str, new_str, path):
    for f in files:
        print("############################")
        print(f)
        f_new=f.replace(old_str,new_str)
        subprocess.call(f"mv {path}/{f} {path}/{f_new}", shell=True) 
        print(f_new)


#files=index(suffix="r_alphaT1", path="data/")
#rename(files, "_r", "_ups1_r", path="data/")
