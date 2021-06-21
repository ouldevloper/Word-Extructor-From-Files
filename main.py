from functools import singledispatch
import struct
import time
import sys
import os
import re
import json
import optparse
import sqlite3
from threading import Thread
import multiprocessing

class Extructor:
    def __init__(self,json_file=None,in_dir="in",out_dir="out"):
        self.in_dir=in_dir
        self.out_dir = out_dir
        self.json_file=json_file
        self.data = {}
        if json_file!=None:
            with open(json_file,'r') as file:
                self.data = json.load(file.read)



    def read_all(self,file_name:str):
        with open(os.path.join(self.in_dir,file_name),"r") as file:
            return file.read()

    def get_fieles(self):
        if not os.path.isdir(self.in_dir):
            os.mkdir(self.in_dir)
        dirs = os.listdir(self.in_dir)
        return list(filter(lambda sub_file : 
                                  os.path.isfile(os.path.join(self.in_dir,sub_file)) and 
                                  sub_file not in ['.','..'],
                                dirs))

    def filter_file_content(self,txt):
        regex = re.sub(r'^((\d(.)*\d)|\d|)$',"",txt,0,re.MULTILINE)
        return regex.replace('.','')\
                    .replace(',','')\
                    .replace('!','')\
                    .replace('?','')\
                    .replace('"','')\
                    .replace("'",'')\
                    .replace('\n\n','')
                    

    def tokenize(self,line,spliter=' '):
        return line.split(spliter)

    def fill_list(self,word):
        try:
            num = self.data[word]
            self.data[word]=num+1
        except:
            self.data[word]=1

    def sort_data(self):
        return 

    def run(self):
        print("Extruct Words from Files")
        i=0
        files = self.get_fieles()
        lenght =len(files)
        for file in files:
            file_data = self.read_all(file)
            file_data = self.filter_file_content(file_data)
            words = self.tokenize(file_data)
            len_words = len(words)
            for ii,word in enumerate(words):
                if word == "": continue
                self.fill_list(word)
                if ii==len_words-1:
                    sys.stdout.write(" File %d : %d%% > %.30s> \n"%(i+1,(ii*100)//len_words,'='*((ii*100)//len_words)))
                    sys.stdout.flush()
                    time.sleep(0.001)
                else:
                    sys.stdout.write(" File %d : %d%% > %.30s> \r"%(i+1,(ii*100)//len_words,'='*(((ii*100)//len_words)//3)))
                    sys.stdout.flush()
                    time.sleep(0.001)

            i+=1
        print("Add Words To Database....")
        self.add_to_db()
        #t1     = Thread(target=self.add_to_db(),args=())
        #t1.run()
        #t1.join()
        

    def add_to_db(self):
        con = sqlite3.connect("db.db")
        cur = con.cursor()
        index = 1
        lenght = len(self.data)
        for key,value in self.data.items():
            try:
                cur.execute(f"INSERT INTO WORDS VALUES('{index}','{key}','{value}')")
                index+=1
            except sqlite3.Error:
                pass
            else:
                con.commit()
            pos = (index*100)//lenght
            sys.stdout.write(" %d%% > %.33s> \r\r"%(pos,'='*(pos//3)))
            sys.stdout.flush()
    
    def console(self):
        index = 0 
        while 1:
            sys.stdout.write(" %d%% ===> %.100s \r\r"%(index,'+'*(index+1)))
            sys.stdout.flush()
            time.sleep(1)
            if index%100==0 and index!=0:
                index=0
                print()
            index+=1

x=Extructor()
x.run()
