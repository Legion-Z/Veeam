""" при необходимости можно изменить имя и расположение лог-файла (значение переменной log_file)"""


import os
import hashlib
import sys


in_file = os.path.abspath(sys.argv[1]) # input file with filenames
files_dir = os.path.abspath(sys.argv[2])# directory to search files
log_file = os.path.join(os.path.dirname(__file__),'task_2.log')# file to log checking results

class HashSumm():
    def __init__(self, hash_type:str, file:os.path) -> None:
        if hash_type == 'md5':
            self.hash_type = hashlib.md5
        elif hash_type == 'sha1':
            self.hash_type = hashlib.sha1
        elif hash_type == 'sha256':
            self.hash_type = hashlib.sha256
        self.file = file

    def hash_summ(self):
        res = self.hash_type()
        with open(self.file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                res.update(chunk)

        return res.hexdigest()
    

with open(log_file,'w',encoding='UTF-8') as lf:
    with open(in_file,'r',encoding='UTF-8') as in_file:
        for line in in_file:
            try:
                line_lst = line.split()
                f_name = os.path.join(files_dir,line_lst[0])
                chs = line_lst[2]
                hsumm = HashSumm(line_lst[1],f_name).hash_summ()
                if chs == hsumm:
                    lf.write(line_lst[0]+' OK\n')
                else:
                    lf.write(line_lst[0]+' FAIL\n')

            except FileNotFoundError:
                lf.write(line_lst[0]+' NOT FOUND\n')
            except Exception as e:
                lf.write(str(e)+'\n')

