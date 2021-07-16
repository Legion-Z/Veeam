"""по заданию Тестовая система представляет собой иерархию классов, описывающую тест-кейсы. 
в реальном проекте предпочел бы испольтзовать класс-агрегатор, чтобы снизить связность."""


import os
import random
import string
from psutil import virtual_memory
from datetime import datetime


log_file = os.path.join(os.path.dirname(__file__),'task_3.log')
test_file = os.path.join(os.path.dirname(__file__),'test')

class BaseTest():
    def __init__(self, tc_id:int, tc_name:str):
        self.tc_id = tc_id
        self.tc_name = tc_name

    def prep(self):
        pass

    def run(self):
        pass


    def clean_up(self):
        pass

    def execute(self):
        try:
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method PREP started at '+str(datetime.now()))
            self.prep()
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method PREP finished at '+str(datetime.now()))
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method RUN started at '+str(datetime.now()))
            self.run()
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method RUN finished at '+str(datetime.now()))
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method ClEAN_UP started at '+str(datetime.now()))
            self.clean_up()
            self.log('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' method CLEAN_UP finished at '+str(datetime.now()))
        except Exception as e:
            self.log(str(e))

    def log(self, text, file ='console'):
        if file == 'console': # log to console
            print(text)
        else: # log to file
            if os.path.isfile(file):
                with open(file,'a',encoding='UTF-8') as f:
                    f.write(text+'\n')
            else:
                with open(file,'w',encoding='UTF-8') as f:
                    f.write(text+'\n')



class TestFiles(BaseTest):
    def __init__(self, tc_id:int, tc_name:str):
        super().__init__(tc_id, tc_name)


    def prep(self):
        """Если текущее системное время, заданное как целое количество секунд от начала эпохи Unix, не кратно двум, то необходимо прервать выполнение тест-кейса."""
        
        if not (int(datetime.timestamp(datetime.now())) % 2):
            raise Exception('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' test was interrupted in method PREP at '+str(datetime.now()))


    def run(self):
        """Вывести список файлов из домашней директории текущего пользователя."""
        for item in os.scandir(os.path.expanduser('~')):
            if not item.name.startswith('.') and item.is_file():
                self.log(item.name+'\n')



class TestRandomFile(TestFiles):
    def __init__(self, tc_id: int, tc_name: str, filename: os.path):
        super().__init__(tc_id, tc_name)
        self.filename = filename

    def prep(self):
        """Если объем оперативной памяти машины, на которой исполняется тест, меньше одного гигабайта, то необходимо прервать выполнение тест-кейса."""
        if virtual_memory().total < 2**30:
            raise Exception('test id = '+str(self.tc_id)+' test name = '+self.tc_name+' test was interrupted in method PREP at '+str(datetime.now()))



    def run(self):
        """Создать файл test размером 1024 КБ со случайным содержимым."""
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=2**20))
        with open(self.filename,'w',encoding='UTF-8') as file:
            file.write(s)
            file.flush()

    def clean_up(self):
        """Удалить файл test"""
        os.remove(self.filename)



if __name__ == '__main__':
    tf = TestRandomFile(1,'Test case 1', test_file)
    tf.execute()
    print()
    tf = TestRandomFile(2,'Test case 2', test_file)
    tf.execute()