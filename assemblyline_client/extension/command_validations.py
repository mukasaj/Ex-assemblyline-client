"""
Filename:       command_validations.py
Description:    This file contains all the error checking functions for each API command
Authors:        Liam Henley-Vachon
Version:        0.0.1
Last Updated:   07/17/2020
"""

from assemblyline_client.extension.al_cli_core import Main
import re
# TODO: Fix documentation function
# TODO: Error check help functions
# TODO: Update help functions

ClientCore = Main()


# This function performs error checking for the alert command
def alert(command):
    pass


# This function performs error checking for the auth command
def auth(command):
    pass


# This function performs error checking for the bundle command
def bundle(command):
    bundle_reg = re.compile('(\\s+)?(bundle)\\s+(((-c)\\s+\\w+)|((-i)\\s+"(.+)"))')
    args = re.search(bundle_reg, command)
    if bundle_reg.match(command):
        if args.group(5):
            ClientCore.bundle(sid=args.group(6))
        elif args.group(8):
            ClientCore.import_bundle(filename=args.group(9))
    else:
        return -1


# This function performs error checking for the documentation command
def documentation(command):
    if len(command) == 1 and command[0] == "documentation":
        pass
    else:
        return -1


# This function performs error checking for the error command
def error(command):
    pass


# This function performs error checking for the file command
def file(command):
    file_reg = re.compile(
        '(file)\\s+(-d|-ga|-gc|-gh|-gi|-gr|(-grs)\\s+(\\w+)|-gscor|-gstr)\\s+(\\w+)(\\s+)?(-m)?(\\s+)?((-o|--out)\\s+(.+))?')
    args = re.search(file_reg, command)
    if file_reg.match(command):
        if args.group(2) == "-d":
            ClientCore.file_download(sha256=args.group(5))
        elif args.group(2) == "-ga":
            ClientCore.file_ascii(sha256=args.group(5),
                                  minimal=args.group(7) if args.group(7) else None,
                                  out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gc":
            ClientCore.file_children(sha256=args.group(5),
                                     minimal=args.group(7) if args.group(7) else None,
                                     out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gh":
            ClientCore.file_hex(sha256=args.group(5),
                                minimal=args.group(7) if args.group(7) else None,
                                out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gi":
            ClientCore.file_info(sha256=args.group(5),
                                 minimal=args.group(7) if args.group(7) else None,
                                 out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gr":
            ClientCore.file_result(sha256=args.group(5),
                                   minimal=args.group(7) if args.group(7) else None,
                                   out=args.group(11) if args.group(11) else None)
        elif args.group(3):
            if args.group(3) == "-grs":
                ClientCore.file_result(sha256=args.group(5),
                                       service=args.group(4),
                                       minimal=args.group(7) if args.group(7) else None,
                                       out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gscor":
            ClientCore.file_score(sha256=args.group(5),
                                  minimal=args.group(7) if args.group(7) else None,
                                  out=args.group(11) if args.group(11) else None)
        elif args.group(2) == "-gstr":
            ClientCore.file_strings(sha256=args.group(5),
                                    minimal=args.group(7) if args.group(7) else None,
                                    out=args.group(11) if args.group(11) else None)
    else:
        return -1


# This function performs error checking for the hash_search command
def hash_search(command):
    pass


# This function performs error checking for the heuristics command
def heuristics(command):
    pass


# this function performs error checking for the ingest command
def ingest(command):
    pass


# This function performs error checking for the live command
def live(command):
    pass


# This function performs error checking for the result command
def result(command):
    pass


# This function performs error checking for the search command
def search(command):
    pass


# This function performs error checking for the service command
def service(command):
    pass


# This function performs error checking for the signature command
def signature(command):
    pass


# This function performs error checking for the submission command
def submission(command):
    sub_reg = re.compile('(\\s+)?(submission)\\s+(-d|-sub|-sum|-fr|-ft)\\s+(\\w+)(\\s+(-m))?((\\s+(-o)\\s+"(.+)")|$)')
    args = re.search(sub_reg, command)
    if sub_reg.match(command):
        if args.group(3) == "-d":
            ClientCore.submission_delete(sid=args.group(4))
        elif args.group(3) == "-sub":
            ClientCore.submission(submission_id=args.group(4),
                                  minimal=args.group(6) if args.group(6) else None,
                                  out=args.group(10) if args.group(10) else None)
        elif args.group(3) == "-sum":
            ClientCore.submission_summary(sid=args.group(4),
                                          minimal=args.group(6) if args.group(6) else None,
                                          out=args.group(10) if args.group(10) else None)
        elif args.group(3) == "-fr":
            ClientCore.submission_full(sid=args.group(4),
                                       minimal=args.group(6) if args.group(6) else None,
                                       out=args.group(10) if args.group(10) else None)
        elif args.group(3) == "-ft":
            ClientCore.submission_tree(sid=args.group(4),
                                       minimal=args.group(6) if args.group(6) else None,
                                       out=args.group(10) if args.group(10) else None)
    else:
        return -1


# This function performs error checking for the submit command
def submit(command):
    submit_reg = re.compile('(submit)\\s+(-f|--file|-u|--url|-ra|-rda)(\\s+)?(-m)?\\s+"(.+)"\\s?((-o|--out)\\s(.+)|$)')
    args = re.search(submit_reg, command)
    if submit_reg.match(command):
        if args.group(2) == "-f" or args.group(2) == "--file":
            ClientCore.submit(file=args.group(5),
                              minimal=args.group(4) if args.group(4) else None,
                              out=args.group(8) if args.group(8) else None)
        elif args.group(2) == "-u" or args.group(2) == "--url":
            ClientCore.submit(url=args.group(5),
                              minimal=args.group(4) if args.group(4) else None,
                              out=args.group(8) if args.group(8) else None)
        elif args.group(2) == "-ra":
            ClientCore.resubmit(sid=args.group(5),
                                minimal=args.group(4) if args.group(4) else None,
                                out=args.group(8) if args.group(8) else None)
        elif args.group(2) == "-rda":
            ClientCore.dynamic_resubmit(sha256=args.group(5),
                                        minimal=args.group(4) if args.group(4) else None,
                                        out=args.group(8) if args.group(8) else None)
    else:
        return -1


# This function performs error checking for the sysconfig command
def sysconfig(command):
    pass


# This function performs error checking for the user command
def user(command):
    pass


# This function performs error checking for the webauthn command
def webauthn(command):
    pass


# This function performs error checking for the workflow command
def workflow(command):
    pass


commands_list = {"alert": alert,
                 "auth": auth,
                 "bundle": bundle,
                 "documentation": documentation,
                 "error": error,
                 "file": file,
                 "hash_search": hash_search,
                 "heuristics": heuristics,
                 "ingest": ingest,
                 "live": live,
                 "result": result,
                 "search": search,
                 "service": service,
                 "signature": signature,
                 "submission": submission,
                 "submit": submit,
                 "sysconfig": sysconfig,
                 "user": user,
                 "webauthn": webauthn,
                 "workflow": workflow}
