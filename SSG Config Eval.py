
##############################################################################
#   Author: Jeremy Edge  #    Date: 2017-08-22     #       Version: 1        #
##############################################################################
# Description:                                                               #
#                                                                            #
##############################################################################

# Permanent imports.
import sys
import os.path
import datetime

# Debug imports.
import time

# Setting static variables
op_sys = sys.platform
if op_sys == "win32":
    dir_sep = '\\'
elif op_sys == 'linux2':
    dir_sep = "/"
else:
    dir_sep = "|"
d_date = str(datetime.date.year) + "-" + str(datetime.date.month) + "-" + str(datetime.date.day)


# Getting the SSG config file name from the user.
print("What is the filename?")
filename = sys.stdin.readline().rstrip()

# Confirming the folder that the file should be in.
print("Is it in this directory?")
print(os.getcwd() + dir_sep)
print("[Y|N|y|n|Yes|No|YES|NO]")
yesno = sys.stdin.readline().rstrip()
if yesno == "yes" or yesno == "y" or yesno == "YES" or yesno == "Y" or yesno == "Yes":
    filename = os.getcwd() + dir_sep + filename
elif yesno == "no" or yesno == "n" or yesno == "NO" or yesno == "N" or yesno == "No":
    print("Okay, what is the correct folder?")
    folder = sys.stdin.readline().rstrip()
    if not(folder.endswith(dir_sep)):
        folder = folder + dir_sep
    filename = folder + filename
else:
    print("Invalid option.")
    exit()

# Checking if file exists.
print("Checking to make sure this file exists.")
print(filename)
if not(os.path.exists(filename)):
    print("The specified file does not exist.")
    exit()

# Reading the files in to a list.
with open(filename, 'r') as infile:
    full_config = infile.read().splitlines()

for line in full_config:
    print(line)
    time.sleep(1)
