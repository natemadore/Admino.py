#!/usr/bin/env python3

import argparse
import subprocess
import os

# define the command-line arguments and help messages
parser = argparse.ArgumentParser(description="Welcome to the Admino system information script")
subparsers = parser.add_subparsers(dest="subcommand")

help_msg = "Show IP address of network interface. Usage: -1 <network adapter>"
parser_ip = subparsers.add_parser("-1", help=help_msg)
parser_ip.add_argument("interface", help="network interface")

help_msg = "Show hostname information. Usage: -2"
subparsers.add_parser("-2", help=help_msg)

help_msg = "List system users. Usage: -3"
subparsers.add_parser("-3", help=help_msg)

help_msg = "List users by group. Usage: -4 <user group> "
parser_group = subparsers.add_parser("-4", help=help_msg)
parser_group.add_argument("group", help="group name")

help_msg = "List files owned by a specific user in a directory. Usage: -5 <user> <directory>"
parser_files = subparsers.add_parser("-5", help=help_msg)
parser_files.add_argument("username", help="name of the user")
parser_files.add_argument("directory", help="directory to search")

help_msg = "Create and encrypt a zip file for all files in directory. Usage: -6 <directory> <zip name>"
parser_zip = subparsers.add_parser("-6", help=help_msg)
parser_zip.add_argument("folder", help="directory to zip")
parser_zip.add_argument("zipfile", help="name of the zip file")

help_msg = "Directory list for a system user. Usage: -7 <directory>"
parser_dir = subparsers.add_parser("-7", help=help_msg)
parser_dir.add_argument("directory", help="directory to list")

help_msg = "List of IPs and number of connections from system users. Usage: -8"
subparsers.add_parser("-8", help=help_msg)

help_msg = "Test internet and display the external IP address of the device. Usage: -9"
subparsers.add_parser("-9", help=help_msg)

# parse the arguments and execute the corresponding function
args = parser.parse_args()
# begin functions for admino

# IP address of a Network Interface
if args.subcommand == "-1":
    cmd = f"ip -br add show | grep {args.interface} | awk '{{print $3}}' | awk -F '/' '{{print $1}}'"
    output = subprocess.check_output(cmd, shell=True)
    print(f"Your ip for {args.interface} interface is: {output.decode().strip()}")

# Hostname Information
elif args.subcommand == "-2":
    cmd = "hostnamectl status"
    subprocess.run(cmd, shell=True)

# List of Users in the System
elif args.subcommand == "-3":
    cmd = "cut -d: -f1 /etc/passwd"
    subprocess.run(cmd, shell=True)

# List Users in a Specific Group
elif args.subcommand == "-4":
    cmd = f"getent group {args.group} | cut -d: -f4 | tr ',' '\n'"
    output = subprocess.check_output(cmd, shell=True)
    print(f"The list of users in the {args.group} group is:\n{output.decode().strip()}")

# List the number of files owned by a specific user from a particular directory
elif args.subcommand == "-5":
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        exit(1)

    cmd = f"find {args.directory} -user {args.username} -print"
    output = subprocess.check_output(cmd, shell=True)
    print(f"Files owned by {args.username} in {args.directory}:")
    print(output.decode().strip())

# Create abd encrypt a zip file for all the files in a directory
elif args.subcommand == "-6":
    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} is not a directory")
        exit(1)

    cmd = f"zip -e {args.zipfile} {args.folder}"
    subprocess.run(cmd, shell=True)

# Directory list of System User
elif args.subcommand == "-7":
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        exit(1)

    cmd = f"tree {args.directory} -a"
    subprocess.run(cmd, shell=True)

# List of IPs and number of connections from where the system's users have connected
elif args.subcommand == "-8":
    cmd = "last | grep 'pts' | awk '{print $3}' | uniq -c"
    subprocess.run(cmd, shell=True)

#Test internet connection speed and show external IP address
elif args.subcommand == "-9":
    cmd = "curl ifconfig.me"
    output = subprocess.check_output(cmd, shell=True)
    print(f"External IP address of the device is: {output.decode().strip()}")

else:
    parser.print_help()
    exit(1)
