import configparser
import getpass
import logging
import sys

from assemblyline_client.al_cli_old import file_handler
from assemblyline_client.al_cli_old import al_var
from os import path
from assemblyline_client import get_client
import requests

"""
Filename:       al_server_client.py
Description:    This file is communicated with an instance of Assemblyline
Authors:        Joshua Mukasa
Version:        0.2.2
Last Updated:   07/30/2020
"""

# creating config parser and reading the config file
config = configparser.ConfigParser()

# Checking if the config.ini file exists and creating one if it doesn't
if not path.exists(al_var.CONFIG_FILE_PATH):
    file_handler.create_settings_file()
config.read(al_var.CONFIG_FILE_PATH)

# Adding a timeout to all requests made using the requests library
old_send = requests.Session.send


def new_send(*args, **kwargs):
    if kwargs.get("timeout", None) is None:
        kwargs["timeout"] = int(config["requests"]["timeout"]) if config.has_option("requests", "timeout") else None
    return old_send(*args, **kwargs)


requests.Session.send = new_send


def print_doc(dictionary, dictionary_name, key):
    if key:
        if key in dictionary:
            print(dictionary[key])
        else:
            logging.error("The key '{}' was not found".format(key))
            ("The '{}' dictionary contains the following keys".format(dictionary_name))
            print(dictionary.keys())
        return
    print("\n\n_____________________________________________________________________")
    print("SECTIONS: " + dictionary_name.upper())
    print("_____________________________________________________________________")
    for key in dictionary:
        print("\n{}:\n".format(key.upper()))
        print('\t' + str(dictionary[key]).replace('\n', '\n\t'))


class AlServerClient:
    connection = None

    def __init__(self):
        try:
            self.connection = get_client(
                config["server"]["host"] if config.has_option("server", "host") else "",
                apikey=(
                    config["user"]["username"] if config.has_option("user", "username") else "",
                    config["user"]["apikey"] if config.has_option('user', 'apikey') else ''
                )
            )
        except Exception as e:
            print(e, file=sys.stderr)
            return

    def extend_priv(self):
        password = getpass.getpass(prompt='Password: ')
        try:
            self.connection = get_client(
                config["server"]["host"] if config.has_option("server", "host") else "",
                auth=(
                    config["user"]["username"] if config.has_option("user", "username") else "",
                    password
                )
            )
        except Exception as e:
            print(e, file=sys.stderr)
            return

    # noinspection PyArgumentList
    def help(self, section=None, key=None):
        api_help = {
            'alert': self.help_alert,
            'bundle': self.help_bundle,
            'file': self.help_file,
            'hashsearch': self.help_hashsearch,
            'heuristics': self.help_heuristics,
            'ingest': self.help_ingest,
            'live': self.help_live,
            'result': self.help_result,
            'search': self.help_search,
            'signature': self.help_signature,
            'submission': self.help_submission,
            'submit': self.help_submit,
            'user': self.help_user,
            'workflow': self.help_workflow
        }
        if section:
            if section in api_help:
                api_help[section](key)
            else:
                print("The section '{}' was not found".format(section))
            return
        for section in api_help:
            api_help[section]()

    def help_alert(self, key=None):
        alert = {
            'label': self.connection.alert.label.__doc__,
            'ownership': self.connection.alert.ownership.__doc__,
            'priority': self.connection.alert.priority.__doc__,
            'status': self.connection.alert.status.__doc__
        }
        print_doc(alert, "alert", key)

    def help_bundle(self, key=None):
        bundle = {
            'import_bundle': self.connection.bundle.import_bundle.__doc__,
            'create': self.connection.bundle.create.__doc__
        }
        print_doc(bundle, "bundle", key)

    def help_file(self, key=None):
        file = {
            'children': self.connection.file.children.__doc__,
            'download': self.connection.file.download.__doc__,
            'result': self.connection.file.result.__doc__,
            'ascii': self.connection.file.ascii.__doc__,
            'hex': self.connection.file.hex.__doc__,
            'info': self.connection.file.info.__doc__,
            'score': self.connection.file.score.__doc__,
            'strings': self.connection.file.strings.__doc__,
        }
        print_doc(file, "file", key)

    def help_hashsearch(self, key=None):
        hashsearch = {
            'list': self.connection.hash_search.list_data_sources.__doc__,
            'search': self.connection.hash_search.__doc__

        }
        print_doc(hashsearch, "hashsearch", key)

    def help_heuristics(self, key=None):
        heuristics = {
            'stats': self.connection.heuristics.stats.__doc__
        }
        print_doc(heuristics, "heuristics", key)

    def help_ingest(self, key=None):
        ingest = {
            'message': self.connection.ingest.get_message.__doc__,
            'message_list': self.connection.ingest.get_message_list.__doc__,
        }
        print_doc(ingest, "ingest", key)

    def help_live(self, key=None):
        live = {
            'message_list': self.connection.live.get_message_list.__doc__,
            'setup_watch_queue': self.connection.live.setup_watch_queue.__doc__,
        }
        print_doc(live, "live", key)

    def help_result(self, key=None):
        result = {
            'error': self.connection.result.error.__doc__,
            'multiple': self.connection.result.multiple.__doc__,
        }
        print_doc(result, "result", key)

    def help_search(self, key=None):
        search = {
            'file': self.connection.search.file.__doc__,
            'submission': self.connection.search.submission.__doc__,
            'alert': self.connection.search.alert.__doc__,
            'heuristic': self.connection.search.heuristic.__doc__,
            'result': self.connection.search.result.__doc__,
            'signature': self.connection.search.signature.__doc__,
            'workflow': self.connection.search.workflow.__doc__
        }
        print_doc(search, "search", key)

    def help_signature(self, key=None):
        signatures = {
            'stats': self.connection.signature.stats.__doc__,
            'download': self.connection.signature.download.__doc__,
            'add_update': self.connection.signature.add_update.__doc__,
            'add_update_many': self.connection.signature.add_update_many.__doc__,
            'update_available': self.connection.signature.update_available.__doc__,
        }
        print_doc(signatures, "signatures", key)

    def help_submission(self, key=None):
        submission = {
            'file': self.connection.submission.file.__doc__,
            'is_completed': self.connection.submission.is_completed.__doc__,
            'delete': self.connection.submission.delete.__doc__,
            'full': self.connection.submission.full.__doc__,
            'summary': self.connection.submission.summary.__doc__,
            'tree': self.connection.submission.tree.__doc__,
        }
        print_doc(submission, "submission", key)

    def help_submit(self, key=None):
        submit = {
            'resubmit': self.connection.submit.resubmit.__doc__,
            'dynamic': self.connection.submit.dynamic.__doc__
        }
        print_doc(submit, "submit", key)

    def help_user(self, key=None):
        user = {
            'submission_params': self.connection.user.submission_params.__doc__
        }
        print_doc(user, "user", key)

    def help_workflow(self, key=None):
        workflow = {
            'labels': self.connection.workflow.labels.__doc__
        }
        print_doc(workflow, "workflow", key)
