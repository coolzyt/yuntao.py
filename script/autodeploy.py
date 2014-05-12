#coding=utf8
__author__ = 'yuntao.zyt'
import subprocess
import os
import datetime
print("Prepare file system")
os.system("rm -rf ./deployfiles")
os.system("mkdir ./deployfiles")
os.chdir("./deployfiles")
print("Downloading files")
subprocess.check_output(["svn","checkout","https://github.com/coolzyt/yuntao.py/trunk/"])
print("Removing .svn files")
curdir = subprocess.check_output(["pwd"]).decode("utf8").strip()
tmpsvnfiles =subprocess.check_output(["find",curdir, "-name" ,".svn"]).decode("utf8")
for line in tmpsvnfiles.split("\n"):
    folder = line.strip()
    os.system("rm -rf %s"%folder)
bakdir = datetime.datetime.now().strftime("%Y%m%d%H%M");
print("Backuping current files")
os.mkdir("/opt/bak/%s/"%bakdir)
os.system("mv /opt/www/yuntao.org/* /opt/bak/%s/"%bakdir)
print("Deploying new files")
os.system("mv /opt/deployfiles/trunk/* /opt/www/yuntao.org/")
print("Finished!")