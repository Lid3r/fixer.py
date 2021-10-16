import sys
from array import *
import numpy as np
import pandas as pd
import csv

#zamiana miejscami kolumn
def df_column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df

if(len(sys.argv) >= 1):
    filename = sys.argv[1] #pobieranie ścieżki

    #nazywanie nowego pliku
    if(len(sys.argv) <= 2):
        newFileName = "poprawiony.csv"
    else:
        newFileName = str(sys.argv[2])+".csv"

    #lista kolumn do obłożenia cudzysłowami
    quotes = ["Nadawca/Odbiorca","Opis","Rachunek nadawcy","Odbiorca","Kwota", "Nadawca","Saldo po operacji","Rachunek odbiorcy","Rodzaj operacji"]

    #odczytywanie danych z bazowego pliku
    df = pd.read_csv(filename, index_col=0)


    #usuwanie spacji po numerze konta
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

    #Zamiana meijscami kolumn
    #############################################################
    df = df_column_switch(df, 'Data operacji', 'Data księgowania')
    df = df_column_switch(df, 'Data operacji', 'Nadawca/Odbiorca')
    df = df_column_switch(df, 'Data operacji', 'Opis')
    df = df_column_switch(df, 'Data operacji', 'Kwota')
    #############################################################

    #Cudzysłowia w kolumnach
    for col in quotes:
        df[col] = '"' + df[col] + '"'

    #Tworzenie przejściowego bo panda ma raka
    df.to_csv("przejsciowy.csv", quoting=csv.QUOTE_MINIMAL, quotechar='"')

    #ostatnia faza, tworzenie nowego pliku
    last = open("przejsciowy.csv", 'r', encoding="utf8")
    lastest = open(newFileName, 'w', encoding="utf8")

    #dla pierwszej lini te wszystkie headery z dobrymi cudzysłowiami
    count = 0
    while True:
        line = last.readline()
        if(count == 0):
            lastest.write("LP,\"Data księgowania\",Nadawca/Odbiorca,Opis,Kwota,\"Saldo po operacji\",\"Data operacji\",Nadawca,\"Rachunek nadawcy\",Odbiorca,\"Rachunek odbiorcy\",\"Rodzaj operacji\"\n")
            count=1
        else:
            if not line:
                break
            line = line.replace("\"\"", "") #usuwanie podwójnych cudzysłowów bo panda ma raka znowu
            lastest.write(line)

    

