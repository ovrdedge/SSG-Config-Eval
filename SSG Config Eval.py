
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
now = datetime.datetime.now()
filedate = str(now.year) + "-" + \
           str(now.month) + "-" + \
           str(now.day) + "_" + \
           str(now.hour) + "-" + \
           str(now.minute) + "-" + \
           str(now.second)

# Getting the SSG config file name from the user.
print("What is the filename? (Just the filename, directory will come next.)")
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

# ~ Should probably check here to make sure the file i'm about to read in, isn't war and peace.

# Reading the files in to a list.
with open(filename, 'r') as infile:
    full_config = infile.read().splitlines()

# Splitting the config file into multiple arrays.
service_config = []
interface_config = []
nat_config = []
address_config = []
addgroup_config = []
policy_config = []
remainder_config = []
for line in full_config:

    # Removing the stupid carriage return.
    line = line.rstrip()

    # Copying the protocol objects in to its own array.
    if line.startswith("set service"):
        service_config.extend([line])

    # Copying the zone config and interface config into it's own array. Excluding NAT stuff.
    elif line.startswith("set zone") or (line.startswith("set interface") and (" mip " not in line)):
        interface_config.extend([line])

    # Copying the nat config into it's own array.
    elif line.startswith("set interface") and " mip " in line:
        nat_config.extend([line])

    # Copying the address objects in to its own array.
    elif line.startswith("set address"):
        address_config.extend([line])

    # Copying the address group objects in to its own array.
    elif line.startswith("set group address"):
        addgroup_config.extend([line])

    # Copying the policy objects in to its own array.
    elif line.startswith("set policy id") \
            or line.startswith("set log session-init") \
            or line.startswith("set src-address") \
            or line.startswith("set dst-address") \
            or line.startswith("set service"):
        policy_config.extend([line])

    else:
        remainder_config.extend([line])


# Processing protocol objects.
i = 0
service_objects = []
for line in service_config:

    # Expanding array
    service_objects.append({})

    # Remove "set service "".
    line = line.replace('set service "', '')

    # Sticking the name in the dictionary.
    service_objects[i]['name'], line = line.split('" ', 1)
    print(service_objects[i]['name'])

    # Pulling the timeout off the string and sticking in the dictionary.
    if "timeout" in line:
        line, service_objects[i]['timeout'] = line.split('timeout ', 1)
    else:
        service_objects[i]['timeout'] = None

    print(line)

    # Incrementing i
    i += 1



time.sleep(1)
