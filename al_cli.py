"""
Filename:       al_cli_old.py
Description:    This file is responsible for running the main loop of the program and calling all necessary functions
Authors:        Liam Henley-Vachon & Joshua Mukasa
Version:        0.2.0
Last Updated:   07/20/2020
"""
import logging

import atexit
from assemblyline_client.extension import help_functions, file_handler, command_validations, al_var
from sys import argv
import argparse
from assemblyline_client.extension.al_cli_core import Main
import re

print()

# Reading arguments from command line
parser = argparse.ArgumentParser(description="Assemblyline client commands")
# General flag
parser.add_argument('--menu', action="store_true", help="Open menu")
parser.add_argument('--service', type=str, help="List")
parser.add_argument('--dev', action="store_true", help="enable dev mode")
parser.add_argument('--debug', action="store_true", help="enable debug mode")
parser.add_argument('--check_cache', action="store_true", help="check cache contents")
parser.add_argument('--clear_cache', action="store_true", help="clear cache")
parser.add_argument('--config', action="store_true", help="update config")
parser.add_argument('-m', '--minimal', action="store_true", help="Set minimal flag for output")
parser.add_argument('-t', '--test', action="store_true", help="used to check for errors")
parser.add_argument('-o', '--out', type=str, help="Output results to a file")
# auth
parser.add_argument('--delkey', type=str, help="delete key")
parser.add_argument('--keygen', type=str, help="generate key")
parser.add_argument('--READ_WRITE', action="store_true", help="set read write priv")
parser.add_argument('--READ', action="store_true", help="set read priv")
parser.add_argument('--WRITE', action="store_true", help="set write priv")
# Bundle flags
parser.add_argument('-b', '--bundle', type=str, help="Create bundle from SID")
parser.add_argument('-ib', '--import_bundle', type=str, help="Import bundle")
# File flags
parser.add_argument('-d', '--download', type=str, help="Download file using sha256 indicator")
parser.add_argument('-fc', '--file_children', type=str, help="File children using sha256 indicator")
parser.add_argument('-fi', '--file_info', type=str, help="File info using sha256 indicator")
parser.add_argument('-fr', '--file_result', type=str, help="File result using sha256 indicator")
parser.add_argument('-fa', '--file_ascii', type=str, help="File ascii using sha256 indicator")
parser.add_argument('-fh', '--file_hex', type=str, help="File hex using sha256 indicator")
parser.add_argument('-fs', '--file_score', type=str, help="File score using sha256 indicator")
parser.add_argument('--file_strings', type=str, help="File strings using sha256 indicator")

# Submit flags
parser.add_argument('-f', '--file', type=str, help="submit file for analysis, use quotes from paths with spaces")
parser.add_argument('-u', '--url', type=str, help="submit url for analysis")
parser.add_argument('--sha', type=str, help="submit sha256 for analysis")
parser.add_argument('-rl', '--resubmit_last', action="store_true", help="resubmit the last submitted file")
parser.add_argument('-r', '--resubmit', type=str, help="resubmit file")
parser.add_argument('-rd', '--resubmit_dynamic', type=str, help="Dynamic resubmit file")

# Signature flags
parser.add_argument('--signature_stats', action='store_true', help="get signature stats")

# Submission flags
parser.add_argument('-s', '--submission', type=str, help="get submission")
parser.add_argument('-sd', '--submission_delete', type=str, help="delete a submission")
parser.add_argument('-sf', '--submission_full', type=str, help="get full submission")
parser.add_argument('-ss', '--submission_summary', type=str, help="get submission summary")
parser.add_argument('-st', '--submission_tree', type=str, help="get submission tree")

# User flags
parser.add_argument('--user', action="store_true", help="update user info")

args = parser.parse_args()

# flag that must run before cli_core instance is created
if args.debug:
    al_var.DEBUG = True
if args.dev:
    al_var.DEV = True
if args.config:
    file_handler.update()

# create and instance of cli_core
clientCore = Main()

# General
if args.test:
    clientCore.test()
if args.check_cache:
    clientCore.check_cache()
if args.clear_cache:
    clientCore.clear_cache()
# auth
if args.delkey:
    clientCore.delkey(args.delkey, minimal=args.minimal, out=args.out)
if args.keygen:
    priv = None
    if args.READ:
        priv = 'READ'
    elif args.WRITE:
        priv = 'WRITE'
    elif args.READ_WRITE:
        priv = 'READ_WRITE'

    if priv:
        clientCore.keygen(args.keygen, priv, minimal=args.minimal, out=args.out)
    else:
        logging.error("Missing priv, can't generate key")
# Bundle
if args.bundle:
    clientCore.bundle(args.bundle)
if args.import_bundle:
    clientCore.import_bundle(args.import_bundle)
# File
if args.download:
    clientCore.file_download(args.download)
if args.file_children:
    clientCore.file_children(args.file_children, minimal=args.minimal, out=args.out)
if args.file_info:
    clientCore.file_info(args.file_info, minimal=args.minimal, out=args.out)
if args.file_result:
    clientCore.file_result(args.file_result, minimal=args.minimal, out=args.out, service=args.service)
if args.file_ascii:
    clientCore.file_ascii(args.file_ascii, minimal=args.minimal, out=args.out)
if args.file_hex:
    clientCore.file_hex(args.file_hex, minimal=args.minimal, out=args.out)
if args.file_score:
    clientCore.file_score(args.file_score, minimal=args.minimal, out=args.out)
if args.file_strings:
    clientCore.file_strings(args.file_strings, minimal=args.minimal, out=args.out)
# User
if args.user:
    file_handler.update_user()
# Submit
if args.file:
    clientCore.submit(file=args.file, minimal=args.minimal, out=args.out)
if args.url:
    clientCore.submit(url=args.url, minimal=args.minimal, out=args.out)
if args.sha:
    clientCore.submit(sha256=args.sha, minimal=args.minimal, out=args.out)
if args.resubmit_last:
    clientCore.auto_resubmit(minimal=args.minimal, out=args.out)
if args.resubmit:
    clientCore.resubmit(args.resubmit, minimal=args.minimal, out=args.out)
if args.resubmit_dynamic:
    clientCore.dynamic_resubmit(args.resubmit_dynamic, minimal=args.minimal, out=args.out)
# Signature
if args.signature_stats:
    clientCore.signature_stats(args.signature_stats, minimal=args.minimal, out=args.out)
# Submission
if args.submission:
    clientCore.submission(args.submission, minimal=args.minimal, out=args.out)
if args.submission_delete:
    clientCore.submission_delete(args.submission_delete, minimal=args.minimal, out=args.out)
if args.submission_full:
    clientCore.submission_full(args.submission_full, minimal=args.minimal, out=args.out)
if args.submission_summary:
    clientCore.submission_full(args.submission_summary, minimal=args.minimal, out=args.out)
if args.submission_tree:
    clientCore.submission_full(args.submission_tree, minimal=args.minimal, out=args.out)

# If there is more than 1 command line argument or the user sets the -m flag, continue to CLI menu
if len(argv) <= 1 or args.menu:
    # Assemblyline title in ASCII art
    print("    ___                             __    __      ___          ")
    print("   /   |  _____________  ____ ___  / /_  / /_  __/ (_)___  ___ ")
    print("  / /| | / ___/ ___/ _ \/ __ `__ \/ __ \/ / / / / / / __ \/ _ \\")
    print(" / ___ |(__  |__  )  __/ / / / / / /_/ / / /_/ / / / / / /  __/")
    print("/_/  |_/____/____/\___/_/ /_/ /_/_.___/_/\__, /_/_/_/ /_/\___/ ")
    print("                                        /____/                 \n")
    print("To see a list of commands, type 'help'")
    minimal = None
    if minimal:
        print("Yes")

    # This function runs the start of the cli and is the main program loop
    def main_function():

        # Submit regex
        command_reg = re.compile(
            '^(alert|auth|bundle|documentation|error|file|hash_search|heuristics|ingest|live|result|search|service'
            '|signature|submission|submit|sysconfig|user|webauthn|workflow){1}$')

        # Boolean to control program loop. Will run until program is False
        program = True

        # This loop is responsible for the running the program logic
        while program:
            command = ""
            # Get the users command
            while command == "":
                command = input("(al_cli_old) $ ")
            split_comm = command.split()
            if split_comm[0] == "help":
                # If the user types help for a specific command
                if len(split_comm) == 2:
                    # If the command matches one of the keys in the dictionary, call that keys function
                    if split_comm[1] in help_functions.help_commands_list.keys():
                        help_functions.help_commands_list[split_comm[1]]()
                    else:
                        print("Invalid command")
                else:
                    # Print the list of commands that have a help menu available
                    help_functions.help_commands()
            elif command_reg.match(split_comm[0]):
                if split_comm[0] in command_validations.commands_list.keys():
                    if command_validations.commands_list[split_comm[0]](command) == -1:
                        print("Invalid command")
            elif split_comm[0] == "quit" or split_comm[0] == "exit":
                program = False
            else:
                print("Invalid command")


    main_function()

if __name__ == '__main__':
    atexit.register(clientCore.__exit__)
