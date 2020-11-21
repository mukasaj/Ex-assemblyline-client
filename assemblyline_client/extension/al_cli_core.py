import configparser
import getpass
import os
import pickle
import sys
import time
from os import path
import json
import requests
import logging

from assemblyline_client import get_client

from assemblyline_client.extension import file_handler, al_var
from assemblyline_client.extension.services.service_manager import ServiceManager

"""
Filename:       al_cli_core.py
Description:    This file is communicated with an instance of Assemblyline
Authors:        Joshua Mukasa & Liam Henley-Vachon
Version:        0.4.0
Last Updated:   07/30/2020
"""

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

# TODO: look into combining with the run functions
def output(json_content, minimal=False, out=None):
    if not json_content:
        return
    try:

        if out is None:
            # TODO: add support for printing up nested json/arrays
            if al_var.DEV:
                for key in json_content:
                    print('{}:\t\t{}'.format(key, str(json_content[key])))
            else:
                print(json.dumps(json_content, indent=4, sort_keys=True).replace('{', '').replace('}', '').replace('[',
                                                                                                                   '').replace(
                    ']', '').replace(',', ''))
                # print_json(json_content)
        else:
            with open(out, 'w') as fi:
                fi.write(
                    str(json_content) if minimal else json.dumps(json_content, indent=4, sort_keys=True).replace('{',
                                                                                                                 '').replace(
                        '}', '').replace('[', '').replace(']', '').replace(',', ''))
    except Exception as e:
        print(e, file=sys.stderr)
        return


class Main:
    connection = None
    cache = {}

    def __init__(self):
        try:
            self.connection = get_client(config["server"]["host"], apikey=(config["user"]["username"], config["user"]["apikey"]))
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        self.service = ServiceManager()
        if path.exists(al_var.CACHE_FILE):  # Loading cache file if it exists
            with open(al_var.CACHE_FILE, 'rb') as file:
                self.cache = pickle.load(file)
                file.close()

    def __exit__(self):
        if not self.cache:  # Return if dictionary is empty
            return
        with open(al_var.CACHE_FILE, 'wb') as file:
            pickle.dump(self.cache, file)
            file.close()

    def test(self):
        pass

    def extend_priv(self):
        password = getpass.getpass(prompt='Password: ')
        try:
            self.connection = get_client(config["server"]["host"], auth=(config["user"]["username"], password))
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    def delkey(self, name, out=None, minimal=None):
        self.run(self.server.extend_priv)
        output(self.run(self.connection.auth.delete_apikey, name), minimal=minimal, out=out)

    def keygen(self, name, priv, out=None, minimal=None):
        self.run(self.extend_priv)
        output(self.run(self.connection.auth.generate_apikey, name=name, priv=priv), minimal=minimal, out=out)

    def alert_label(self, alert_id, labels, out=None, minimal=None):
        output(self.run(self.connection.alert.label, alert_id, labels), minimal=minimal, out=out)

    def bundle(self, sid):
        data = self.run(self.connection.bundle.create, sid)

        filename = sid + ".bundle"
        counter = 1
        if path.exists(filename):
            while path.exists("bundle/" + filename):
                filename = sid + "({}).bundle".format(counter)
                counter += 1

        if data:
            with open("bundle/" + filename, "wb") as file:
                file.write(data)

    def import_bundle(self, filename, min_classification=None):
        if not os.path.exists(filename):
            logging.error("'{}' bundle not found".format(filename))
            return

        self.run(self.connection.bundle.import_bundle, filename, min_classification=min_classification)

    def file_download(self, sha256, sid=None, encoding=None):
        data = self.run(self.connection.file.download, sha256=sha256, sid=sid, encoding=encoding)
        if data and sha256:
            if not os.path.isdir(al_var.DOWNLOADS):
                os.mkdir(al_var.DOWNLOADS)
            with open(al_var.DOWNLOADS + sha256 + ".cart", "wb") as file:
                file.write(data)

    def file_children(self, sha256, minimal=None, out=None):
        data = self.run(self.connection.file.children, sha256=sha256)
        if not data:
            logging.warning("No children found")
            return
        output(data, minimal=minimal, out=out)

    def file_info(self, sha256, minimal=None, out=None):
        output(self.run(self.connection.file.info, sha256=sha256), minimal=minimal, out=out)

    def file_result(self, sha256, service=None, minimal=None, out=None):
        output(self.run(self.connection.file.result, sha256=sha256, service=service), minimal=minimal, out=out)

    def file_ascii(self, sha256, minimal=None, out=None):
        output(self.run(self.connection.file.ascii, sha256=sha256), minimal=minimal, out=out)

    def file_hex(self, sha256, minimal=None, out=None):
        output(self.run(self.connection.file.hex, sha256=sha256), minimal=minimal, out=out)

    def file_score(self, sha256, minimal=None, out=None):
        output(self.run(self.connection.file.score, sha256=sha256), minimal=minimal, out=out)

    def file_strings(self, sha256, minimal=None, out=None):
        output(self.run(self.connection.file.strings, sha256=sha256), minimal=minimal, out=out)

    def submit(self, file=None, url=None, sha256=None, minimal=None, out=None):
        if file:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.iso':
                self.run(self.submit_iso, file)
                return

            if os.path.getsize(file) > al_var.MAX_FILE_SIZE:
                logging.error(f"'{os.path.basename(file)}' skipped, filesize over {al_var.MAX_FILE_SIZE / 1000000}mb")
                return

            file = str(file).replace("\\", '/')

        elif url:  # removing the needing slash, users sometimes copy urls with an extra slash
            url = url[:-1] if str(url).endswith('/') else url

        data = self.run(self.connection.submit, file, url=url, sha256=sha256)

        if isinstance(data, dict):
            # Caching sid and getting results
            self.get_results(data['sid'], minimal=minimal, out=out)

    def submit_iso(self, iso):
        self.service.iso.extract(iso)
        error_occurred = False
        sid_list = []
        for file in self.service.iso.get_paths():
            if os.path.getsize(file) < al_var.MAX_FILE_SIZE:
                data = self.run(self.connection.submit, file)
                if data:
                    print(os.path.basename(file) + " SID: " + data['sid'])
                    sid_list.append(data['sid'])
                else:
                    error_occurred = True
                    # TODO: log errors
                    logging.error(f"'{os.path.basename(file)}' failed to submit")
            else:
                logging.warning(f"'{os.path.basename(file)}' skipped, filesize over {al_var.MAX_FILE_SIZE / 1000000}mb")

        if error_occurred:
            logging.error("some files failed to submit ")

    def resubmit(self, sid, minimal=None, out=None):
        data = self.run(self.server.connection.submit.resubmit, sid)

        # Caching the new sid and getting results
        self.get_results(data['sid'], minimal=minimal, out=out)

    def auto_resubmit(self, minimal=None, out=None):
        if 'sid' not in self.cache:
            logging.error("No cached sid")
            return
        self.resubmit(self.cache['sid'], minimal=minimal, out=out)

    def dynamic_resubmit(self, sha256, sid=None, name=None, minimal=None, out=None):
        data = self.run(self.connection.submit.dynamic, sha256=sha256, copy_sid=sid, name=name)
        if isinstance(data, dict):
            self.get_results(data['sid'], minimal=minimal, out=out)

    def signature_stats(self, submission_id, minimal=None, out=None):
        output(self.run(self.connection.signature.stats), minimal=minimal, out=out)

    def submission(self, submission_id, minimal=None, out=None):
        output(self.run(self.connection.submission, submission_id), minimal=minimal, out=out)

    def submission_delete(self, sid, minimal=None, out=None):
        output(self.run(self.connection.submission.delete, sid), minimal=minimal, out=out)

    def submission_full(self, sid, minimal=None, out=None):
        output(self.run(self.connection.submission.full, sid), minimal=minimal, out=out)

    def submission_summary(self, sid, minimal=None, out=None):
        output(self.run(self.connection.submission.summary, sid), minimal=minimal, out=out)

    def submission_tree(self, sid, minimal=None, out=None):
        output(self.run(self.connection.submission.tree, sid), minimal=minimal, out=out)

    def get_results(self, sid, minimal=None, out=None):
        print("Waiting for the results, press ctrl+c to cancel")
        try:
            while self.connection.submission.is_completed(sid) is False:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logging.warning("\nCanceled loading of results for submission '" + sid + "'")
            return

        # Get results for the submission
        output(self.run(self.connection.submission, sid), minimal=minimal, out=out)

    # try catch wrapper for calling server functions
    def run(self, func, *args, **kwargs):
        if al_var.DEBUG:
            data = func(*args, **kwargs)
            if isinstance(data, dict):
                if 'sid' in data:
                    self.cache['sid'] = data['sid']
                    print("Cache sid: {}".format(data['sid']))
            return data

        try:
            data = func(*args, **kwargs)
            # cache sid if response contains it
            if isinstance(data, dict):
                if 'sid' in data:
                    self.cache['sid'] = data['sid']
            return data
        except requests.exceptions.ReadTimeout:
            logging.error("The request timed out")
            return
        except Exception as e:
            logging.error(e)
            return

    def check_cache(self):
        print("Content of cache")
        print(self.cache)

    def clear_cache(self):
        self.cache = None
        os.remove(al_var.CACHE_FILE)
