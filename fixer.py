import sys
from array import *
import numpy as np
import pandas as pd
import csv

#switch column places
def df_column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df

if(len(sys.argv) >= 1):
    filename = sys.argv[1] #take the path file

    #name the new file
    if(len(sys.argv) <= 2):
        newFileName = "poprawiony.csv"
    else:
        newFileName = str(sys.argv[2])+".csv"

    #columns that had to have the ""
    quotes = ["Nadawca/Odbiorca","Opis","Rachunek nadawcy","Odbiorca","Kwota", "Nadawca","Saldo po operacji","Rachunek odbiorcy","Rodzaj operacji"]

    #read data from csv
    df = pd.read_csv(filename, index_col=0)


    #delete spaces from the account number
    ##########################################
    for index, row in df.iterrows():
        tmp = df.at[index, 'Rachunek odbiorcy']
        tmp = tmp[:-1]
        df.at[index, 'Rachunek odbiorcy'] = tmp
        #print(df.at[index, 'Rachunek odbiorcy'])

    for index, row in df.iterrows():
        tmp = df.at[index, 'Rachunek nadawcy']
        tmp = tmp[:-1]
        df.at[index, 'Rachunek nadawcy'] = tmp
    ###########################################

    #switch the columns
    #############################################################
    df = df_column_switch(df, 'Data operacji', 'Data księgowania')
    df = df_column_switch(df, 'Data operacji', 'Nadawca/Odbiorca')
    df = df_column_switch(df, 'Data operacji', 'Opis')
    df = df_column_switch(df, 'Data operacji', 'Kwota')
    #############################################################

    #add the quotes into specific columns
    for col in quotes:
        df[col] = '"' + df[col] + '"'

    #the following has to be done to delete unnecessary quotes, as the database wouldn't accept them
    df.to_csv("przejsciowy.csv", quoting=csv.QUOTE_MINIMAL, quotechar='"')

    #new file
    last = open("przejsciowy.csv", 'r', encoding="utf8")
    lastest = open(newFileName, 'w', encoding="utf8")

    #make new headers
    count = 0
    while True:
        line = last.readline()
        if(count == 0):
            lastest.write("LP,\"Data księgowania\",Nadawca/Odbiorca,Opis,Kwota,\"Saldo po operacji\",\"Data operacji\",Nadawca,\"Rachunek nadawcy\",Odbiorca,\"Rachunek odbiorcy\",\"Rodzaj operacji\"\n")
            count=1
        else:
            if not line:
                break
            line = line.replace("\"\"", "") #delete the double quotes
            lastest.write(line)

    

