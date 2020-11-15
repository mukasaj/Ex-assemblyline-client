import os
import pickle
import sys
import time
from os import path
from al_server_client import AlServerClient
import json
import al_var
import requests
import logging

from services.service_manager import ServiceManager

"""
Filename:       al_cli_core.py
Description:    This file is communicated with an instance of Assemblyline
Authors:        Joshua Mukasa & Liam Henley-Vachon
Version:        0.4.0
Last Updated:   07/30/2020
"""


# TODO: testing, and fix bugs found
# TODO: get results from a single inside a folder/zip
# TODO: user docs

# def print_json(dic):
#     for key, value in dic.items():
#         if isinstance(value, dic):
#             print(key + ":")
#             print_json(dic)
#         if isinstance(value, list):
#             print(key + ":")
#         else:
#             print("{0}: {1}".format(key, value))

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
    server = None
    cache = {}

    def __init__(self):
        self.server = AlServerClient()
        self.service = ServiceManager()
        if path.exists(al_var.CACHE_FILE):  # Loading cache file if it exists
            with open(al_var.CACHE_FILE, 'rb') as file:
                self.cache = pickle.load(file)
                file.close()

    def __exit__(self):
        if not self.cache:  # Return if dictionary is empty
            return


            file.close()

    def test(self):
        # sha256 = "3ac4f5f42e2be505d538522422fc4cb88cb5396a855d11486ca0dcf349cba270"

        # iso_path = 'ubuntu.iso'
        # self.service.iso.extract(iso_path)
        # #print(self.service.iso.get_paths())
        # paths = self.service.iso.get_paths()
        # error_occurred = False
        # sid_list = []
        # for filepath in paths:
        #     time.sleep(60)
        #     if os.path.getsize(filepath) < 100000000:
        #         data = self.run(self.server.connection.submit, filepath)
        #         if data:
        #             print(os.path.basename(filepath)+" SID: "+data['sid'])
        #             sid_list.append(data['sid'])
        #         else:
        #             error_occurred = True
        #             logging.error(f"'{os.path.basename(filepath)}' failed to submit")
        #     else:
        #         logging.warning(f"'{os.path.basename(filepath)}' was skipped, filesize over 100mb")
        #
        # if error_occurred:
        #     logging.error("some files failed to submit ")
        pass

    def delkey(self, name, out=None, minimal=None):
        self.run(self.server.extend_priv)
        output(self.run(self.server.connection.auth.delete_apikey, name), minimal=minimal, out=out)

    def keygen(self, name, priv, out=None, minimal=None):
        self.run(self.server.extend_priv)
        output(self.run(self.server.connection.auth.generate_apikey, name=name, priv=priv), minimal=minimal, out=out)

    def alert_label(self, alert_id, labels, out=None, minimal=None):
        output(self.run(self.server.connection.alert.label, alert_id, labels), minimal=minimal, out=out)

    def bundle(self, sid):
        data = self.run(self.server.connection.bundle.create, sid)

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

        self.run(self.server.connection.bundle.import_bundle, filename, min_classification=min_classification)

    def file_download(self, sha256, sid=None, encoding=None):
        data = self.run(self.server.connection.file.download, sha256=sha256, sid=sid, encoding=encoding)
        if data and sha256:
            if not os.path.isdir(al_var.DOWNLOADS):
                os.mkdir(al_var.DOWNLOADS)
            with open(al_var.DOWNLOADS + sha256 + ".cart", "wb") as file:
                file.write(data)

    def file_children(self, sha256, minimal=None, out=None):
        data = self.run(self.server.connection.file.children, sha256=sha256)
        if not data:
            logging.warning("No children found")
            return
        output(data, minimal=minimal, out=out)

    def file_info(self, sha256, minimal=None, out=None):
        output(self.run(self.server.connection.file.info, sha256=sha256), minimal=minimal, out=out)

    def file_result(self, sha256, service=None, minimal=None, out=None):
        output(self.run(self.server.connection.file.result, sha256=sha256, service=service), minimal=minimal, out=out)

    def file_ascii(self, sha256, minimal=None, out=None):
        output(self.run(self.server.connection.file.ascii, sha256=sha256), minimal=minimal, out=out)

    def file_hex(self, sha256, minimal=None, out=None):
        output(self.run(self.server.connection.file.hex, sha256=sha256), minimal=minimal, out=out)

    def file_score(self, sha256, minimal=None, out=None):
        output(self.run(self.server.connection.file.score, sha256=sha256), minimal=minimal, out=out)

    def file_strings(self, sha256, minimal=None, out=None):
        output(self.run(self.server.connection.file.strings, sha256=sha256), minimal=minimal, out=out)

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

        data = self.run(self.server.connection.submit, file, url=url, sha256=sha256)

        if isinstance(data, dict):
            # Caching sid and getting results
            self.get_results(data['sid'], minimal=minimal, out=out)

    def submit_iso(self, iso):
        self.service.iso.extract(iso)
        error_occurred = False
        sid_list = []
        for file in self.service.iso.get_paths():
            if os.path.getsize(file) < al_var.MAX_FILE_SIZE:
                data = self.run(self.server.connection.submit, file)
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
        data = self.run(self.server.connection.submit.dynamic, sha256=sha256, copy_sid=sid, name=name)
        if isinstance(data, dict):
            self.get_results(data['sid'], minimal=minimal, out=out)

    def signature_stats(self, submission_id, minimal=None, out=None):
        output(self.run(self.server.connection.signature.stats), minimal=minimal, out=out)

    def submission(self, submission_id, minimal=None, out=None):
        output(self.run(self.server.connection.submission, submission_id), minimal=minimal, out=out)

    def submission_delete(self, sid, minimal=None, out=None):
        output(self.run(self.server.connection.submission.delete, sid), minimal=minimal, out=out)

    def submission_full(self, sid, minimal=None, out=None):
        output(self.run(self.server.connection.submission.full, sid), minimal=minimal, out=out)

    def submission_summary(self, sid, minimal=None, out=None):
        output(self.run(self.server.connection.submission.summary, sid), minimal=minimal, out=out)

    def submission_tree(self, sid, minimal=None, out=None):
        output(self.run(self.server.connection.submission.tree, sid), minimal=minimal, out=out)

    def get_documentation(self, section=None, key=None):
        self.server.help(section=section, key=key)

    def get_results(self, sid, minimal=None, out=None):
        print("Waiting for the results, press ctrl+c to cancel")
        try:
            while self.server.connection.submission.is_completed(sid) is False:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logging.warning("\nCanceled loading of results for submission '" + sid + "'")
            return

        # Get results for the submission
        output(self.run(self.server.connection.submission, sid), minimal=minimal, out=out)

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
