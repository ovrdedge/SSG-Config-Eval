
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
    folder = os.getcwd() + dir_sep
    full_filename = folder + filename
elif yesno == "no" or yesno == "n" or yesno == "NO" or yesno == "N" or yesno == "No":
    print("Okay, what is the correct folder?")
    folder = sys.stdin.readline().rstrip()
    if not(folder.endswith(dir_sep)):
        folder = folder + dir_sep
    full_filename = folder + filename
else:
    # Defining folder and full_filename here to make pycharm happy. Don't really need it here since i'm exiting.
    folder = os.getcwd() + dir_sep
    full_filename = folder + filename
    print("Invalid option.")
    exit()

# Checking if file exists.
print("Checking to make sure this file exists.")
print(full_filename)
if not(os.path.exists(full_filename)):
    print("The specified file does not exist.")
    exit()

# Sanity check here to make sure the file i'm about to read in, isn't war and peace. 10meg should be enough.
if os.path.getsize(full_filename) > 10485760:
    print("That file seems kind of excessive.")
    exit()

# Reading the files in to a list.
with open(full_filename, 'r') as infile:
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
    if line.startswith("set service") and ("dst-port" in line or "timeout" in line):
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

    # Copying the policy objects in to its own array. This section may need more stuff as more complicated SSG's are
    # exposed.
    elif line.startswith("set policy id") \
            or line.startswith("set log session-init") \
            or line.startswith("set src-address") \
            or line.startswith("set dst-address") \
            or line.startswith("set service"):
        policy_config.extend([line])

    else:
        remainder_config.extend([line])

# Offering to dump the arrays in to individual text files.
print("Before we go any further, do you want to dump the split config in to text files?")
print("[Y|N|y|n|Yes|No|YES|NO]")
yesno = sys.stdin.readline().rstrip()

if yesno == "yes" or yesno == "y" or yesno == "YES" or yesno == "Y" or yesno == "Yes":

    # Prefix to use to build the dump file names. This assumes it has an extension.
    if filename.endswith(".txt"):
        part_filename, throw_away = filename.rsplit('.', 1)
    else:
        part_filename = filename

    # Dumping service_config. Files are going in same place as the original file.
    throw_away = folder + dir_sep + part_filename + "-" + "services-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in service_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping interface_config
    throw_away = folder + dir_sep + part_filename + "-" + "interfaces-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in interface_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping nat_config
    throw_away = folder + dir_sep + part_filename + "-" + "nat-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in nat_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping address_config
    throw_away = folder + dir_sep + part_filename + "-" + "addresses-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in address_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping addgroup_config
    throw_away = folder + dir_sep + part_filename + "-" + "address_group-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in addgroup_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping policy_config
    throw_away = folder + dir_sep + part_filename + "-" + "policy-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in policy_config:
        out_file.write(line + "\n")
    out_file.close()

    # Dumping remainder_config
    throw_away = folder + dir_sep + part_filename + "-" + "remainder-" + filedate + ".txt"
    out_file = open(throw_away, 'w')
    for line in remainder_config:
        out_file.write(line + "\n")
    out_file.close()

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

    # Pulling the timeout off the string and sticking it in the dictionary.
    if " timeout" in line:
        line, service_objects[i]['timeout'] = line.split(' timeout ', 1)
    elif "timeout" in line:
            line, service_objects[i]['timeout'] = line.split('timeout ', 1)
    else:
        service_objects[i]['timeout'] = None

    # Pulling out the destination port and sticking it in the dictionary.
    if "dst-port" in line:
        line, service_objects[i]['dst-port'] = line.split(' dst-port ')
    else:
        service_objects[i]['dst-port'] = None

    # Pulling out the source port and sticking it in the dictionary. Don't really need this for ASA but it's there.
    if "src-port" in line:
        line, service_objects[i]['src-port'] = line.split(' src-port ')
    else:
        service_objects[i]['src-port'] = None

    # Finally grabbing the protocol and sticking it in the dictionary.
    if "protocol tcp" in line:
        service_objects[i]['protocol'] = 'tcp'
        service_objects[i]['additive'] = False
    elif "protocol udp" in line:
        service_objects[i]['protocol'] = 'tcp'
        service_objects[i]['additive'] = False
    elif "+ tcp" in line:
        service_objects[i]['protocol'] = 'tcp'
        service_objects[i]['additive'] = True
    elif "+ udp" in line:
        service_objects[i]['protocol'] = 'udp'
        service_objects[i]['additive'] = True
    else:
        service_objects[i]['protocol'] = None
        service_objects[i]['additive'] = False

    # Incrementing i
    i += 1

# Processing address objects.
i = 0
address_objects = []
for line in address_config:

    # Grabbing the original line in case i need to display to user.
    original_line = line

    # Expanding array
    address_objects.append({})

    # Remove "set address "".
    line = line.replace('set address "', '')

    # Probably could do all of this logic with just splitting on the " " into an array except for the comments.
    # Sticking the zone in the dictionary.
    address_objects[i]['zone'], line = line.split('" "', 1)

    # Sticking the name in the dictionary.
    address_objects[i]['name'], line = line.split('" ', 1)

    # Sticking the address in the dictionary.
    if line[:1].isdigit():
        address_objects[i]['address'], line = line.split(' ', 1)
    else:
        # Have to pop the last entry in the array since its crap.
        address_objects.pop()
        print('Command not understood: "' + original_line + '"')
        continue

    # Sticking the subnet mask in the dictionary. Also checking for comments.
    if " " in line:
        address_objects[i]['mask'], line = line.split(' ', 1)
        address_objects[i]['comment'] = line.replace('"', '')
    else:
        address_objects[i]['mask'] = line
        address_objects[i]['comment'] = None

    # Incrementing i
    i += 1

# Processing NAT.
i = 0
nat_objects = []
for line in nat_config:

    # Grabbing the original line in case i need to display to user.
    original_line = line

    # Expanding array
    nat_objects.append({})

    # Stripping off the first part of the command.
    line = line.replace('set interface "', '')

    # Gambling that i can evenly split the remaining fields on ' '. Will double check to make sure its the right size.
    temp_array = line.split(' ')
    if len(temp_array) != 9:
        nat_objects.pop()
        print("Command not understood " + original_line + '"')
        continue

    # Pulling out the interface that the nat is bound to. Not sure i need it, but whatever.
    nat_objects[i]['interface'] = temp_array[0].replace('"', '')

    # Pulling out the inside global IP. Don't care about index 1.
    nat_objects[i]['global'] = temp_array[2]

    # Pulling out the inside local IP. Don't care about index 3.
    nat_objects[i]['local'] = temp_array[4]

    # Pulling out the netmask. Might care later when building objects but not so far. Don't care about index 5.
    nat_objects[i]['mask'] = temp_array[6]

    # Pulling out the vrf in case it's needed. Don't care about index 7.
    nat_objects[i]['vrf'] = temp_array[8].replace('"', '')

    # Incrementing i
    i += 1

# Processing address groups.
i = 0
addgroup_objects = []
for line in addgroup_config:

    # Grabbing the original line in case i need to display to user.
    original_line = line

    # Expanding array
    addgroup_objects.append({})

    # Stripping off the first part of the command.
    line = line.replace('set group address "', '')

    # Couldn't split on ' ' due to more than one text sections with spaces. So will have to nibble at it.
    if '" add "' in line or '" comment "' in line:

        # Pulling the zone out.
        addgroup_objects[i]['zone'], line = line.split('" "', 1)

        if '" add "' in line:

            # Pulling the address group name out.
            addgroup_objects[i]['name'], line = line.split('" add "', 1)
            addgroup_objects[i]['name'] = addgroup_objects[i]['name'].replace('"', '')

            # Pulling the address name out.
            addgroup_objects[i]['address'] = line.replace('"', '')

        else:
            # Pulling the address group name out.
            addgroup_objects[i]['name'], line = line.split('" comment "', 1)
            addgroup_objects[i]['name'] = addgroup_objects[i]['name'].replace('"', '')

            # Pulling the comment out.
            addgroup_objects[i]['comment'] = line.replace('"', '')

    else:
        # Have to pop the last entry in the array since its crap.
        addgroup_objects.pop()
        print('Command not understood: "' + original_line + '"')
        continue

    # Incrementing i
    i += 1

# Processing interface config.
i = 0
interface_objects = []
for line in interface_config:

    # Grabbing the original line in case i need to display to user.
    original_line = line

    # Expanding array
    addgroup_objects.append({})

    # Incrementing i
    i += 1

# Processing policy config. This loop is different than the previous ones. This will generate a 3 dimensional array.
# It also has a forward looking scan of the policy_config array since additional items are declared on following lines.
# First dimension is an array with each rule getting its own index.
# Second dimension is a dictionary that has specifics like zones, action, and logging.
# Third dimension is an array but only for certain things from second dimension (like src-add, dst-add, dst-port).
i = 0
j = 0
loop = True
policy_objects = []
while loop:

    # The first entry in the policy_config array must be a line with a full policy entry. If not something went wrong.
    if not(policy_config[j].startswith('set policy id') and ' from ' in policy_config[j]):
        print("Something went wrong with the policy import.")
        exit()

    # Putting the current line in a variable so i don't change the original.
    line = policy_config[j]

    # Expanding array
    policy_objects.append({})

    # Stripping off the set policy id part of the command.
    line = line.replace('set policy id ', '')

    # Pushing policy id into dictionary.
    policy_objects[i]['id'], line = line.split(' from "', 1)

    # Pushing source zone into dictionary.
    policy_objects[i]['src-zone'], line = line.split('" to "', 1)

    # Pushing destination zone in to dictionary.
    policy_objects[i]['dst-zone'], line = line.split('"  "', 1)

    # Pushing source address into dictionary as an array (3rd dimension).
    throw_away, line = line.split('" "', 1)
    policy_objects[i]['src-address'] = [throw_away]

    # Pushing destination address into dictionary as an array (3rd dimension).
    throw_away, line = line.split('" "', 1)
    policy_objects[i]['dst-address'] = [throw_away]

    # Pushing service address into dictionary as an array (3rd dimension).
    throw_away, line = line.split('" ', 1)
    policy_objects[i]['port'] = [throw_away]

    # Checking for url-filter
    if ' url-filter' in line:
        line = line.replace(' url-filter', '')
        policy_objects[i]['url-filter'] = True
    else:
        policy_objects[i]['url-filter'] = False

    # Checking for traffic mbw. This assumes it is the last thing on the line. If not, it will be to greedy.
    if ' traffic mbw ' in line:
        line, policy_objects[i]['rate-limit'] = line.split(' traffic mbw ', 1)
    else:
        policy_objects[i]['rate-limit'] = None

    # Checking for SNAT.
    if ' nat src' in line:
        line = line.replace(' nat src', '')
        policy_objects[i]['snat'] = True
    else:
        policy_objects[i]['snat'] = False

    # Checking if log keyword is on command line. Wish it was perl so i could use regex natively.
    if ' log' in line:
        line = line.replace(' log', '')
        policy_objects[i]['log'] = True
    else:
        policy_objects[i]['log'] = False

    # Pushing action into dictionary.
    if 'permit' in line:
        line = line.replace('permit', '')
        policy_objects[i]['action'] = 'permit'
    elif 'deny' in line:
        line = line.replace('deny', '')
        policy_objects[i]['action'] = 'deny'
    elif 'tunnel vpn' in line:

        # Pushing the vpn variables into the dictionary but don't really need them for ASA build.
        line, policy_objects[i]['pair-policy'] = line.split(' pair-policy ', 1)

        # Pushing the vpn id into the dictionary but don't really need them for ASA build.
        line, policy_objects[i]['vpn-id'] = line.split('" id ', 1)

        # Pushing the tunnel name into the dictionary. This one is may cause me fits.
        policy_objects[i]['vpn-name'] = line.replace('tunnel vpn "', '')

    # This part begins the looking forward loop.
    inner_loop = True
    while inner_loop:

        # Incrementing j
        j += 1

        # Checking if we're going to look past the current array and error out.
        if j >= len(policy_config):
            inner_loop = False
            continue

        # Checking the next entry in array to see if its part of current policy or a new one.
        elif policy_config[j].startswith('set policy id ') and ' from "' in policy_config[j]:
            inner_loop = False

        # Checking to see if the line is the empty set policy id config line. If so go around again.
        elif policy_config[j].startswith('set policy id ') and ' disable' in policy_config[j]:
            policy_objects[i]['disable'] = True
            pass

        # Checking to see if the line is the empty set policy id config line. If so go around again.
        elif policy_config[j].startswith('set policy id '):
            pass

        # Checking to see if the line is the exit line. If so go around again.
        elif policy_config[j] == 'exit':
            pass

        # Checking to see if the line is the extra log init line. Don't care. Going around again.
        elif policy_config[j] == 'set log session-init':
            pass

        # Checking to see if it's an additional source address that i need to add to the src-address array.
        elif 'set src-address ' in policy_config[j]:
            throw_away = policy_config[j]
            throw_away = throw_away.replace("set src-address ", '').replace('"', '')
            policy_objects[i]['src-address'].extend([throw_away])

        # Checking to see if it's an additional destination address that i need to add to the dst-address array.
        elif 'set dst-address ' in policy_config[j]:
            throw_away = policy_config[j]
            throw_away = throw_away.replace("set dst-address ", '').replace('"', '')
            policy_objects[i]['dst-address'].extend([throw_away])

        # Checking to see if it's an additional service port that i need to add to the service address array.
        elif 'set service "' in policy_config[j]:
            throw_away = policy_config[j]
            throw_away = throw_away.replace("set service ", '').replace('"', '')
            policy_objects[i]['port'].extend([throw_away])

        # Not sure what would hit here. But should tell the user i found something unexpected.
        else:
            print("Command not understood " + policy_config[j] + '"')

    print(policy_objects[i])

    # Incrementing i
    i += 1
    if j >= len(policy_config):
        loop = False

    if i >= 20:
        loop = False

time.sleep(1)
