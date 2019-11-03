import random
import string
import os
import subprocess
import datetime

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        ).communicate()[0]
    return int(out.partition(b' ')[0])

def delete_first_lines(filename, line_nums):
    n = '1,{}d'.format(line_nums)
    subprocess.Popen(['sed', '-i', n, filename ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )


class Db():

    maxsize = 2000

    def write(self, node, message, module):
        dir_path  = os.getcwd() + '/data/' + node
        if not os.path.exists(dir_path ):
            os.makedirs(dir_path)
        db_file = '{}/{}.db'.format(dir_path, module)

        with open(db_file, 'a') as f:
            f.write(message.rstrip() +'\n')

        c = wccount(db_file) - self.maxsize
        if c > 0:
            delete_first_lines(db_file, c)

    def read(self, node, module):

        file_name = os.getcwd() + '/data/' + node +'/'+ module + '.db'
        print(file_name)
        with open(file_name, 'r') as f:
            line = f.readline()
            module_data = []
            while line != '':
                m = {}
                m_data = line.split(' {')[0]
                c = m_data.split(' ')
                m['ts'] = c[0]
                m['node'] = c[1]
                m['module'] = c[2]
                print(m)
                line = f.readline()

    def read_main(self):
        block = []
        pass
