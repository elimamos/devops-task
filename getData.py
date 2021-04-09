#!/usr/bin/env python
import sys, getopt
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re
import os
import pandas as pd
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv

def main(argv):
    params={}
    page_content=''
    table=[]
    params=get_params(argv)
    page_content=get_page_source(params['source_url'])

    table=parse_page_source(page_content)
    plot_data(table[0])

# Plot the received data into a graph
def plot_data(filename):
    df =pd.read_csv(filename, sep=',')
    plt.figure(figsize=(35,15))

    plt.plot(df['Year'], df['Bicycle Production'], label='Bicycle Production',linestyle='-', marker='x')
    plt.plot(df['Year'], df['Auto Production'], label='Auto Production',linestyle='-', marker='x')
    plt.plot(df['Year'], df['Auto Fleet'], label='Auto Fleet',linestyle='-', marker='x')
    plt.gca().set_xticks(list(df['Year']))
    plt.gca().set_xticklabels(list(df['Year']))
    plt.legend()
    img_name=filename.replace(".csv",".png")
    plt.grid()

    plt.savefig(img_name)

def create_csv(filename):
    try:
        open(filename, "x")
    except:
        return False

def write_to_csv(filename, row):
    # The  data will be written to a CSV here.
    try:
        with open(filename, "a") as fopen:  # Open the csv file.
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(row)
    except Exception as ex:
        print("ERROR!", ex)
        return False

#read input params
def get_params(argv):
     inputfile = ''
     outputfile = ''
     params = {}
     try:
        opts, args = getopt.getopt(argv,"hu:",["url="])
     except getopt.GetoptError:
        print ('getData.py -u <inputfile')
        sys.exit(2)
     for opt, arg in opts:
       if opt in ('-h', "--help"):
           print('getData.py -u <inputfile>')
           sys.exit()
       elif opt in ("-u", "--url"):
           source_url = arg
           params['source_url'] = source_url

     return params

def get_page_source(source_url):
   # pretending to be a browser to receive the source of the page
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(source_url, headers=header)

    return r.text
#parse source of the page to retrive specific table
def parse_page_source(page_content):
     soup = BeautifulSoup(page_content, "html.parser")
     column_names=[]
     table_name=""
     table_data=[]
     outputfile=""
     table3=soup.find_all("table")[3]
     rows=table3.find_all("tr")
     index=0;
     has_column_name=False
     for row in rows:
         columns=row.find_all("td")
         current_row=[]
         for column in columns:
             if index==0:
                 table_name=re.sub(' +', ' ',column.text.strip().replace("\r","").replace("\n",""))
                 outputfile=table_name.replace(" ","_")+".csv"
                 if os.path.exists(outputfile):
                   os.remove(outputfile)
                 else:
                   print("The file does not exist")
                 create_csv(outputfile)
             elif index==1:
                 column_names.append(re.sub(' +', ' ',column.text.strip().replace("\r","").replace("\n","")))
             else:
                current_row.append(column.text.strip())
         if len(column_names)==4 and has_column_name==False:
             write_to_csv(outputfile,column_names)
             has_column_name=True
         if len(current_row)<3:
            print("WRONG ROW! ", index)
         else:
             table_data.append(current_row)
             write_to_csv(outputfile,current_row)
         index=index+1
     table = pd.DataFrame(table_data,columns=column_names)
     return [outputfile,table]

if __name__ == "__main__":
    main(sys.argv[1:])
