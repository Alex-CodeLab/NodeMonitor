import datetime
import json
import os
import random
import string
import subprocess
import pathlib


def linecount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT
                           ).communicate()[0]
    return int(out.partition(b' ')[0])


def delete_first_lines(filename, line_nums):
    n = '1,{}d'.format(line_nums)
    subprocess.Popen(['sed', '-i', n, filename],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT
                     )


class Store():

    # max #lines per module
    maxsize = 1000

    def write(self, data):
        for module in data:
            for client in data[module]:
                dir_path = os.getcwd() + '/data/' + client
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                db_file = '{}/{}.db'.format(dir_path, module)
                with open(db_file, 'a') as f:
                    for line in data[module][client]:
                        f.write(line.rstrip() + '\n')

                c = linecount(db_file) - self.maxsize
                if c > 0:
                    delete_first_lines(db_file, c)

    def read(self, node, module):
        file_name = os.getcwd() + '/data/' + node + '/' + module + '.db'
        data = []

        file = pathlib.Path(file_name)
        if not file.exists():
            f = open(file, 'w+')

        with open(file_name, 'r') as f:
            for line in f:
                try:
                    data.append(json.loads(line.strip()))
                except:
                    pass
        return data
