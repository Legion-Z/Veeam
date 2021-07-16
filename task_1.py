"""для нормальной работы необходимо правильно указать путь к файлу конфигурации и к файлу лога.
по умолчанию предполагается, что оба файла находятся по одному пути с исполняемым модулем и имеют имена
'task_1.config' и 'task_1.log' соответственно"""


import os
import xml.etree.ElementTree as ET
import shutil


cfg_file = os.path.join(os.path.dirname(__file__),'task_1.config')
log_file = os.path.join(os.path.dirname(__file__),'task_1.log')


tree = ET.parse(cfg_file)
root = tree.getroot()

with open(log_file,'w+',encoding='UTF-8') as lf:
    for child in root:
        try:
            source_path = os.path.abspath(child.attrib['source_path'])
            dest_path = os.path.abspath(child.attrib['destination_path'])
            file_name = child.attrib['file_name']
            source_file = os.path.join(source_path, file_name)
            dest_file = os.path.join(dest_path, file_name)
            lf.write('Trying to copy file '+str(source_file)+' to '+str(dest_file)+'\n')
            res = shutil.copy(source_file, dest_file)
            lf.write('Result: '+res+'\n')
        except Exception as e:
            lf.write(str(e)+'\n')
