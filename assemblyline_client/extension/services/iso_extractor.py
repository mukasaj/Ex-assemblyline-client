import os
import zipfile
import shutil
import pycdlib

"""
Filename:       iso_extractor.py
Description:    Service to extract contents of iso and packing into zip archives for submission to Assemblyline
Authors:        Joshua Mukasa
Version:        1.0
Last Updated:   08/11/2020
"""

class Iso:
    _iso = None
    _iso_temp = "iso_temp"
    _iso_extracted = "iso_packs"
    _max_iso_pack_size = 5000000
    _max_iso_pack_items = 200

    def __init__(self):
        self.iso = pycdlib.PyCdlib()

    def extract(self, filename):
        self.iso.open(filename)

        # creating the temp folder if it does not exist
        temp_folder = os.path.join(os.path.dirname(__file__), self._iso_temp)
        if os.path.isdir(temp_folder):
            shutil.rmtree(temp_folder)
        os.mkdir(temp_folder)

        # creating the extract folder if it does not exist
        extract_folder = os.path.join(os.path.dirname(__file__), self._iso_extracted)
        if os.path.isdir(extract_folder):
            shutil.rmtree(extract_folder)
        os.mkdir(extract_folder)

        # Writing files from iso to temp folder
        for dirname, dirlist, filelist in self.iso.walk(iso_path='/'):
            for file in filelist:
                record = self.iso.get_record(iso_path=dirname + "/" + file)
                if not record.is_symlink():
                    trimmed_filename = file.replace(';1', '')
                    self.iso.get_file_from_iso(
                        iso_path=dirname + "/" + file,
                        local_path=os.path.join(os.path.dirname(__file__), self._iso_temp, trimmed_filename)
                    )

        counter = 1
        current_size = 0
        zip_name = "iso_pack({}).zip"
        zip_path = os.path.join(os.path.dirname(__file__), self._iso_extracted, zip_name.format(counter))

        # Writing the files in temp folder in to zip archives
        zf = zipfile.ZipFile(zip_path, "w")
        for dirname, dirlist, filelist in os.walk(os.path.join(os.path.dirname(__file__), self._iso_temp)):
            for file in filelist:
                current_size += os.path.getsize(os.path.join(os.path.dirname(__file__), self._iso_temp, file))
                zf.write(os.path.join(os.path.dirname(__file__), self._iso_temp, file), arcname=file)
                # If archive has 150 items or is over max size create a new archive
                if len(zf.filelist) >= 1000 or current_size > self._max_iso_pack_size:
                    current_size = 0
                    counter += 1
                    zf.close()
                    zip_path = os.path.join(os.path.dirname(__file__), self._iso_extracted, zip_name.format(counter))
                    zf = zipfile.ZipFile(zip_path, "w")

        # delete temp folder
        shutil.rmtree(temp_folder)
        # close iso and archive
        zf.close()
        self.iso.close()

    def get_paths(self):
        file_paths = []
        # get the path of the extract folder
        extract_folder = os.path.join(os.path.dirname(__file__), self._iso_extracted)
        for dirname, dirlist, filelist in os.walk(extract_folder):
            # add the file names in the extract folder to the file_path list
            for file in filelist:
                filepath = os.path.join(extract_folder, file)
                file_paths.append(filepath.replace('\\', '/'))
        return file_paths

