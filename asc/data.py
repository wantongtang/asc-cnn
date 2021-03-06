# -*- coding: utf-8 -*-

""" Data module

This module lets the program to download the data from the server.

"""
import os
import requests
import shutil
import sys
import zipfile


class Data(object):
    """ Data collection.
    """

    def __init__(self):
        pass

    def file_to_list(self, filename):
        """ Parse a file and transform it into a list

        Parse a file line by line to make a list with the urls contained
        inside.

        Args:
            filename (str): path to the file containing the URLs.

        """
        lines = []
        with open(filename) as f:
            for line in f.readlines():
                lines.append(line.split('\n')[0])
        return lines

    def download(self, url_list, dest_dir):
        """ Download data from a list of URLs

        Download data from a list of URLs and display a progress according to
        the size of the file.

        Args:
            url_list(list): list containing URLs of files to download.
            dest_dir (str): path to where download the data.

        """
        elem_nb = len(url_list)
        counter = 0
        dest_dir = os.path.abspath(dest_dir)

        for elem in url_list:
            filename = elem.split('/')[-1]

            with open(dest_dir + '/' + filename, 'wb') as f:
                r = requests.get(elem, stream=True)
                dl = 0
                file_size = int(r.headers['Content-length'])
                if file_size is None:
                    f.write(r.conent)
                else:
                    counter += 1
                    for chunk in r.iter_content(chunk_size=1024):
                        dl += len(chunk)
                        f.write(chunk)
                        done = int(50 * dl / file_size)
                        sys.stdout.write(
                            "\r%s/%d [%s%s]" %
                            (counter, elem_nb, '=' * done, ' ' * (50-done)))
                        sys.stdout.flush()

            print('')

    def unzip_data(self, url_list, origin_dir, dest_dir):
        """ Unzip data files

        Unzip data files given a list of file names, the path where they are
        store and where they will be unzipped.

        Args:
            url_list (str): list of strings containing the urls
            origin_dir (str): directory where are stored the files
            dest_dir (str): directory where the files will be extracted
        """
        origin_dir = os.path.abspath(origin_dir)
        for elem in url_list:
            filename = os.path.basename(elem)
            zip_ref = zipfile.ZipFile(origin_dir + '/' + filename, 'r')
            zip_ref.extractall(dest_dir)
            zip_ref.close()

    def clear_zip(self, url_list, tmp_dir):
        """ Clear the archives

        Delete the downloaded archives.

        Args:
            url_list (str): list of strings containing the urls
            tmp_dir (str): path where are store the archives
        """
        for elem in url_list:
            #  filename = os.path.basename(elem)
            os.remove(tmp_dir + '/' + elem)
            print("%s deleted" % elem)

    def move_files(self, url_list, origin_dir, dest_dir):
        """ Move the audio files into the data folder

        Move the audio folder created by the unzipped archives into the data
        root folder. The function can specify the origin and destination folder
        but assumes that the audio files are located into an folder called
        'audio' and can't be changed.

        Args:
            url_list (list): list of all the archive URLs.
            origin_dir (str): directory of origin.
            dest_dir (str): directory of destination.

        Returns:
            None

        Todo:
            The fact that the 'audio' folder is hard coded makes this function
            rather bad and should be corrected in the future.

        """
        filename = os.path.basename(url_list[0])
        zip_ref = zipfile.ZipFile(origin_dir + '/' + filename, 'r')
        zip_info = zip_ref.infolist()
        folder_name = zip_info[0].filename
        origin_dir = os.path.join(origin_dir, folder_name, 'audio')
        dest_dir = os.path.abspath(dest_dir)

        shutil.move(origin_dir, dest_dir)
