import pip
from subprocess import call
import os,sys

#获取python文件当前路径
print(os.path.dirname(sys.argv[0]))
for dist in pip.get_installed_distributions():
    cmd = "pip install --upgrade " + dist.project_name
    print(cmd)
    call(cmd, shell=True)
